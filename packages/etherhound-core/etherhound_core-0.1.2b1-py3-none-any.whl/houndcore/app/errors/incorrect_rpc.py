from houndcore.app.scanners.base import Scanner

class IncorrectRPC(Exception):
    '''raised when the RPC type doesn't match the Scanner needed RPC
    
    Args:
      scanner (:class:`houndcore.app.scanners.base.Scanner`): the Scanner
      rpc (str): the rpc'''

    def __init__(
        self,
        scanner: Scanner,
        rpc: str,
    ):
        self.rpc_type = "WebSocket" if rpc.startswith("ws") else "HTTP"
        self.rpc = rpc
        self.scanner = scanner
        self.message = f"Scanner {self.scanner.__name__} Needs {'WebSocket' if self.rpc_type=='HTTP' else 'HTTP'} RPC not {self.rpc_type}"
        super().__init__(self.message)