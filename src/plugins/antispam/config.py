from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    groups=[962767850]
    class Config:
        extra = "ignore"