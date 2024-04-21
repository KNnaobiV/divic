import asyncio
import configparser
import ssl

from task_manager.utils import get_logger

logger = get_logger(name="server", loglevel="INFO")

cfg = configparser.ConfigParser()
cfg.read("server.cfg")
host = cfg.get("app", "host", fallback=None)
port = cfg.get("app", "port", fallback=None)

CA_FILE = cfg.get("auth", "cafile", fallback="")
CERT_FILE = cfg.get("auth", "certfile", fallback="")
CERT_KEY = cfg.get("auth", "certkey", fallback="")

def get_context():
    """
    Creates an SSL context object to wrap communication in TLS.

    :return SSLContext: an SSL context object which wraps the communication 
        in TLS
    :raise FileNotFoundError: when CERT_FILE, CERT_KEY OR CA_FILE is not 
        found. 
    """
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=CERT_KEY)
    context.load_verify_locations(cafile=CA_FILE)
    context.check_hostname = False
    context.minimum_version = ssl.TLSVersion.TLSv1
    return context


async def my_server(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    logger.info(f"Received {message!r} from {addr!r}")

    logger.info(f"Send: {message!r}")
    writer.write(data)
    await writer.drain()

    logger.info("Closing the connection")
    writer.close()

async def run_server():
    context = get_context()
    server = await asyncio.start_server(my_server, host, port, ssl=context)
    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets())
    logger.info(f"Serving on {addrs}")
    async with server:
        await server.serve_forever()