class MetricsWorker:

    def __init__(
        self,
        queue,
        monitoring_service,
    ):

        self.queue = queue
        self.monitoring = (
            monitoring_service
        )

    def process_once(self):

        message = (
            self.queue.receive()
        )

        if message is None:

            return None

        metric = (
            self.monitoring.record(
                resource_id=message[
                    "resource_id"
                ],
                cpu_usage=message[
                    "cpu_usage"
                ],
                memory_usage=message[
                    "memory_usage"
                ],
            )
        )

        return metric