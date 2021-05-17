import os
from dataclasses import dataclass
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()


@dataclass
class CompletionRequest:
    started_ts: int
    filename: str
    code: str
    offset: int
    prefix: str = ""
    mode: str = "FULL_LINE"
    num_iterations: int = 5
    beam_size: int = 6
    diversity_groups: int = 1
    diversity_strength: float = 0.3
    len_norm_base: float = 2.0
    len_norm_pow: float = 0.7
    top_n: int = 3
    only_full_lines: bool = False
    group_answers: bool = False
    context_len: int = -1
    min_prefix_dist: float = 0.2
    min_edit_dist: float = 0.0
    keep_kinds: tuple = ("short", "prob")


class CompletionClient:
    def __init__(self, language: str, url: str = None):
        self.language = language.lower()
        self.auth_token = os.getenv("FLCC_KEY")
        assert self.auth_token
        if not url:
            self.url = os.getenv(f"FLCC_{language.upper()}_URL")
            if not self.url:
                url_template = os.getenv("FLCC_URL_TEMPLATE")
                assert url_template is not None, "URL is not specified"
                self.url = url_template.format(language=language.lower())
        else:
            self.url = url

    def complete(self, filename: str, context: str, prefix: str = ""):
        complete_url = f"{self.url}/v1/complete/gpt"
        prep_context = self.preprocess_context(context)
        request = CompletionRequest(
            started_ts=int(datetime.now().timestamp() * 1000),
            filename=filename,
            code=prep_context,
            prefix=prefix,
            offset=len(context) - len(prefix),
        )
        s = requests.Session()
        http_request = requests.Request(
            "POST",
            complete_url,
            json=request.__dict__,
            headers={"Authorization": "a99a760b-1a57-4ff5-871c-5463fa1f132b"},
        ).prepare()
        return s.send(http_request).json()

    def preprocess_context(self, context: str):
        new_context = context
        if self.language == "python":
            pass  # TODO: format with black

        new_context = new_context.replace("    ", "\t")
        return new_context
