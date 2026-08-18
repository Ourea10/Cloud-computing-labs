from datetime import datetime

from .exceptions import BillingError

from .models import (
    Invoice,
    InvoiceItem,
    PricingRule,
    ResourceType,
    UsageRecord,
)


class BillingManagementSystem:

    def __init__(self):

        self.pricing: dict[
            tuple[ResourceType, str],
            PricingRule,
        ] = {}

        self.usage: list[
            UsageRecord
        ] = []

    def add_pricing_rule(
        self,
        rule: PricingRule,
    ) -> None:

        self.pricing[
            (
                rule.resource_type,
                rule.unit,
            )
        ] = rule

    def record_usage(
        self,
        record: UsageRecord,
    ) -> None:

        self.usage.append(record)

    def calculate_usage_cost(
        self,
        record: UsageRecord,
    ) -> float:

        rule = self.pricing.get(
            (
                record.resource_type,
                record.unit,
            )
        )

        if rule is None:

            raise BillingError(
                "No pricing rule found"
            )

        return (
            record.quantity
            * rule.price_per_unit
        )

    def generate_invoice(
        self,
        customer_id: str,
        period: str,
    ) -> Invoice:

        records = [
            record
            for record in self.usage
            if record.owner_id
            == customer_id
        ]

        items = []

        for record in records:

            amount = (
                self.calculate_usage_cost(
                    record
                )
            )

            items.append(
                InvoiceItem(
                    description=(
                        f"{record.resource_type.value}"
                        f" - {record.unit}"
                    ),
                    quantity=record.quantity,
                    unit_price=(
                        amount / record.quantity
                        if record.quantity
                        else 0
                    ),
                    amount=amount,
                )
            )

        total = sum(
            item.amount
            for item in items
        )

        return Invoice(
            invoice_id=f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            customer_id=customer_id,
            period=period,
            items=items,
            total=total,
        )