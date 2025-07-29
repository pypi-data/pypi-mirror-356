import os
import requests
import json
from types import MappingProxyType
from typing import List
import dataclasses
from ibm_watsonx_ai.foundation_models import ModelInference, Embeddings
from ibm_watsonx_ai.credentials import Credentials
from threading import Lock


ACCESS_URL = "https://iam.cloud.ibm.com/identity/token"
ACCESS_HEADER = {
    "content-type": "application/x-www-form-urlencoded",
    "accept": "application/json",
}

YPQA_URL = "https://yp-qa.ml.cloud.ibm.com"
PROD_URL = "https://us-south.ml.cloud.ibm.com"
DEFAULT_PARAM = MappingProxyType(
    {"min_new_tokens": 0, "decoding_method": "greedy", "max_new_tokens": 100}
)


class WatsonXProvider:
    def __init__(
        self,
        model_id=None,
        api_key=None,
        space_id=None,
        api_endpoint=PROD_URL,
        url=ACCESS_URL,
        timeout=60,
        llm_decode_parameter=DEFAULT_PARAM,
        embedding_model_id=None,
    ):
        super().__init__()
        self.url = url
        if (embedding_model_id is None) and (model_id is None):
            raise Exception("either model_id or embedding_model_id must be specified")
        self.model_id = model_id
        api_key = os.environ.get("WATSONX_APIKEY", api_key)
        if not api_key:
            raise Exception("apikey must be specified")
        self.api_key = api_key
        self.access_data = {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": self.api_key,
        }
        self.api_endpoint = api_endpoint
        space_id = os.environ.get("WATSONX_SPACE_ID", space_id)
        if not space_id:
            raise Exception("space id must be specified")
        self.space_id = space_id
        self.timeout = timeout
        self.embedding_model_id = embedding_model_id
        self.lock = Lock()

        if isinstance(llm_decode_parameter, MappingProxyType):
            llm_decode_parameter = dict(llm_decode_parameter)
        if dataclasses.is_dataclass(llm_decode_parameter):
            llm_decode_parameter = dataclasses.asdict(llm_decode_parameter)

        self.decode_param = llm_decode_parameter
        self._refresh_token()

    def _get_access_token(self):
        response = requests.post(
            self.url, headers=ACCESS_HEADER, data=self.access_data, timeout=self.timeout
        )
        if response.status_code == 200:
            token_data = json.loads(response.text)
            token = token_data["access_token"]

            return token

        raise RuntimeError(
            f"try to acquire access token and get {response.status_code}"
        )

    def _refresh_token(self):
        self.access_token = self._get_access_token()

        if self.embedding_model_id is not None:
            self.embedding_client = Embeddings(
                model_id=self.embedding_model_id,
                credentials=Credentials(token=self.access_token, url=self.api_endpoint),
                space_id=self.space_id,
            )
        else:
            self.embedding_client = None

        if self.model_id is not None:
            self.client = ModelInference(
                model_id=self.model_id,
                params=self.decode_param,
                credentials=Credentials(token=self.access_token, url=self.api_endpoint),
                space_id=self.space_id,
            )
        else:
            self.client = None

    def query(self, sentence: str) -> dict:
        if self.model_id is None:
            raise Exception("model id must be specified for text generation")
        try:
            return self.client.generate([sentence])[0][
                "results"
            ][  # pylint: disable=E1136
                0
            ]
        except Exception as e:
            with self.lock:
                if "authentication_token_expired" in str(e):
                    self._refresh_token()
                raise e

    def batch_query(self, sentences: List[str]) -> List[dict]:
        if self.model_id is None:
            raise Exception("model id must be specified for text generation")
        try:
            outputs = self.client.generate(sentences)
            outputs = [output["results"][0] for output in outputs]
            return outputs
        except Exception as e:
            with self.lock:
                if "authentication_token_expired" in str(e):
                    self._refresh_token()
                raise e
        # pylint: disable=E1133
        return []

    def encode(self, sentences: List[str]) -> List[list]:
        if self.embedding_model_id is None:
            raise Exception("embedding model id must be specified for text encoding")
        output = self.embedding_client.generate(sentences)
        return [entry["embedding"] for entry in output["results"]]


if __name__ == "__main__":
    import os

    provider = WatsonXProvider(model_id="meta-llama/llama-3-2-90b-vision-instruct")

    prompt = """
<|begin_of_text|><|start_header_id|>system<|end_header_id|>


Your username is nwaters and you want to find out timeoff schedule for yourself for 20250101 to 20250303
<|eot_id|><|start_header_id|>user<|end_header_id|>


Reminder:
- try to respond only once per input
- if you get everything you need. respond with END

<|eot_id|>
<|start_header_id|>user<|end_header_id|>
my username is nwaters. what's my timeoff schedule?<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
we need to call get_assignment_id for username nwaters. do you want to make the function call? yes/no<|eot_id|>
<|start_header_id|>user<|end_header_id|>
yes<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
ok, i have your assignment id. what's the start and end date?<|eot_id|>
<|start_header_id|>user<|end_header_id|>
start and end is 20250101 to 20250303<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
Usernwaters did not take anytime off during the period<|eot_id|>

{% endfor -%}
<|eot_id|><|start_header_id|>user<|end_header_id|>
"""

    print(provider.query(prompt))
