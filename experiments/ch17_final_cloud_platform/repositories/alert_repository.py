class AlertRepository:

    def __init__(self):

        self.alerts = {}

    def create(self, alert):

        self.alerts[
            alert.id
        ] = alert

        return alert

    def list_by_resource(
        self,
        resource_id,
    ):

        return [
            alert
            for alert
            in self.alerts.values()
            if alert.resource_id
            == resource_id
        ]