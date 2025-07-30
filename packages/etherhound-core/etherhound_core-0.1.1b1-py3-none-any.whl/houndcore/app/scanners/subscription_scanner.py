from web3 import AsyncWeb3, WebSocketProvider
from typing import List, Union
from houndcore.app.types import Subscription
from houndcore.config import Config
from houndcore.app.scanners.base import Scanner
from houndcore.app.dispatcher import Dispatcher
from houndcore.app.errors.incorrect_rpc import IncorrectRPC

class SubscriptionScanner(Scanner):
    '''a Fast Subscription-Based Scanner that uses `eth_subscribe` to monitor events
    (**MAY NOT COVER SOME USE CASES**)
    
    Args:
      config (:class:`houndcore.config.Config`): the config'''

    def __init__(
        self,
        config: Config,
        dispatcher: Dispatcher | None = None
    ):
        if not config.RPC.startswith("ws"):
            raise IncorrectRPC(
                scanner=SubscriptionScanner,
                rpc=config.RPC
            )

        self.w3: AsyncWeb3 = AsyncWeb3(WebSocketProvider(
            endpoint_uri=config.RPC
        ))
        self.dispatcher = dispatcher or Dispatcher()
        self.is_running: bool = False

    @property
    async def is_connected(self) -> bool:
        return await self.w3.provider.is_connected()

    async def connect(self) -> None:
        '''connects the WebSocketProvider, if not connected'''
        if await self.is_connected:
            return
        await self.w3.provider.connect()
    
    async def subscribe(
        self,
        subs: Union[List[Subscription], Subscription],
    ) -> List[str]:
        '''subscribes to events
        
        Args:
          subs (Union[List[Subscription], Subscription]): The subscriptions
        Returns:
          HexStr'''
        subscriptions = []

        if isinstance(subs, Subscription):
            subs = [subs]

        for sub in subs:

            if not sub.handler:
                sub.handler = self.dispatcher.handle_event

            sub_id = await self.w3.subscription_manager.subscribe(sub.to_web3())
            subscriptions.append(sub_id)
            self.dispatcher.subscribe(
                sub_id=sub_id
            )
        return subscriptions
    
    async def unsubscribe(
        self,
        sub_id: str
    ) -> None:
        '''unsubscribe from web3 and dispatcher
        
        Args:
          sub_id (str): Subscription ID
        Returns:
          None'''
        try:
            await self.w3.subscription_manager.unsubscribe(
                sub_id
            )
            self.dispatcher.unsubscribe(sub_id=sub_id)
        except Exception as e:
            print(e)
    
    async def run(self) -> None:
        '''running the handlers'''
        if self.is_running: return
        self.is_running = True
        await self.w3.subscription_manager.handle_subscriptions()