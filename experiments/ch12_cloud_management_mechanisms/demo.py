from .cloud_manager import CloudManager
from .models import (
    PricingRule,
    ResourceQuota,
    ResourceType,
    SLAPolicy,
)


def main():

    print(
        "=== Chapter 12 ==="
    )

    manager = CloudManager()

    manager.add_pricing_rule(
        PricingRule(
            resource_type=ResourceType.VM,
            unit="cpu_hour",
            price_per_unit=0.05,
        )
    )

    manager.add_pricing_rule(
        PricingRule(
            resource_type=ResourceType.VM,
            unit="memory_gb_hour",
            price_per_unit=0.01,
        )
    )

    # --------------------------------
    # 1. Configure quota
    # --------------------------------

    manager.configure_quota(
        ResourceQuota(
            owner_id="alice",
            max_cpu=16,
            max_memory_gb=32,
            max_storage_gb=500,
        )
    )

    print(
        "\n[1] Quota configured"
    )

    # --------------------------------
    # 2. Create resource
    # --------------------------------

    vm = manager.create_vm(
        owner_id="alice",
        name="web-server",
        cpu=4,
        memory_gb=8,
        storage_gb=100,
    )

    print(
        "\n[2] VM created"
    )

    print(vm)

    # --------------------------------
    # 3. SLA
    # --------------------------------

    manager.create_sla(
        SLAPolicy(
            sla_id="sla-001",
            customer_id="alice",
            resource_id=vm.resource_id,
            availability_target=0.999,
            response_time_target_ms=300,
            monthly_price=100,
        )
    )

    print(
        "\n[3] SLA created"
    )

    # --------------------------------
    # 4. Record usage
    # --------------------------------

    manager.record_usage(
        resource_id=vm.resource_id,
        owner_id="alice",
        resource_type=ResourceType.VM,
        quantity=20,
        unit="cpu_hour",
    )

    manager.record_usage(
        resource_id=vm.resource_id,
        owner_id="alice",
        resource_type=ResourceType.VM,
        quantity=160,
        unit="memory_gb_hour",
    )

    print(
        "\n[4] Usage recorded"
    )

    # --------------------------------
    # 5. Billing
    # --------------------------------

    invoice = manager.generate_invoice(
        customer_id="alice",
        period="2026-08",
    )

    print(
        "\n[5] Invoice"
    )

    for item in invoice.items:

        print(
            f"{item.description}: "
            f"{item.quantity} × "
            f"{item.unit_price} = "
            f"{item.amount}"
        )

    print(
        f"\nTotal: ${invoice.total:.2f}"
    )


if __name__ == "__main__":
    main()
