from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any

from experiments.ch09_specialized_mechanisms.models import (
    Device,
    DeviceType,
)


@dataclass(frozen=True)
class BrokerMessage:

    source_device: str
    topic: str
    payload: dict[str, Any]


class MultiDeviceBroker:

    def __init__(self):

        self.devices: dict[
            str,
            Device,
        ] = {}

        self.subscriptions: dict[
            str,
            set[str],
        ] = defaultdict(set)

        self.queues: dict[
            str,
            deque[BrokerMessage],
        ] = defaultdict(deque)

    def register_device(
        self,
        device: Device,
    ) -> None:

        self.devices[
            device.device_id
        ] = device

    def unregister_device(
        self,
        device_id: str,
    ) -> None:

        self.devices.pop(
            device_id,
            None,
        )

        for subscribers in (
            self.subscriptions.values()
        ):
            subscribers.discard(
                device_id
            )

        self.queues.pop(
            device_id,
            None
        )

    def subscribe(
        self,
        device_id: str,
        topic: str,
    ) -> None:

        if device_id not in self.devices:
            raise KeyError(
                "Device is not registered"
            )

        self.subscriptions[
            topic
        ].add(device_id)

    def publish(
        self,
        message: BrokerMessage,
    ) -> int:

        subscribers = self.subscriptions.get(
            message.topic,
            set(),
        )

        for device_id in subscribers:

            self.queues[
                device_id
            ].append(message)

        return len(subscribers)

    def consume(
        self,
        device_id: str,
    ) -> BrokerMessage | None:

        queue = self.queues[
            device_id
        ]

        if not queue:
            return None

        return queue.popleft()