import json
from pathlib import Path

from .case_model import CloudCase, ResourceRequirement


def load_cases() -> dict[str, CloudCase]:
    path = Path(__file__).parent / "cases.json"

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    cases = {}

    for case_name, case_data in data.items():
        cases[case_name] = CloudCase(
            name=case_data["name"],
            resource_requirements=ResourceRequirement(
                cpu=case_data["resource_requirements"]["cpu"],
                memory=case_data["resource_requirements"]["memory"],
            ),
            desired_instances=case_data["desired_instances"],
            characteristics=case_data["characteristics"],
        )

    return cases
