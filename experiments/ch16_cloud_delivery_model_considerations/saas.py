from dataclasses import dataclass


@dataclass
class SaaSSubscription:

    subscription_id: str
    customer_id: str
    service_name: str
    active: bool = True


class SaaSProvider:

    def __init__(self):

        self.subscriptions: dict[
            str,
            SaaSSubscription,
        ] = {}

    def subscribe(
        self,
        subscription_id: str,
        customer_id: str,
        service_name: str,
    ):

        subscription = SaaSSubscription(
            subscription_id=subscription_id,
            customer_id=customer_id,
            service_name=service_name,
        )

        self.subscriptions[
            subscription_id
        ] = subscription

        return subscription

    def cancel(
        self,
        subscription_id: str,
    ):

        subscription = (
            self.subscriptions[
                subscription_id
            ]
        )

        subscription.active = False