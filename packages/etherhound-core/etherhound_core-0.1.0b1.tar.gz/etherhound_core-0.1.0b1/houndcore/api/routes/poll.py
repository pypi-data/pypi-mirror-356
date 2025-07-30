from houndcore.api.dependencies import DependsScanner
from houndcore.api.schema.context import Context, PendingTransaction, LogsTransaction
from houndcore.api.response import Json
from typing import List
from .router import router

@router.get(
    "/poll/{sub_id}"
)
async def poll(
    scanner: DependsScanner,
    sub_id: str,
    limit: int = 10
) -> List[Context]:
    '''poll any new updates
    
    Args:
      sub_id (str): the subscription_id returned from /api/subscribe
      limit (int, def=10): the limit of returned events
    Returns:
      List[Context]'''
    
    updates = scanner.dispatcher.poll(
        sub_id=sub_id,
        limit=limit
    )
    res = []

    if updates is None:
        return Json(
            content={
                "ok": False,
                "message": f"there are no subscription with ID={sub_id}",
                "result": None
            },
            status_code=404
        )

    # translate contexts
    for context in updates:
        if isinstance(context.result, bytes):
            tx = context.result.to_0x_hex()
        else:
            _type = context.subscription.subscription_params[0]
            if _type == "logs":
                tx = LogsTransaction.from_web3(context.result)
            elif _type == "newPendingTransactions":
                tx = PendingTransaction.from_web3(context.result)
            else:
                tx = f"0x{context.result.hex()}"
                
        res.append(
            Context(
                label=getattr(
                    context.subscription, "label", "pending"
                ),
                result=tx
            )
        )
    
    return res