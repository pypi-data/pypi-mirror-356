import json

class Response:
    def __init__(self, raw_data):
        header_data, body = raw_data.split(b"\r\n\r\n", 1)
        self.body = body.decode("utf-8")
        lines = header_data.decode("utf-8").splitlines()
        self.status = int(lines[0].split()[1])
        self.headers = {}

        for line in lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                self.headers[key.lower()] = value

    def text(self):
        return self.body

    def json(self):
        return json.loads(self.body)
