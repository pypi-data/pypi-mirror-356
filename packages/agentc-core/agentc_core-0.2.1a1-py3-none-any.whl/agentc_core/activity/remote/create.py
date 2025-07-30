import couchbase.cluster
import logging
import pathlib

from agentc_core.defaults import DEFAULT_ACTIVITY_LOG_COLLECTION
from agentc_core.defaults import DEFAULT_ACTIVITY_SCOPE

logger = logging.getLogger(__name__)


def create_analytics_views(cluster: couchbase.cluster.Cluster, bucket: str) -> None:
    logger.debug("Creating analytics log scope.")
    ddl_result = cluster.analytics_query(f"""
        CREATE ANALYTICS SCOPE `{bucket}`.`{DEFAULT_ACTIVITY_SCOPE}`
        IF NOT EXISTS;
    """)
    for _ in ddl_result.rows():
        pass

    logger.debug("Creating analytics log collection.")
    ddl_result = cluster.analytics_query(f"""
        CREATE ANALYTICS COLLECTION
        IF NOT EXISTS
        `{bucket}`.`{DEFAULT_ACTIVITY_SCOPE}`.`{DEFAULT_ACTIVITY_LOG_COLLECTION}`
        ON `{bucket}`.`{DEFAULT_ACTIVITY_SCOPE}`.`{DEFAULT_ACTIVITY_LOG_COLLECTION}`;
    """)
    for _ in ddl_result.rows():
        pass

    # Onto to our View DDLs...
    ddls_folder = pathlib.Path(__file__).parent / "analytics"
    ddl_files = sorted(file for file in ddls_folder.iterdir())
    for ddl_file in ddl_files:
        with open(ddl_file, "r") as fp:
            raw_ddl_string = fp.read()
            ddl_string = (
                raw_ddl_string.replace("[BUCKET_NAME]", bucket)
                .replace("[SCOPE_NAME]", DEFAULT_ACTIVITY_SCOPE)
                .replace("[LOG_COLLECTION_NAME]", DEFAULT_ACTIVITY_LOG_COLLECTION)
            )
            logger.debug(f"Issuing the following statement: {ddl_string}")

            ddl_result = cluster.analytics_query(ddl_string)
            for _ in ddl_result.rows():
                pass


def create_query_udfs(cluster: couchbase.cluster.Cluster, bucket: str) -> None:
    udfs_folder = pathlib.Path(__file__).parent / "query"
    udfs_files = sorted(file for file in udfs_folder.iterdir())
    for udf_file in udfs_files:
        with open(udf_file, "r") as fp:
            raw_udf_string = fp.read()
            udf_string = (
                raw_udf_string.replace("[BUCKET_NAME]", bucket)
                .replace("[SCOPE_NAME]", DEFAULT_ACTIVITY_SCOPE)
                .replace("[LOG_COLLECTION_NAME]", DEFAULT_ACTIVITY_LOG_COLLECTION)
            )
            logger.debug(f"Issuing the following statement: {udf_string}")

            ddl_result = cluster.query(udf_string)
            for _ in ddl_result.rows():
                pass
