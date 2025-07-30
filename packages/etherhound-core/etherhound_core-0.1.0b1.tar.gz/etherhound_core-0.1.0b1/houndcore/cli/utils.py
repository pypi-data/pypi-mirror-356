from houndcore.config import Config
import os, sys, subprocess

def run_server(
    host: str,
    port: int,
    config: Config,
    detach: bool,
):
    '''
    Run the EtherHound Core FastAPI server.

    Args:
        host (str): Host to bind to.
        port (int): Port to run on.
        config (:class:`houndcore.config.Config`): the Configuration
    '''

    if not os.path.isfile(".env"):
        with open(".env", "w+") as config_file:
            config_file.write(
                "\n".join([
                    f"{k}={v}" for k,v in config.model_dump().items()
                ])
            )

    command = [
        sys.executable, "-m", "uvicorn",
        "houndcore.api.app:app",
        "--host", host,
        "--port", str(port)
    ]
    print("Running Server...")

    if detach:
        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
        )
    else:
        subprocess.run(command, check=True)