from houndcore.api.dependencies import DependsScanner
from houndcore.api.response import Json
from .router import router

@router.delete(
    "/unsubscribe/{sub_id}"
)
async def unsubscribe(
    scanner: DependsScanner,
    sub_id: str
) -> Json:
    '''unsubscribe
    
    Args:
      sub_id (str): the subscription id
    Returns:
      Json'''
    await scanner.unsubscribe(
        sub_id=sub_id
    )
    return Json(
        {
            "ok": True,
            "message": "Unsubscribed Successfully",
            "result": True
        }
    )