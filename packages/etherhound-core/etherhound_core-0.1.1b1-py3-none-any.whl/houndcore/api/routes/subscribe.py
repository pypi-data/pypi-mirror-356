from houndcore.api.dependencies import DependsScanner, DependsLogger
from houndcore.api.schema.subscription import SupportedSubscription
from houndcore.app.types.subscription import Subscription
from houndcore.api.response import Json
from typing import Union, List
from .router import router
import asyncio

@router.post(
    "/subscribe"
)
async def subscribe(
    scanner: DependsScanner,
    logger: DependsLogger,
    subscriptions: Union[
        SupportedSubscription,
        List[SupportedSubscription]
    ]
) -> Json:
    '''subscribe to specified subscriptions
    
    Args:
      subscriptions (Union[SupportedSubscription, List[SupportedSubscription]]): the subscriptions
    Returns:
      Json response with subscription ids in the result'''
    try:
        if not isinstance(subscriptions, list): subscriptions = [subscriptions]
        subscriptions = [
            Subscription(
                type=sub.type,
                **sub.model_dump()
            ) for sub in subscriptions
        ]
        sub_ids = await scanner.subscribe(subscriptions)
        if not scanner.is_running:
            asyncio.create_task(scanner.run())
        return Json(
            {
                "ok": True,
                "message": None,
                "result": sub_ids
            }
        )
    except Exception as e:
        logger.info(f"{scanner.__class__.__name__}: Subscription Failed ({e}) 🔴")
        return Json(
            {
                "ok": False,
                "message": "Cannot Subscribe, an issue has occurred",
                "result": None
            },
            status_code=500
        )