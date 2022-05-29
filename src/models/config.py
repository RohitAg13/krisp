from typing import Optional

from pydantic import BaseSettings


class ModelSetting(BaseSettings):
    hugging_face_api_key: Optional[str] = None

    class Config:
        env_file = ".env"
