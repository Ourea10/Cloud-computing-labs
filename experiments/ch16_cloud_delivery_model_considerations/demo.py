import json
from pathlib import Path

from .delivery_service import (
    DeliveryService,
)

from .models import Workload


BASE_DIR = Path(__file__).parent


def load_workloads():

    path = (
        BASE_DIR
        / "scenarios"
        / "workloads.json"
    )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


def main():

    service = DeliveryService()

    data = load_workloads()

    for item in data["workloads"]:

        workload = Workload(
            workload_id=item[
                "workload_id"
            ],
            name=item["name"],
            requires_os_control=item[
                "requires_os_control"
            ],
            requires_runtime_control=item[
                "requires_runtime_control"
            ],
            requires_application_control=item[
                "requires_application_control"
            ],
            operational_complexity=item[
                "operational_complexity"
            ],
            scalability_requirement=item[
                "scalability_requirement"
            ],
            budget=item["budget"],
        )

        service.workloads.register(
            workload
        )

    print(
        "================================"
    )

    print(
        "CLOUD DELIVERY MODEL EVALUATION"
    )

    print(
        "================================"
    )

    for workload in (
        service.workloads.list()
    ):

        result = service.evaluate(
            workload.workload_id,
            workload_size=10,
        )

        print(
            f"\nWorkload: "
            f"{workload.name}"
        )

        print(
            f"Recommended model: "
            f"{result['delivery_model']}"
        )

        print(
            f"Score: "
            f"{result['score']}"
        )

        print(
            "Reasons:"
        )

        for reason in result[
            "reasons"
        ]:

            print(
                f"  - {reason}"
            )

        print(
            f"Estimated cost: "
            f"{result['cost']['total']}"
        )

        print(
            f"Risk: "
            f"{result['risk']['total']}"
        )

    print(
        "\n================================"
    )

    print(
        "IaaS RESPONSIBILITY"
    )

    print(
        "================================"
    )

    matrix = (
        service.responsibility.matrix(
            model=__import__(
                "experiments."
                "ch16_cloud_delivery_model_considerations."
                "enums",
                fromlist=["DeliveryModel"],
            ).DeliveryModel.IAAS
        )
    )

    for layer, owner in matrix.items():

        print(
            f"{layer:20} -> {owner}"
        )


if __name__ == "__main__":
    main()