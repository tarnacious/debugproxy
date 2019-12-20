from mitmproxy.addons import anticache
from mitmproxy.addons import core
from mitmproxy.addons import anticomp
from mitmproxy.addons import check_ca
from mitmproxy.addons import clientplayback
from mitmproxy.addons import disable_h2c
from mitmproxy.addons import onboarding
from mitmproxy.addons import proxyauth
from mitmproxy.addons import replace
from mitmproxy.addons import readfile
from mitmproxy.addons import script
from mitmproxy.addons import serverplayback
from mitmproxy.addons import setheaders
from mitmproxy.addons import stickyauth
from mitmproxy.addons import stickycookie
from mitmproxy.addons import streambodies
from mitmproxy.addons import upstream_auth


def default_addons():
    return [
        core.Core(),
        anticache.AntiCache(),
        anticomp.AntiComp(),
        check_ca.CheckCA(),
        #clientplayback.ClientPlayback(),
        disable_h2c.DisableH2C(),
        #onboarding.Onboarding(),
        #proxyauth.ProxyAuth(),
        #replace.Replace(),
        #script.ScriptLoader(),
        #serverplayback.ServerPlayback(),
        #setheaders.SetHeaders(),
        #stickyauth.StickyAuth(),
        #stickycookie.StickyCookie(),
        #streambodies.StreamBodies(),
        #readfile.ReadFile(),
        #upstream_auth.UpstreamAuth(),
    ]
