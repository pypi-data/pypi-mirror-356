import logging
import re
import time
from datetime import datetime, timedelta
from typing import Optional, List, Tuple, Iterator, Sequence, Union

import pandas as pd
from iotdb import SessionPool
from iotdb.Session import Session
from iotdb.SessionPool import create_session_pool, PoolConfig

from gxkit_dbtools.client.base import BaseDBClient
from gxkit_dbtools.exception import DBConnectionError, SQLExecutionError
from gxkit_dbtools.parser.sql_parser import SQLParser

try:
    # 3.x path
    from iotdb.utils.IoTDBConnectionException import IoTDBConnectionException
except ImportError:
    try:
        # 2.x path
        from iotdb.utils.exception import IoTDBConnectionException
    except ImportError:
        # 1.x path
        try:
            from iotdb.utils import IoTDBConnectionException
        except ImportError:
            raise ImportError(
                "[IoTDBClient] Failed to import IoTDBConnectionException. Please ensure you have installed a compatible version of apache-iotdb"
            )


class BaseClient(BaseDBClient):
    """IoTDB 基础客户端"""

    def __init__(self, **connection_params):
        self.db_type = "iotdb"
        self._connection_params = connection_params

    # BaseDBClient abstract methods -------------------------------------------------
    def connect(self, *args, **kwargs):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def _get_session(self):
        raise NotImplementedError

    def _return_session(self, session):
        pass

    def execute(self, sql: str, auto_decision: bool = False, stream: bool = False, batch_size: Optional[int] = 10000,
                prefix_path: int = 1, use_native: bool = False, max_retry: int = 3, ) -> Union[
        pd.DataFrame, Iterator[pd.DataFrame], int, None]:
        session = self._get_session()
        if session is None:
            raise DBConnectionError("dbtools.IoTDBClient.execute", "iotdb", "Database not connected")
        parsed_sql = SQLParser(sql, db_type="iotdb")
        sql_type = parsed_sql.sql_type()

        if sql_type == "statement" and stream:
            logging.warning(
                "[dbtools.IoTDBClient.execute] | Stream function unsupported for this SQL. Using normal execution."
            )
            stream = False
        stream_started = False
        try:
            if auto_decision and sql_type == "query":
                try:
                    need_page, limit_size = self._decision(session, sql, parsed_sql, prefix_path)
                except Exception:
                    if stream:
                        self._return_session(session)
                    raise
                if need_page:
                    if stream:
                        batch_size = self._adjust_batch_size_for_limit(batch_size, limit_size, context="execute")
                        result = self._stream_core(session, parsed_sql, batch_size, prefix_path)
                        stream_started = True
                        return result
                    return self._execute_stream_core(session, parsed_sql, limit_size, prefix_path)
            if stream and sql_type == "query":
                result = self._stream_core(session, parsed_sql, batch_size, prefix_path)
                stream_started = True
                return result
            return self._execute_core(session, sql, sql_type, prefix_path)
        except Exception as e:  # pragma: no cover - thin wrapper
            if stream and sql_type == "query" and not stream_started:
                self._return_session(session)
            raise SQLExecutionError("dbtools.IoTDBClient.execute", sql, str(e)) from e
        finally:
            if not (stream and sql_type == "query"):
                self._return_session(session)

    def executemany(self, sqls: Sequence[str], auto_decision: bool = False, stream: bool = False,
                    batch_size: Optional[int] = 10000, collect_results: bool = True, prefix_path: int = 1,
                    use_native: bool = False, max_retry: int = 3) -> List[Union[pd.DataFrame, int, None]]:
        if not isinstance(sqls, Sequence) or isinstance(sqls, str) or not sqls:
            raise SQLExecutionError("dbtools.IoTDBClient.executemany", str(sqls), "unsupported sqls type")

        results: List[Union[pd.DataFrame, int, None]] = []
        for sql in sqls:
            parsed_sql = SQLParser(sql, db_type="iotdb")
            sql_type = parsed_sql.sql_type()
            result = self.execute(
                sql,
                auto_decision=auto_decision,
                stream=stream,
                batch_size=batch_size,
                prefix_path=prefix_path,
                use_native=use_native,
                max_retry=max_retry,
            )
            if collect_results and sql_type == "query":
                results.append(result)

        return results if collect_results else []

    def _decision(self, session, sql: str, parsed_sql: SQLParser, prefix_path: int) -> Tuple[bool, int]:
        max_columns = 200
        max_rows = 100_000
        max_cells = 750_000
        max_limits = 20_000
        fallback_limit = 10_000
        small_limit_threshold = 2_000

        if parsed_sql.sql_type() != "query":
            return False, fallback_limit
        if parsed_sql.operation() not in {"select", "union", "intersect", "except", "with"}:
            return False, fallback_limit

        try:
            columns = self._get_columns(session, parsed_sql, prefix_path)
            column_count = len(columns)
            if column_count == 0:
                return False, fallback_limit
            if column_count == 1 and re.match(r"(?i)\b(count|sum|avg|min|max)\s*\(.*\)", columns[0]):
                return False, 1

            user_limit = parsed_sql.segments("limit").get("limit")
            if user_limit:
                try:
                    limit_value = int(user_limit[0].split()[1])
                    if limit_value <= small_limit_threshold:
                        return False, limit_value
                except Exception:
                    pass

            count_column = columns[1].split(".")[-1] if len(columns) > 1 else columns[0].split(".")[-1]
            row_count = self._get_rows(session, parsed_sql, count_column)

            limit_value = min(max(1, max_cells // column_count), max_limits)
            if row_count:
                limit_value = min(limit_value, row_count)
            cell_score = (column_count * row_count) / max_cells
            need_page = cell_score > 1.0 or column_count > max_columns or row_count > max_rows

            return need_page, limit_value
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

    def _execute_stream_core(self, session, parsed_sql: SQLParser, batch_size: int, prefix_path: int) -> Optional[
        pd.DataFrame]:
        dfs = list(self._paged_generator(session, parsed_sql, batch_size, prefix_path))
        if not dfs:
            return None
        return pd.concat(dfs, ignore_index=True)

    def _stream_core(self, session, parsed_sql: SQLParser, batch_size: int, prefix_path: int) -> Optional[
        Iterator[pd.DataFrame]]:
        generator = self._paged_generator(session, parsed_sql, batch_size, prefix_path)
        try:
            first_batch = next(generator)
        except StopIteration:
            self._return_session(session)
            return None
        except Exception:
            self._return_session(session)
            raise

        def stream_generator():
            try:
                yield first_batch
                for batch in generator:
                    yield batch
            finally:
                self._return_session(session)

        return stream_generator()

    def _paged_generator(self, session, parsed_sql: SQLParser, limit: int, prefix_path: int, col_time: str = "Time") -> \
            Iterator[pd.DataFrame]:
        seg_where = parsed_sql.segments("where").get("where")
        original_where = seg_where[0] if seg_where else None
        start_ts, end_ts = None, None

        if original_where:
            time_start_pattern = rf"(?i)\b{col_time}\s*(>=|>)\s*(\d+(?:\.\d+)?|'[^']+'|\"[^\"]+\")"
            time_end_pattern = rf"(?i)\b{col_time}\s*(<=|<)\s*(\d+(?:\.\d+)?|'[^']+'|\"[^\"]+\")"
            match_start = re.search(time_start_pattern, original_where)
            match_end = re.search(time_end_pattern, original_where)
            if match_start:
                start_ts = match_start.group(2).strip("'\"")
            if match_end:
                end_ts = match_end.group(2).strip("'\"")

        last_ts = start_ts
        prev_ts = None

        while True:
            logging.debug(f"[IoTDBClient._paged_generator] | last_ts: {last_ts}")
            final_where = None
            if original_where:
                cond = f"{col_time} > {last_ts}" if last_ts else None
                if cond:
                    time_gt_pattern = rf"(?i)\b{col_time}\s*(>=|>)\s*(\d+(?:\.\d+)?|'[^']+'|\"[^\"]+\")"
                    if re.search(time_gt_pattern, original_where):
                        final_where = re.sub(time_gt_pattern, cond, original_where, count=1)
                    else:
                        final_where = f"({original_where}) AND {cond}"
                else:
                    final_where = original_where
            elif last_ts:
                final_where = f"{col_time} > {last_ts}"

            replacements = {"limit": str(limit)}
            if final_where:
                replacements["where"] = final_where
            page_sql = parsed_sql.change_segments(replacements)
            logging.debug(f"[IoTDBClient._paged_generator] | final_where: {final_where}")
            logging.debug(f"[IoTDBClient._paged_generator] | page_sql: {page_sql}")

            df = self._execute_core(session, page_sql, "query", prefix_path)
            if df is None or df.empty:
                break

            df.columns = self._build_col_mapping(list(df.columns), prefix_path)
            yield df

            if len(df) < limit:
                break

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
                logging.warning(
                    "[IoTDBClient._paged_generator] | Timestamp not progressing. Breaking to avoid loop."
                )
                break

            if end_ts is not None and float(last_ts) >= float(end_ts):
                break
            prev_ts = last_ts

    def _execute_core(self, session, sql: str, sql_type: str, prefix_path: int) -> Union[pd.DataFrame, int, None]:
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
                inner = col[start + 1: end]
                if "." in inner:
                    inner_short = ".".join(inner.split(".")[-prefix_path:]) if prefix_path > 0 else inner
                    return f"{col[: start + 1]}{inner_short}{col[end:]}"
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
                f"[IoTDBClient.{context}] | batch_size ({batch_size}) exceeds optimal limit ({limit_size}). Using limit_size instead."
            )
            return limit_size
        return batch_size


class IoTDBClient(BaseClient):
    """IoTDB 客户端(非线程池版)"""

    def __init__(self, host: str, port: int, user: str, password: str, **kwargs):
        super().__init__(host=host, port=port, user=user, password=password, **kwargs)
        self.session: Optional[Session] = None
        self._last_success_time: Optional[datetime] = None
        self._reconnect_delay: timedelta = timedelta(minutes=10)
        self.connect(host, port, user, password, **kwargs)

    def _check_and_reconnect(self):
        if self.session is None or self._last_success_time is None:
            return

        now = datetime.now()
        if now - self._last_success_time > self._reconnect_delay:
            try:
                logging.info("[dbtools.IoTDBClient] Reconnecting due to inactivity timeout")
                self.session.execute_query_statement("SHOW STORAGE GROUP").close_operation_handle()
                self._last_success_time = now
            except Exception:
                logging.warning("[dbtools.IoTDBClient] Ping failed, reconnecting from scratch...")
                try:
                    self.close()
                finally:
                    self.connect(**self._connection_params)
                self._last_success_time = datetime.now()

    def connect(self, host: str, port: int, user: str, password: str, **kwargs) -> None:
        try:
            self.session = Session(host, port, user, password, **kwargs)
            self.session.open(False)
            self.session.execute_query_statement("SHOW STORAGE GROUP").close_operation_handle()
            self._last_success_time = datetime.now()
        except Exception as e:
            raise DBConnectionError("dbtools.IoTDBClient.connect", "iotdb", str(e)) from e

    def _get_session(self):
        if self.session is None:
            raise DBConnectionError("dbtools.IoTDBClient.execute", "iotdb", "Database not connected")
        return self.session

    def execute(self, sql: str, auto_decision: bool = False, stream: bool = False,
                batch_size: Optional[int] = 10000, prefix_path: int = 1,
                use_native: bool = False, max_retry: int = 3) -> Union[
        pd.DataFrame, Iterator[pd.DataFrame], int, None]:
        last_error = None
        for attempt in range(1, max_retry + 1):
            session = self._get_session()
            parsed_sql = SQLParser(sql, db_type="iotdb")
            sql_type = parsed_sql.sql_type()

            if sql_type == "statement" and stream:
                logging.warning(
                    "[dbtools.IoTDBClient.execute] | Stream function unsupported for this SQL. Using normal execution."
                )
                stream = False

            stream_started = False
            try:
                self._check_and_reconnect()
                if auto_decision and sql_type == "query":
                    need_page, limit_size = self._decision(session, sql, parsed_sql, prefix_path)
                    if need_page:
                        if stream:
                            batch_size = self._adjust_batch_size_for_limit(batch_size, limit_size, context="execute")
                            result = self._stream_core(session, parsed_sql, batch_size, prefix_path)
                            stream_started = True
                            self._last_success_time = datetime.now()
                            return result
                        result = self._execute_stream_core(session, parsed_sql, limit_size, prefix_path)
                        self._last_success_time = datetime.now()
                        return result
                if stream and sql_type == "query":
                    result = self._stream_core(session, parsed_sql, batch_size, prefix_path)
                    stream_started = True
                    self._last_success_time = datetime.now()
                    return result
                result = self._execute_core(session, sql, sql_type, prefix_path)
                self._last_success_time = datetime.now()
                return result
            except IoTDBConnectionException as e:
                last_error = e
                logging.warning(f"[IoTDBClient.execute] Retry {attempt}/{max_retry} after IoTDBConnectionException: {e}")
                self.close()
                self.connect(**self._connection_params)
                time.sleep(1)
            except Exception as e:
                if stream and sql_type == "query" and not stream_started:
                    self._return_session(session)
                raise SQLExecutionError("dbtools.IoTDBClient.execute", sql, str(e)) from e
            finally:
                if not (stream and sql_type == "query") or last_error is not None:
                    self._return_session(session)

        raise SQLExecutionError("dbtools.IoTDBClient.execute", sql, f"Failed after {max_retry} retries")

    def close(self) -> None:
        if self.session:
            try:
                self.session.close()
            except Exception:
                pass
            self.session = None


class IoTDBPoolClient(BaseClient):
    """IoTDB 客户端(线程池版)"""

    def __init__(self, host: str, port: int, user: str, password: str, max_pool_size: int = 10,
                 wait_timeout_in_ms: int = 3000, **kwargs):
        super().__init__(host=host, port=port, user=user, password=password, max_pool_size=max_pool_size,
                         wait_timeout_in_ms=wait_timeout_in_ms, **kwargs)
        self.pool: Optional[SessionPool] = None
        self.connect(host, port, user, password, max_pool_size, wait_timeout_in_ms, **kwargs)

    def connect(self, host: str, port: int, user: str, password: str, max_pool_size: int, wait_timeout_in_ms: int,
                retry: int = 3, **kwargs) -> None:
        try:
            config = PoolConfig(host=host, port=str(port), user_name=user, password=password, **kwargs)
            self.pool = create_session_pool(config, max_pool_size=max_pool_size, wait_timeout_in_ms=wait_timeout_in_ms)
            last_error = None

            for attempt in range(1, retry + 1):
                try:
                    session = self.pool.get_session()
                    try:
                        session.execute_query_statement("SHOW STORAGE GROUP").close_operation_handle()
                    finally:
                        self.pool.put_back(session)
                    return
                except Exception as e:
                    if type(e).__name__ == "IoTDBConnectionException":
                        last_error = e
                        if attempt < retry:
                            logging.warning(
                                f"[IoTDBClient.connect] Retry {attempt}/{retry} after IoTDBConnectionException: {e}"
                            )
                        else:
                            break
                    else:
                        raise DBConnectionError("dbtools.IoTDBClient.connect", "iotdb", str(e)) from e

            raise DBConnectionError("dbtools.IoTDBClient.connect", "iotdb", str(last_error)) from last_error

        except Exception as e:
            raise DBConnectionError("dbtools.IoTDBClient.connect", "iotdb", str(e)) from e

    def _get_session(self):
        if self.pool is None:
            raise DBConnectionError("dbtools.IoTDBClient.execute", "iotdb", "Database not connected")
        last_error = None
        for attempt in range(1, 4):
            try:
                return self.pool.get_session()
            except Exception as e:
                last_error = e
                logging.warning(
                    f"[IoTDBPoolClient._get_session] Retry {attempt}/3 after {type(e).__name__}: {e}"
                )
                time.sleep(0.5)
        raise DBConnectionError("dbtools.IoTDBClient.execute", "iotdb", str(last_error)) from last_error

    def _return_session(self, session):
        if self.pool is None:
            return
        last_error = None
        for attempt in range(1, 4):
            try:
                self.pool.put_back(session)
                return
            except Exception as e:
                last_error = e
                logging.warning(
                    f"[IoTDBPoolClient._return_session] Retry {attempt}/3 after {type(e).__name__}: {e}"
                )
                time.sleep(0.5)
        logging.error(
            f"[IoTDBPoolClient._return_session] Failed to return session after 3 retries: {last_error}"
        )

    def execute(
        self,
        sql: str,
        auto_decision: bool = False,
        stream: bool = False,
        batch_size: Optional[int] = 10000,
        prefix_path: int = 1,
        use_native: bool = False,
        max_retry: int = 3,
    ) -> Union[pd.DataFrame, Iterator[pd.DataFrame], int, None]:
        last_error = None
        for attempt in range(1, max_retry + 1):
            session = self._get_session()
            parsed_sql = SQLParser(sql, db_type="iotdb")
            sql_type = parsed_sql.sql_type()

            if sql_type == "statement" and stream:
                logging.warning(
                    "[dbtools.IoTDBClient.execute] | Stream function unsupported for this SQL. Using normal execution."
                )
                stream = False

            stream_started = False
            try:
                if auto_decision and sql_type == "query":
                    need_page, limit_size = self._decision(session, sql, parsed_sql, prefix_path)
                    if need_page:
                        if stream:
                            batch_size = self._adjust_batch_size_for_limit(batch_size, limit_size, context="execute")
                            result = self._stream_core(session, parsed_sql, batch_size, prefix_path)
                            stream_started = True
                            return result
                        return self._execute_stream_core(session, parsed_sql, limit_size, prefix_path)
                if stream and sql_type == "query":
                    result = self._stream_core(session, parsed_sql, batch_size, prefix_path)
                    stream_started = True
                    return result
                result = self._execute_core(session, sql, sql_type, prefix_path)
                return result
            except IoTDBConnectionException as e:
                last_error = e
                logging.warning(
                    f"[IoTDBClient.execute] Retry {attempt}/{max_retry} after IoTDBConnectionException: {e}")
                self.close()
                self.connect(**self._connection_params)
                time.sleep(1)
            except Exception as e:
                if stream and sql_type == "query" and not stream_started:
                    self._return_session(session)
                raise SQLExecutionError("dbtools.IoTDBClient.execute", sql, str(e)) from e
            finally:
                if not (stream and sql_type == "query") or last_error is not None:
                    self._return_session(session)

        raise SQLExecutionError("dbtools.IoTDBClient.execute", sql, f"Failed after {max_retry} retries")

    def close(self) -> None:
        if self.pool:
            try:
                self.pool.close()
            except Exception:
                pass
            self.pool = None
