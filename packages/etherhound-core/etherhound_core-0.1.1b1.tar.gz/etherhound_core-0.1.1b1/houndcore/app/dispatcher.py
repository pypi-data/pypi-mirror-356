from houndcore.app.types.context import Context
from typing import List, Dict, Union

class Dispatcher:
    '''the event manager (dispatcher)'''
    
    def __init__(
        self,
    ):
        self.events: Dict[str, List[Context]] = {} # sub_id:events
        self.listeners: Dict[str, int] = {} # sub_id:index
    
    def subscribe(
        self,
        sub_id: str
    ) -> None:
        '''Subscribe to a subscription using its id
        
        Args:
          sub_id (str): the subscription id'''
        if self.listeners.get(sub_id, None) is None:
            self.listeners[sub_id] = 0
        
        self.listeners[sub_id] = 0
    
    def unsubscribe(
        self,
        sub_id: str
    ) -> None:
        '''Un-Subscribe to a subscription using its id
        
        Args:
          sub_id (str): the subscription id'''
        if self.listeners.get(sub_id, None) is None:
            return
        
        self.listeners.pop(sub_id)
    
    async def handle_event(
        self,
        context: Context
    ) -> None:
        '''handles any new events
        
        Args:
          context (Union[web3.utils.PendingTxSubscriptionContext, web3.utils.LogsSubscriptionContext]): the event context'''
        sub_id = context.subscription.id
        if sub_id not in self.events:
            self.events[sub_id] = []
        
        self.events[sub_id].append(context)
    
    def poll(
        self,
        sub_id: str,
        limit: int
    ) -> Union[List[Context], None]:
        '''poll any new events using the subscription id
        
        Args:
          sub_id (str): the subscription id
          limit (int): the limit of returned results
        Return:
          Union[List[Context], None]'''
        if (index := self.listeners.get(sub_id, None)) is None:
            return
        
        data = []
        events = self.events.get(sub_id, [])

        try:
            events_index = len(events)
            new_events = events[index : min(events_index, index + limit)]
            self.listeners[sub_id] = index + len(new_events)
        except IndexError:
            new_events = []

        data.extend(new_events)
        return data