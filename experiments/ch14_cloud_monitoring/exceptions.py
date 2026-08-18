class MonitoringError(Exception):
    """Base monitoring exception."""


class MetricNotFoundError(MonitoringError):
    pass


class InvalidMetricError(MonitoringError):
    pass


class AlertRuleNotFoundError(MonitoringError):
    pass


class UnsupportedOperatorError(MonitoringError):
    pass