from houndcore.config import Config
from typer import Typer, Option
from typing import Union
from houndcore.cli.utils import (
    run_server
)

app = Typer(
    name="HoundCore-CLI"
)

@app.command()
def deploy(
    host: str = Option("127.0.0.1", help="The server Host"),
    port: int = Option(8080, help="The Sever Port"),
    rpc: str = Option("null", help="the WebSocket RPC from your provider"),
    mode: str = Option("fast", help="The Hound Mode, read the docs for more info Union[fast, block (not yet supported)]"),
    detach: bool = Option(False, help="de-attach from the server"),
    load_env: bool = Option(False, help="load the rpc/mode/etc from the .env file"),
):
    if load_env:
        config = Config.from_env()
    else:
        if rpc == "null":
            return print("Please specify an RPC or use --load_env")

        config = Config(
            RPC=rpc,
            MODE=mode
        )
    
    run_server(
        host=host,
        port=port,
        config=config,
        detach=detach,
    )

if __name__ == "__main__":
    app()