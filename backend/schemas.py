from pydantic import BaseModel


class ImageResponse(BaseModel):

    filename: str
    nsfw: float
    violence: float
    status: str
