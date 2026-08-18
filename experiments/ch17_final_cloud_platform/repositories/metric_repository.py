class MetricRepository:

    def __init__(self):

        self.metrics = []

    def save(self, metric):

        self.metrics.append(
            metric
        )

    def list_by_resource(
        self,
        resource_id,
    ):

        return [
            metric
            for metric
            in self.metrics
            if metric.resource_id
            == resource_id
        ]