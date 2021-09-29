from pydantic import BaseSettings



class Config(BaseSettings):
    # group_id= 464747480
    group_id=464747480
    
    class Config:
        extra = "ignore"