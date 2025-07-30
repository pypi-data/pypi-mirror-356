from web3.utils.subscriptions import (
    LogsSubscription,
    PendingTxSubscription
)
from typing import Literal, Callable

class Subscription:
    '''Subscription, Includes all supported Subscription Types
    
    Args:
      label (str): the subscription label
      type (Literal["logs", "pending"], *optional*, def="logs"): the subscription type
      handler (Callable, *optional*): the function to handle the events
      address (Union[str, List[str]], *optional*): the address/s to track (Only for Logs)
      topics (list[str], *optional*): the events signatures to track (Only For Logs)
      full_transactions (bool, *optional*, def=False): wether to return FullTransaction details or not (Only For Pending)'''

    def __init__(
        self,
        label: str | None = None,
        address: str | list[str] | None = None,
        topics: list[str] | None = None,
        handler: Callable | None = None,
        full_transactions: bool = False,
        type: Literal["logs", "pending"] = "logs"
    ):
        self.label = label
        self.address = address
        self.topics = topics
        self.type = type
        self.handler = handler
        self.full_transactions = full_transactions
    
    def to_web3(
        self
    ) -> LogsSubscription | PendingTxSubscription | None:
        
        if self.type == "logs":
            return LogsSubscription(
                label=self.label,
                address=self.address,
                topics=self.topics,
                handler=self.handler
            )
        
        elif self.type == "pending":
            return PendingTxSubscription(
                label=self.label,
                full_transactions=self.full_transactions,
                handler=self.handler
            )