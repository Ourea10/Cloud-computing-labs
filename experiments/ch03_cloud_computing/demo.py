from .scaling import AutoScaler, ScalingPolicy
from .risk import CloudRisk, Severity
from .workload import Workload


def run_scaling_demo():
    policy = ScalingPolicy(
        scale_out_threshold=70,
        scale_in_threshold=30,
        min_instances=1,
        max_instances=5,
    )

    scaler = AutoScaler(policy)

    scenarios = [
        (20, 2),
        (50, 2),
        (85, 2),
        (90, 3),
        (20, 3),
    ]

    print("=== Scaling Simulation ===")

    for utilization, instances in scenarios:
        decision = scaler.decide(
            utilization,
            instances,
        )

        print(
            f"utilization={utilization}% "
            f"instances={instances} "
            f"decision={decision}"
        )


def run_workload_demo():
    workload = Workload(
        name="checkout-service",
        cpu_demand=60,
        memory_demand=20,
    )

    print("\n=== Workload ===")
    print(f"name={workload.name}")
    print(f"demand={workload.total_demand}")


def run_risk_demo():
    risks = [
        CloudRisk(
            name="Vendor lock-in",
            severity=Severity.HIGH,
            mitigation="Use provider-independent interfaces.",
        ),
        CloudRisk(
            name="Cost overrun",
            severity=Severity.HIGH,
            mitigation="Monitor usage and enforce budgets.",
        ),
    ]

    print("\n=== Risks ===")

    for risk in risks:
        print(
            f"{risk.name}: "
            f"{risk.severity.value} - "
            f"{risk.mitigation}"
        )


def main():
    run_scaling_demo()
    run_workload_demo()
    run_risk_demo()


if __name__ == "__main__":
    main()
