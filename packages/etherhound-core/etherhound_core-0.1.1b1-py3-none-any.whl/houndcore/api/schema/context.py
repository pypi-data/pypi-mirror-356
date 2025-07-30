from pydantic import BaseModel
from typing import Union, Self, Any

class PendingTransaction(BaseModel):
    address: str
    gas: int
    gas_price: int
    max_fee_per_gas: int
    max_priority_fee_per_gas: int
    hash: str
    input: str
    nonce: int
    to: str
    value: int
    type: int
    access_list: list[str]
    chain_id: int
    v: int
    r: str
    s: str
    y_parity: str
    transaction_index: Union[int, None] = None
    block_hash: Union[str, None] = None
    block_number: Union[int, None] = None

    @classmethod
    def from_web3(
        cls,
        data: dict[str, Any]
    ) -> Self:
        return PendingTransaction(
            address=data["from"],
            gas=data["gas"],
            gas_price=data["gasPrice"],
            max_fee_per_gas=data.get("maxFeePerGas", 0),
            max_priority_fee_per_gas=data.get("maxPriorityFeePerGas", 0),
            hash=f'0x{data["hash"].hex()}',
            input=f'0x{data["input"].hex()}',
            nonce=data["nonce"],
            to=data.get("to", ""),
            transaction_index=data.get("transactionIndex", 0),
            value=data["value"],
            type=data.get("type", 0),
            access_list=[item.hex() for item in data.get("accessList", [])],
            chain_id=data.get("chainId", 0),
            v=data["v"],
            r=f'0x{data["r"].hex()}',
            s=f'0x{data["s"].hex()}',
            y_parity=str(data.get("yParity", "")),
            block_hash=f'0x{data.get("blockHash").hex()}' if hasattr(data.get("blockHash"), "hex") else data.get("blockHash"),
            block_number=data.get("blockNumber", None)
        )

class LogsTransaction(BaseModel):
    address: str
    topics: list[str]
    data: str
    transaction_index: int
    transaction_hash: str
    log_index: int
    removed: bool
    block_hash: str
    block_number: int

    @classmethod
    def from_web3(
        cls,
        data: dict[str, Any]
    ) -> Self:
        return LogsTransaction(
            address=data["address"],
            topics=[f"0x{topic.hex()}" for topic in data["topics"]],
            data=data["data"].hex(),
            transaction_index=data["transactionIndex"],
            transaction_hash=f'0x{data["transactionHash"].hex()}',
            log_index=data["logIndex"],
            removed=data["removed"],
            block_hash=f'0x{data.get("blockHash").hex()}' if hasattr(data.get("blockHash"), "hex") else data.get("blockHash"),
            block_number=data.get("blockNumber", None)
        )

class Context(BaseModel):
    '''the returned context from /api/poll
    
    Args:
      label (str): the subscription label
      result (Union[PendingTransaction, Union[LogsTransaction, str]]): the event'''
    label: str
    result: Union[
        PendingTransaction, Union[
            LogsTransaction, str
        ]
    ]