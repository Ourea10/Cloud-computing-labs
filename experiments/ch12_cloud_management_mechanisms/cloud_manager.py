from datetime import datetime, timezone

from .billing import (
    BillingManagementSystem,
)

from .models import (
    PricingRule,
    ResourceQuota,
    ResourceType,
    SLAPolicy,
    UsageRecord,
)

from .remote_administration import (
    RemoteAdministrationSystem,
)

from .resource_management import (
    ResourceManagementSystem,
)

from .sla_management import (
    SLAManagementSystem,
)


class CloudManager:

    def __init__(self):

        self.resource_manager = (
            ResourceManagementSystem()
        )

        self.admin = (
            RemoteAdministrationSystem(
                self.resource_manager.resources
            )
        )

        self.sla_manager = (
            SLAManagementSystem()
        )

        self.billing = (
            BillingManagementSystem()
        )

    def configure_quota(
        self,
        quota: ResourceQuota,
    ) -> None:

        self.resource_manager.set_quota(
            quota
        )

    def create_vm(
        self,
        owner_id: str,
        name: str,
        cpu: int,
        memory_gb: int,
        storage_gb: int,
    ):

        resource = (
            self.resource_manager.create_resource(
                owner_id=owner_id,
                resource_type=ResourceType.VM,
                name=name,
                cpu=cpu,
                memory_gb=memory_gb,
                storage_gb=storage_gb,
            )
        )

        self.admin.start(
            resource.resource_id
        )

        return resource

    def create_sla(
        self,
        policy: SLAPolicy,
    ):

        return self.sla_manager.create_policy(
            policy
        )

    def record_usage(
        self,
        resource_id: str,
        owner_id: str,
        resource_type: ResourceType,
        quantity: float,
        unit: str,
    ):

        self.billing.record_usage(
            UsageRecord(
                resource_id=resource_id,
                owner_id=owner_id,
                resource_type=resource_type,
                quantity=quantity,
                unit=unit,
                timestamp=datetime.now(
                    timezone.utc
                ),
            )
        )

    def add_pricing_rule(
        self,
        rule: PricingRule,
    ) -> None:
        self.billing.add_pricing_rule(rule)

    def generate_invoice(
        self,
        customer_id: str,
        period: str,
    ):

        return self.billing.generate_invoice(
            customer_id=customer_id,
            period=period,
        )
