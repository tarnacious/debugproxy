def flow_to_json(flow: mitmproxy.flow.Flow) -> dict:
    """
    Remove flow message content and cert to save transmission space.

    Args:
        flow: The original flow.
    """
    f = {
        "id": flow.id,
        "intercepted": flow.intercepted,
        "client_conn": flow.client_conn.get_state(),
        "server_conn": flow.server_conn.get_state(),
        "type": flow.type,
        "modified": flow.modified(),
        "marked": flow.marked,
    }
    # .alpn_proto_negotiated is bytes, we need to decode that.
    for conn in "client_conn", "server_conn":
        if f[conn]["alpn_proto_negotiated"] is None:
            continue
        f[conn]["alpn_proto_negotiated"] = \
            f[conn]["alpn_proto_negotiated"].decode(errors="backslashreplace")
    if flow.error:
        f["error"] = flow.error.get_state()

    if isinstance(flow, http.HTTPFlow):
        if flow.request:
            if flow.request.raw_content:
                content_length = len(flow.request.raw_content)
                content_hash = hashlib.sha256(flow.request.raw_content).hexdigest()
            else:
                content_length = None
                content_hash = None
            f["request"] = {
                "method": flow.request.method,
                "scheme": flow.request.scheme,
                "host": flow.request.host,
                "port": flow.request.port,
                "path": flow.request.path,
                "http_version": flow.request.http_version,
                "headers": tuple(flow.request.headers.items(True)),
                "contentLength": content_length,
                "contentHash": content_hash,
                "timestamp_start": flow.request.timestamp_start,
                "timestamp_end": flow.request.timestamp_end,
                "is_replay": flow.request.is_replay,
                "pretty_host": flow.request.pretty_host,
            }
        if flow.response:
            if flow.response.raw_content:
                content_length = len(flow.response.raw_content)
                content_hash = hashlib.sha256(flow.response.raw_content).hexdigest()
            else:
                content_length = None
                content_hash = None
            f["response"] = {
                "http_version": flow.response.http_version,
                "status_code": flow.response.status_code,
                "reason": flow.response.reason,
                "headers": tuple(flow.response.headers.items(True)),
                "contentLength": content_length,
                "contentHash": content_hash,
                "timestamp_start": flow.response.timestamp_start,
                "timestamp_end": flow.response.timestamp_end,
                "is_replay": flow.response.is_replay,
            }
    f.get("server_conn", {}).pop("cert", None)
    f.get("client_conn", {}).pop("mitmcert", None)

    return f
