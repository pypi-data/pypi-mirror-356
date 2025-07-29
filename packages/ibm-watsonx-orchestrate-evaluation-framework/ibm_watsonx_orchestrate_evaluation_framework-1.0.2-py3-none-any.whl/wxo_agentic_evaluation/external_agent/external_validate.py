from wxo_agentic_evaluation.external_agent.types import UniversalData
import requests
from typing import Generator
import json


MESSAGES = [{"role": "assistant", "content": "how can i help you"}, {"role": "user", "content": "what's the holiday is June 13th in us?"},
            {"role": "assistant", "content": "tool_name: calendar_lookup, args {\"location\": \"USA\", \"data\": \"06-13-2025\"}}"},
            {"role": "assistant", "content":"it's National Sweing Machine Day"}]


class ExternalAgentValidation:
    def __init__(self, credential, auth_scheme, service_url):
        self.credential = credential
        self.auth_scheme = auth_scheme
        self.service_url = service_url

    def get_auth_header(self):
        if self.auth_scheme == "API_KEY":
            header = {"x-api-key": self.credential}

        elif self.auth_scheme == "BEARER_TOKEN":
            header = {"Authorization": f"Bearer {self.credential}"}

        else:
            raise Exception(f"Auth scheme: {self.auth_scheme} is not supported")

        return header

    def _parse_streaming_evenst(self, resp: Generator[bytes, None, None]):
        data = b''
        for chunk in resp:
            for line in chunk.splitlines(True):
                if line.startswith(b'data:'):
                    line = line.replace(b'data:', b'')
                if line.strip() == b'[DONE]':
                    return
                data += line
                if data.endswith((b'\r\r', b'\n\n', b'\r\n\r\n')):
                    yield data
                    data = b''
        if data:
            yield data

    def call_validation(self, input: str):
        header = {"Content-Type": "application/json"}
        header.update(self.get_auth_header())

        new_messages = []
        new_messages.extend(MESSAGES)
        new_messages.append({"role": "user", "content": input})

        payload = {"messages": new_messages}

        resp = requests.post(url=self.service_url, headers=header, json=payload, stream=True)
        results = []
        for json_str in self._parse_streaming_evenst(resp):
            json_dict = None
            try:
                json_dict = json.loads(json_str)
                UniversalData(**json_dict)
                results.append(json_dict)
            except Exception as e:
                print(f"event parsing failed with {e}")
                raise e

        return results
