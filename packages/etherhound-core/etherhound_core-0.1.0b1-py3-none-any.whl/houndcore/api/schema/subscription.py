from pydantic import BaseModel
from typing import Union, Optional, List

# Base
class SubscriptionBase(BaseModel):
    label: Optional[str]

    @property
    def type(self) -> str:
        raise NotImplementedError

# Logs
class LogsSubscription(SubscriptionBase):
    address: Union[str, List[str]]
    topics: Optional[List[str]]

    @property
    def type(self) -> str: return "logs"

# PendingTransactions
class PendingTransactionsSubscription(SubscriptionBase):
    full_transactions: bool = False

    @property
    def type(self) -> str: return "pending"

SupportedSubscription = Union[
    LogsSubscription, PendingTransactionsSubscription
]