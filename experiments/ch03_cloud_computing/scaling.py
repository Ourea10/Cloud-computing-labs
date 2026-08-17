from dataclasses import dataclass


@dataclass
class ScalingPolicy:
    scale_out_threshold: float = 70.0
    scale_in_threshold: float = 30.0
    min_instances: int = 1
    max_instances: int = 10


class AutoScaler:
    def __init__(
        self,
        policy: ScalingPolicy,
    ):
        self.policy = policy

    def decide(
        self,
        utilization: float,
        instance_count: int,
    ) -> str:

        if (
            utilization >= self.policy.scale_out_threshold
            and instance_count < self.policy.max_instances
        ):
            return "scale_out"

        if (
            utilization <= self.policy.scale_in_threshold
            and instance_count > self.policy.min_instances
        ):
            return "scale_in"

        return "keep"