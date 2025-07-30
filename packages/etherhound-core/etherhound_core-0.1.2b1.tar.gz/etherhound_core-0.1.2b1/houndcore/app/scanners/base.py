from houndcore.config import Config
from houndcore.app.types import Subscription
from houndcore.app.dispatcher import Dispatcher
from typing import Union, List

class Scanner:
    '''The Base class for Scanners'''

    def __init__(
        self,
        config: Config,
        dispatcher: Dispatcher
    ):
        self.config = Config
        self.dispatcher = dispatcher

    @property
    async def is_connected(self) -> bool:
        raise NotImplementedError

    async def connect(
        self
    ) -> None:
        raise NotImplementedError
    
    async def subscribe(
        self,
        subs: Union[List[Subscription], Subscription]
    ) -> None:
        raise NotImplementedError

    async def unsubscribe(
        self,
        sub_id: str
    ) -> None:
        raise NotImplementedError
    
    async def run(
        self
    ) -> None:
        raise NotImplementedError