from pydantic import BaseModel
from typing import Self, Literal
from dotenv import load_dotenv
from os import getenv

class Config(BaseModel):
    '''Config Class
    
    Args:
      RPC (str): WebSocket or HTTP RPC
      MODE (Literal["fast", "block"]): The Scanner Mode'''

    RPC: str
    MODE: Literal["fast", "block"]

    def from_env() -> Self:
      '''load local .env file and returns Config'''
      load_dotenv()
      return Config(
          RPC=getenv("RPC"),
          MODE=getenv("MODE", "fast")
      )