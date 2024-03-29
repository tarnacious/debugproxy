from multiprocessing import Process
from logging.config import fileConfig
from mitmproxy.tools import cmdline
import logging
import concurrent_log_handler
fileConfig('config/logging.ini')
logger = logging.getLogger(__name__)
logging.getLogger("passlib").setLevel(logging.WARNING)
logging.getLogger("hpack").setLevel(logging.WARNING)

def proxyserver() -> None:
    from proxyserver.master import Master
    from mitmproxy.tools.main import run
    run(Master, cmdline.mitmproxy, None)

def proxyworker() -> None:
    from proxyworker.worker import worker
    worker()

def proxywebsocket() -> None:
    from proxywebsocket.main import main
    main()

# Generates a certificate with "debugproxy" as the organization and commona name
# in the default location mitmproxy expects it. The ~/.mitmproxy directory must
# be removed manually for this command to work.
def generate_certificates():
    import os
    p = os.path.expanduser('~/.mitmproxy')
    # This needs to be more specific, as we want to generate using an existing
    # dh_params.pem file
    #
    #if os.path.exists(p):
    #    print("Certificate directory,", p, ", already exists");
    #    print("Exiting.");
    #    return

    from mitmproxy.certs import CertStore
    print("Writing certificates to ", p);
    CertStore.create_store(p, "mitmproxy", 2048, organization="debugproxy", cn="debugproxy")
    print("Exiting.");
