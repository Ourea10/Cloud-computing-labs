class DeliveryModelError(Exception):
    pass


class UnsupportedWorkloadError(
    DeliveryModelError
):
    pass


class InvalidResponsibilityError(
    DeliveryModelError
):
    pass