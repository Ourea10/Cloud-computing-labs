from dataclasses import dataclass, field


@dataclass
class HardenedImage:
    image_id: str
    base_image: str
    disabled_services: set[str] = field(
        default_factory=set
    )
    security_patches: set[str] = field(
        default_factory=set
    )
    open_ports: set[int] = field(
        default_factory=set
    )


class HardenedImageBuilder:

    def build(
        self,
        image_id: str,
        base_image: str,
    ) -> HardenedImage:

        return HardenedImage(
            image_id=image_id,
            base_image=base_image,
            disabled_services={
                "telnet",
                "ftp",
            },
            security_patches={
                "latest-security-patch",
            },
            open_ports={
                22,
                443,
            },
        )