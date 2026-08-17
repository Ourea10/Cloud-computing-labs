from dataclasses import dataclass

from experiments.ch09_specialized_mechanisms.models import (
    PricingRule,
    UsageEvent,
)


@dataclass(frozen=True)
class UsageCharge:

    tenant_id: str
    resource_id: str
    quantity: float
    unit: str
    price_per_unit: float
    total_cost: float


class PayPerUseMonitor:

    def __init__(self):

        self.pricing: dict[
            str,
            PricingRule,
        ] = {}

        self.usage_events: list[
            UsageEvent
        ] = []

        self.charges: list[
            UsageCharge
        ] = []

    def register_price(
        self,
        rule: PricingRule,
    ) -> None:

        self.pricing[
            rule.resource_type
        ] = rule

    def record_usage(
        self,
        event: UsageEvent,
    ) -> UsageCharge:

        self.usage_events.append(event)

        rule = self.pricing.get(
            event.resource_type
        )

        if rule is None:
            raise KeyError(
                "No pricing rule registered"
            )

        cost = (
            event.quantity
            * rule.price_per_unit
        )

        charge = UsageCharge(
            tenant_id=event.tenant_id,
            resource_id=event.resource_id,
            quantity=event.quantity,
            unit=event.unit,
            price_per_unit=rule.price_per_unit,
            total_cost=cost,
        )

        self.charges.append(charge)

        return charge

    def tenant_total(
        self,
        tenant_id: str,
    ) -> float:

        return sum(
            charge.total_cost
            for charge in self.charges
            if charge.tenant_id
            == tenant_id
        )