import requests
from typing import List, Optional
from .types import RequestParams, ClientOptions, BatchOptions

AVAILABLE_MODELS = [
    "llama3:8b",
    "llama2-uncensored",
    "gemma3",
    "gemma",
    "phi3:mini",
    "mistral",
    "gemma:2b",
    "gemma:7b",
    "qwen:7b",
    "qwen2.5-coder",
    "qwen3",
    "deepseek-coder:6.7b",
    "deepseek-v2:16b",
    "dolphin-mistral:7b",
    "dolphin3",
    "starcoder2:7b",
    "magistral",
    "devstral",
]

class M3ChatClient:
    def __init__(self, options: Optional[ClientOptions] = None) -> None:
        self.stream = options.get("stream", False) if options else False

    def get_response(self, params: RequestParams) -> Optional[str]:
        if params["model"] not in AVAILABLE_MODELS:
            raise ValueError(f"{params['model']} is not a valid model. Available: {AVAILABLE_MODELS}")

        url = "https://m3-chat.vercel.app/api/gen"
        headers = {"Accept": "text/event-stream" if self.stream else "application/json"}
        response = requests.get(url, headers=headers, params=params, stream=self.stream)

        response.raise_for_status()

        if self.stream:
            # Simple streaming print; could be improved with callbacks
            for chunk in response.iter_lines():
                if chunk:
                    print(chunk.decode("utf-8"))
            return None
        else:
            return response.text

    def batch_requests(self, messages: List[str], options: Optional[BatchOptions] = None) -> List[str]:
        results = []
        options = options or {}

        for content in messages:
            params = {"content": content}
            if "model" in options and options["model"]:
                params["model"] = options["model"]

            response = requests.get("https://m3-chat.vercel.app/api/gen", params=params)
            response.raise_for_status()
            results.append(response.text)

        return results
