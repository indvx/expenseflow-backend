from pydantic import BaseModel


class MetaDataResponse(BaseModel):
    limit: int | None = None
    page: int | None = None
    total_items: int | None = None
    item: int | None = None
