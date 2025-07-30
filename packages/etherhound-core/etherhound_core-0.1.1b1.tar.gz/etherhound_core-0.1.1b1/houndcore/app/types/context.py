from web3.utils.subscriptions import (
    PendingTxSubscriptionContext,
    LogsSubscriptionContext
)
from typing import Union

Context = Union[
    LogsSubscriptionContext, PendingTxSubscriptionContext
]
'''The Handled Subscription Contexts'''