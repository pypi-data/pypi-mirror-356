import os

from weni_datalake_sdk.clients.redshift.redshift_client import query_dc_api


def get_events(**kwargs) -> dict:
    metric = os.environ.get("EVENTS_METRIC_NAME")

    if not kwargs.get("project"):
        raise Exception("Project is required")

    if not kwargs.get("date_start"):
        raise Exception("Date start is required")

    if not kwargs.get("date_end"):
        raise Exception("Date end is required")

    try:
        result = query_dc_api(metric=metric, query_params=kwargs)
        return result.json()

    except Exception as e:
        raise Exception(f"Error querying events: {e}")
