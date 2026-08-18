from pydantic import BaseModel


class DirectIORequest(BaseModel):

    resource_id: str
    lun_id: str
    client_id: str


class EdgeProcessRequest(BaseModel):

    node_id: str
    data: dict


class MaintenanceRequest(BaseModel):

    resource_id: str
    start: str
    end: str
    reason: str


class MultipathRequest(BaseModel):

    source_id: str
    target_id: str