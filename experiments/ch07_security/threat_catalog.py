import json
from pathlib import Path

from experiments.ch07_security.threat_models import (
    Threat,
    ThreatCategory,
)


def load_threat_catalog() -> dict[str, Threat]:
    path = Path(__file__).parent / "threat_catalog.json"

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    result = {}

    for name, item in data.items():
        result[name] = Threat(
            name=name,
            category=ThreatCategory(item["category"]),
            description=item["description"],
        )

    return result