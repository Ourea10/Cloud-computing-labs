from dataclasses import dataclass

from ..exceptions import (
    DeliveryModelError,
)


@dataclass
class DeliveryModel:

    name: str
    compute: str
    networking: str
    operating_system: str
    runtime: str
    application: str


class DeliveryService:

    MODELS = {

        "on_premises": DeliveryModel(
            name="On-Premises",
            compute="Customer",
            networking="Customer",
            operating_system="Customer",
            runtime="Customer",
            application="Customer",
        ),

        "iaas": DeliveryModel(
            name="IaaS",
            compute="Customer",
            networking="Shared",
            operating_system="Customer",
            runtime="Customer",
            application="Customer",
        ),

        "paas": DeliveryModel(
            name="PaaS",
            compute="Provider",
            networking="Provider",
            operating_system="Provider",
            runtime="Provider",
            application="Customer",
        ),

        "serverless": DeliveryModel(
            name="Serverless",
            compute="Provider",
            networking="Provider",
            operating_system="Provider",
            runtime="Provider",
            application="Customer",
        ),
    }

    def get_model(
        self,
        model_name: str,
    ):

        model = self.MODELS.get(
            model_name
        )

        if model is None:
            raise DeliveryModelError(
                f"Unknown delivery model: "
                f"{model_name}"
            )

        return model

    def compare(
        self,
        first: str,
        second: str,
    ):

        first_model = self.get_model(
            first
        )

        second_model = self.get_model(
            second
        )

        return {
            "first": first_model,
            "second": second_model,
        }

    def recommend(
        self,
        requirements: dict,
    ):

        if requirements.get(
            "minimal_operations"
        ):

            return self.get_model(
                "serverless"
            )

        if requirements.get(
            "maximum_control"
        ):

            return self.get_model(
                "iaas"
            )

        return self.get_model(
            "paas"
        )