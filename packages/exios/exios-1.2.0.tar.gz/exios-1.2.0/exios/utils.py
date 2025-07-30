def build_headers(method, host, path, default_headers, custom_headers, body=None):
    headers = f"{method} {path} HTTP/1.1\r\n"
    headers += f"Host: {host}\r\n"
    headers += "Connection: close\r\n"

    combined = default_headers.copy()
    if custom_headers:
        combined.update(custom_headers)

    if body:
        combined['Content-Length'] = str(len(body))
        combined['Content-Type'] = 'application/json'

    for key, value in combined.items():
        headers += f"{key}: {value}\r\n"

    return headers + "\r\n"
