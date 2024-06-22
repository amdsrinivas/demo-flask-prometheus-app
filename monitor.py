import time

import google.protobuf.duration_pb2
from google.cloud import monitoring_v3

client = monitoring_v3.MetricServiceClient()

project_name = "projects/firm-capsule-426913-g7"

now = time.time()
seconds = int(now)
nanos = int((now - seconds) * 10 ** 9)
interval = monitoring_v3.TimeInterval(
    {
        "end_time": {"seconds": seconds, "nanos": nanos},
        "start_time": {"seconds": (seconds - 300), "nanos": nanos}
    }
)

'''
AND resource.type="k8s_container" '
                  'AND resource.labels.container_name="demo-flask-prom"
'''

# aggregation = monitoring_v3.Aggregation(
#     {
#         "alignment_period": {"seconds": 60},
#         "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_NEXT_OLDER,
#         "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_PERCENTILE_05,
#         "group_by_fields": ['resource.location', 'resource.pod_name'],
#
#         # "secondary_aggregation": monitoring_v3.Aggregation(
#         #     {
#         #         "group_by_fields": ['resource.location', 'resource.pod_name'],
#         #         "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_SUM,
#         #     }
#         #
#         # )
#     }
#
# )

used_bytes = client.list_time_series(
    request={
        "name": project_name,
        "filter": 'metric.type = "kubernetes.io/container/memory/used_bytes" AND resource.labels.container_name="demo-flask-prom"',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        #"aggregation": aggregation
    }
)

requested_bytes = client.list_time_series(
    request={
        "name": project_name,
        "filter": 'metric.type = "kubernetes.io/container/memory/request_bytes" AND resource.labels.container_name="demo-flask-prom"',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }
)
print("memory usage(timestamp, used_bytes, requested_bytes, percentage)")
for used_bytes_page, requested_bytes_page in zip(used_bytes.pages, requested_bytes.pages):
    used_series = used_bytes_page.time_series
    requested_series = requested_bytes_page.time_series

    for point_pair in zip(used_series[0].points, requested_series[0].points):
        timestamp = point_pair[0].interval.end_time
        usedBytes = point_pair[0].value.int64_value
        requestedBytes = point_pair[1].value.int64_value
        print(timestamp, usedBytes, requestedBytes, usedBytes / requestedBytes)

used_cpu = client.list_time_series(
    request={
        "name": project_name,
        "filter": 'metric.type = "kubernetes.io/container/cpu/core_usage_time" AND resource.labels.container_name="demo-flask-prom"',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }
)

requested_cpu = client.list_time_series(
    request={
        "name": project_name,
        "filter": 'metric.type = "kubernetes.io/container/cpu/request_cores" AND resource.labels.container_name="demo-flask-prom"',
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }
)

print("cpu usage(timestamp, core_usage_time, requested_cores)")
for used_cpu_page, requested_cpu_page in zip(used_cpu.pages, requested_cpu.pages):
    used_series = used_cpu_page.time_series
    requested_series = requested_cpu_page.time_series

    for point_pair in zip(used_series[0].points, requested_series[0].points):
        timestamp = point_pair[0].interval.end_time
        usedCpu = point_pair[0].value.double_value
        requestedCpu = point_pair[1].value.double_value
        print(timestamp, usedCpu, requestedCpu)
