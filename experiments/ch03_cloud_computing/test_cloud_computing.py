from .scaling import AutoScaler, ScalingPolicy
from .workload import Workload


def test_high_utilization_scales_out():
    scaler = AutoScaler(
        ScalingPolicy()
    )

    decision = scaler.decide(
        utilization=90,
        instance_count=2,
    )

    assert decision == "scale_out"


def test_low_utilization_scales_in():
    scaler = AutoScaler(
        ScalingPolicy()
    )

    decision = scaler.decide(
        utilization=10,
        instance_count=2,
    )

    assert decision == "scale_in"


def test_workload_demand():
    workload = Workload(
        name="api",
        cpu_demand=50,
        memory_demand=30,
    )

    assert workload.total_demand == 80
