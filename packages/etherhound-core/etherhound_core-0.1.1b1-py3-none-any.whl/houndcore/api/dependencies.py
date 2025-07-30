from fastapi import Depends
from typing import Annotated
from logging import Logger
from houndcore.app.scanners import Scanner, SubscriptionScanner
from houndcore.logger import get_logger
from houndcore.config import Config

config = Config.from_env()
scanner: Scanner = None

async def get_scanner() -> SubscriptionScanner:
    global scanner

    if not scanner:
        
        if config.MODE == "fast":
            scanner = SubscriptionScanner(config=config)
    
    if not await scanner.is_connected:
        await scanner.connect()

    return scanner

DependsScanner = Annotated[Scanner, Depends(get_scanner)]
DependsLogger = Annotated[Logger, Depends(get_logger)]