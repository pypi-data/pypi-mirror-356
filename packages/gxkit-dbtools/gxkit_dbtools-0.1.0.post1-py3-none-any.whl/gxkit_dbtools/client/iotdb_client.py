import logging
import re
import math
import pandas as pd
from typing import Optional, List, Tuple, Iterator, Sequence, Union, Any
from iotdb import SessionPool
from iotdb.SessionPool import create_session_pool, PoolConfig
from iotdb.utils.exception import IoTDBConnectionException
from gxkit_dbtools.parser.sql_parser import SQLParser
from gxkit_dbtools.client.base import BaseDBClient
from gxkit_dbtools.exceptions import DBConnectionError, SQLExecutionError


class IoTDBClient(BaseDBClient):
    """
    IoTDBClient - Apache IoTDB 原生客户端
    Version: 0.1.0
    """

    def __init__(self, host: str, port: int, user: str, password: str, max_pool_size: int = 10,
                 wait_timeout_in_ms: int = 3000, **kwargs):
        self.pool: Optional[SessionPool] = None
        self.db_type = "iotdb"
        self._connection_params = dict(host=host, port=port, user=user, password=password,
                                       max_pool_size=max_pool_size,
                                       wait_timeout_in_ms=wait_timeout_in_ms, **kwargs)
        self.connect(host, port, user, password, max_pool_size, wait_timeout_in_ms, **kwargs)

    def connect(self, host: str, port: int, user: str, password: str, max_pool_size: int, wait_timeout_in_ms: int,
                retry: int = 3, **kwargs) -> None:
        try:
            config = PoolConfig(host=host, port=str(port), user_name=user, password=password, **kwargs)
            self.pool = create_session_pool(config, max_pool_size=max_pool_size,
                                            wait_timeout_in_ms=wait_timeout_in_ms)
            last_error = None
            for attempt in range(1, retry + 1):
                try:
                    session = self.pool.get_session()
                    try:
                        session.execute_query_statement("SHOW STORAGE GROUP").close_operation_handle()
                    finally:
                        self.pool.put_back(session)
                    return
                except IoTDBConnectionException as e:
                    last_error = e
                    if attempt < retry:
                        logging.warning(
                            f"[IoTDBClient.connect] Retry {attempt}/{retry} after IoTDBConnectionException: {e}"
                        )
                    else:
                        break
            raise DBConnectionError("dbtools.IoTDBClient.connect", "iotdb", str(last_error)) from last_error

        except Exception as e:
            raise DBConnectionError("dbtools.IoTDBClient.connect", "iotdb", str(e)) from e

    def execute(self, sql: str, auto_decision: bool = False, stream: bool = False, batch_size: Optional[int] = 10000,
                prefix_path: int = 1, use_native: bool = False, max_retry: int = 3) -> Union[
        pd.DataFrame, Iterator[pd.DataFrame], int, None]:
        if self.pool is None:
            raise DBConnectionError("dbtools.IoTDBClient.execute", "iotdb", "Database not connected")
        parsed_sql = SQLParser(sql, db_type="iotdb")
        sql_type = parsed_sql.sql_type()
        session = self.pool.get_session()

        if sql_type == "statement" and stream:
            logging.warning(
                "[dbtools.IoTDBClient.execute] | Stream function unsupported for this SQL. Using normal execution.")
            stream = False
        try:
            if auto_decision and sql_type == "query":
                need_page, limit_size, max_iter = self._decision(session, sql, parsed_sql, prefix_path)
                if need_page:
                    if stream:
                        batch_size = self._adjust_batch_size_for_limit(batch_size, limit_size, context="execute")
                        return self._stream_core(session, parsed_sql, batch_size, prefix_path, max_iter)
                    return self._execute_stream_core(session, parsed_sql, limit_size, prefix_path, max_iter)
            if stream and sql_type == "query":
                return self._stream_core(session, parsed_sql, batch_size, prefix_path)
            return self._execute_core(session, sql, sql_type, prefix_path)
        except Exception as e:
            raise SQLExecutionError("dbtools.IoTDBClient.execute", sql, str(e)) from e
        finally:
            if not (stream and sql_type == "query"):
                self.pool.put_back(session)

    def executemany(self, sqls: Sequence[str], auto_decision: bool = False, stream: bool = False,
                    batch_size: Optional[int] = 10000, collect_results: bool = True, prefix_path: int = 1,
                    use_native: bool = False, max_retry: int = 3) -> List[Union[pd.DataFrame, int, None]]:
        if not isinstance(sqls, Sequence) or isinstance(sqls, str) or not sqls:
            raise SQLExecutionError("dbtools.IoTDBClient.executemany", str(sqls), "unsupported sqls type")

        results: List[Union[pd.DataFrame, int, None]] = []
        for sql in sqls:
            parsed_sql = SQLParser(sql, db_type="iotdb")
            sql_type = parsed_sql.sql_type()
            result = self.execute(sql, auto_decision=auto_decision, stream=stream,
                                  batch_size=batch_size, prefix_path=prefix_path,
                                  use_native=use_native, max_retry=max_retry)
            if collect_results and sql_type == "query":
                results.append(result)

        return results if collect_results else []

    def close(self) -> None:
        if self.pool:
            try:
                self.pool.close()
            except Exception:
                pass
            self.pool = None

    def _decision(self, session, sql: str, parsed_sql: SQLParser, prefix_path: int) -> Tuple[bool, int, Optional[int]]:
        max_columns = 200
        max_rows = 100_000
        max_cells = 750_000
        max_limits = 20_000
        fallback_limit = 10_000
        small_limit_threshold = 2_000

        if parsed_sql.sql_type() != "query":
            return False, fallback_limit, None
        if parsed_sql.operation() not in {"select", "union", "intersect", "except", "with"}:
            return False, fallback_limit, None

        try:
            columns = self._get_columns(session, parsed_sql, prefix_path)
            column_count = len(columns)
            # 空字段直接return
            if column_count == 0:
                return False, fallback_limit, None
            # 聚合函数单字段直接return
            if column_count == 1 and re.match(r"(?i)\b(count|sum|avg|min|max)\s*\(.*\)", columns[0]):
                return False, 1, 1

            # sql中主动设定了 limit
            user_limit = parsed_sql.segments("limit").get("limit")
            if user_limit:
                try:
                    limit_value = int(user_limit[0].split()[1])
                    if limit_value <= small_limit_threshold:
                        return False, limit_value, 1
                except Exception:
                    pass

            # 获取数据总行数
            count_column = columns[1].split(".")[-1] if len(columns) > 1 else columns[0].split(".")[-1]
            row_count = self._get_rows(session, parsed_sql, count_column)

            limit_value = min(max(1, max_cells // column_count), max_limits)
            if row_count:
                limit_value = min(limit_value, row_count)
            cell_score = (column_count * row_count) / max_cells
            need_page = cell_score > 1.0 or column_count > max_columns or row_count > max_rows

            max_iterations = math.ceil(row_count / limit_value) if row_count else None
            return need_page, limit_value, max_iterations
        except Exception as e:
            raise SQLExecutionError("dbtools.IoTDBClient._decision", sql, str(e)) from e

    def _get_columns(self, session, parsed_sql: SQLParser, prefix_path: int) -> Optional[List[str]]:
        try:
            column_sql = parsed_sql.change_segments({"limit": "10"})
            df = self._query_dataframe(session, column_sql, prefix_path)
            return [] if df is None else list(df.columns)
        except Exception:
            return []

    def _get_rows(self, session, parsed_sql: SQLParser, column: str) -> int:
        limit = parsed_sql.segments("limit").get("limit")
        count_limit = None if not limit else int(limit[0].split()[1])
        try:
            count_sql = SQLParser(parsed_sql.change_columns(f"count({column})"), db_type="iotdb").sql()
        except Exception:
            inner_sql = parsed_sql.sql()
            count_sql = f"SELECT count(*) FROM ({inner_sql})"
        count_df = self._execute_core(session, count_sql, "query", 1)
        count_lines = int(count_df.iloc[0, 0]) if count_df is not None else 0
        return min(count_limit, count_lines) if count_limit else count_lines

    def _execute_stream_core(self, session, parsed_sql: SQLParser, batch_size: int, prefix_path: int,
                              max_iterations: Optional[int] = None) -> Optional[pd.DataFrame]:
        dfs = list(self._paged_generator(session, parsed_sql, batch_size, prefix_path, max_iterations))
        if not dfs:
            return None
        return pd.concat(dfs, ignore_index=True)

    def _stream_core(self, session, parsed_sql: SQLParser, batch_size: int, prefix_path: int,
                      max_iterations: Optional[int] = None) -> Optional[Iterator[pd.DataFrame]]:
        generator = self._paged_generator(session, parsed_sql, batch_size, prefix_path, max_iterations)
        try:
            first_batch = next(generator)
        except StopIteration:
            self.pool.put_back(session)
            return None

        def stream_generator():
            try:
                yield first_batch
                for batch in generator:
                    yield batch
            finally:
                # 当 generator 消耗完或被外部终止时，释放 session
                self.pool.put_back(session)

        return stream_generator()

    def _paged_generator(self, session, parsed_sql: SQLParser, limit: int, prefix_path: int,
                         max_iterations: Optional[int] = None) -> Iterator[pd.DataFrame]:
        seg_where = parsed_sql.segments('where').get('where')
        original_where = seg_where[0] if seg_where else None
        start_ts, end_ts = None, None
        if original_where:
            time_start_pattern = r"(?i)\bTime\s*(>=|>)\s*(\d+(?:\.\d+)?|'[^']+'|\"[^\"]+\")"
            time_end_pattern = r"(?i)\bTime\s*(<=|<)\s*(\d+(?:\.\d+)?|'[^']+'|\"[^\"]+\")"
            match_start = re.search(time_start_pattern, original_where)
            match_end = re.search(time_end_pattern, original_where)
            if match_start:
                start_ts = match_start.group(2).strip("'\"")
            if match_end:
                end_ts = match_end.group(2).strip("'\"")
        last_ts = start_ts
        if max_iterations is None:
            max_iterations = 1000
        iteration = 0

        while True:
            iteration += 1
            if iteration >= max_iterations:
                logging.warning("[IoTDBClient._paged_generator] | Reached max page iterations.")
                break
            logging.debug(f"[IoTDBClient._paged_generator] | last_ts: {last_ts}")
            if original_where and original_where.strip():
                where_clause = original_where.strip()
                cond = f"Time > {last_ts}" if last_ts is not None else None
                if cond:
                    time_gt_pattern = r"(?i)\bTime\s*(>=|>)\s*(\d+(?:\.\d+)?|'[^']+'|\"[^\"]+\")"
                    if re.search(time_gt_pattern, where_clause):
                        final_where = re.sub(time_gt_pattern, cond, where_clause, count=1)
                    else:
                        final_where = f"({where_clause}) AND {cond}"
                else:
                    final_where = where_clause
            elif last_ts:
                final_where = f"Time > {last_ts}"
            else:
                final_where = None
            logging.debug(f"[IoTDBClient._paged_generator] | final_where: {final_where}")
            replacements = {"limit": str(limit)}
            if final_where:
                replacements["where"] = final_where
            page_sql = parsed_sql.change_segments(replacements)
            logging.debug(f"[IoTDBClient._paged_generator] | page_sql: {page_sql}")
            df = self._execute_core(session, page_sql, "query", prefix_path)
            if df is None or df.empty:
                break
            yield df
            if len(df) < limit:
                break
            prev_ts = last_ts
            ts_max = df["timestamp"].max()
            if pd.notnull(ts_max):
                try:
                    last_ts = int(ts_max) + 1
                except Exception:
                    logging.warning(f"[IoTDBClient._paged_generator] | Invalid timestamp {ts_max}")
                    break
            else:
                break
            if last_ts == prev_ts:
                logging.warning("[IoTDBClient._paged_generator] | Timestamp not progressing. Breaking to avoid loop.")
                break
            if end_ts is not None and float(last_ts) >= float(end_ts):
                break

    def _execute_core(self, session, sql: str, sql_type: str, prefix_path: int) -> Union[
        pd.DataFrame, int, None]:
        if sql_type != "query":
            session.execute_non_query_statement(sql)
            return 1
        return self._query_dataframe(session, sql, prefix_path)

    def _query_dataframe(self, session, sql: str, prefix_path: int) -> Optional[pd.DataFrame]:
        result = session.execute_query_statement(sql)
        df = result.todf()
        result.close_operation_handle()
        if df is None or df.empty:
            return None
        df.columns = self._build_col_mapping(list(df.columns), prefix_path)
        return df

    @staticmethod
    def _build_col_mapping(raw_cols: List[str], prefix_path: int) -> List[str]:
        def shorten(col: str) -> str:
            if col.lower() == "time":
                return "timestamp"

            if "(" in col and ")" in col:
                start = col.index("(")
                end = col.rindex(")")
                inner = col[start + 1:end]
                if "." in inner:
                    inner_short = ".".join(inner.split(".")[-prefix_path:]) if prefix_path > 0 else inner
                    return f"{col[:start + 1]}{inner_short}{col[end:]}"
                return col

            parts = col.split(".")
            return ".".join(parts[-prefix_path:]) if prefix_path > 0 else col

        return [shorten(col) for col in raw_cols]

    @staticmethod
    def _adjust_batch_size_for_limit(batch_size: int, limit_size: int, context: str = "execute") -> int:
        if batch_size is None or batch_size <= 0:
            return limit_size
        elif batch_size > limit_size:
            logging.warning(
                f"[IoTDBClient.{context}] | batch_size ({batch_size}) exceeds optimal limit ({limit_size}). "
                f"Using limit_size instead.")
            return limit_size
        return batch_size
