"""SSL compatibility fix for macOS LibreSSL.

macOS LibreSSL 2.8.3 cannot negotiate TLS 1.3 with Fastly/Cloudflare CDNs.
This forces TLS 1.2 which works universally.

Import before any other network code:
    import _ssl_compat  # noqa
"""

import ssl

if 'LibreSSL' in ssl.OPENSSL_VERSION:
    try:
        # Restrict to TLS 1.2 — the max LibreSSL 2.8 reliably supports
        _ctx = ssl.create_default_context()
        _ctx.maximum_version = ssl.TLSVersion.TLSv1_2
        ssl._create_default_https_context = lambda: _ctx
    except Exception:
        pass  # Non-macOS or newer LibreSSL: keep defaults
