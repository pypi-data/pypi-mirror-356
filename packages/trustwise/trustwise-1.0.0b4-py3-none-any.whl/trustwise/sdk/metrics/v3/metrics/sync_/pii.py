from trustwise.sdk.client import TrustwiseClient
from trustwise.sdk.metrics.base import PIIMetricBase
from trustwise.sdk.types import PIIResponse


class PIIMetric(PIIMetricBase):
    def __init__(self, client: TrustwiseClient) -> None:
        self.client = client
        self.base_url = client.config.get_safety_url("v3")

    def evaluate(self, *, text: str, allowlist: list[str], blocklist: list[str], **kwargs) -> PIIResponse:
        request_dict = self._build_request(text=text, allowlist=allowlist, blocklist=blocklist, **kwargs)
        result = self.client._post(
            endpoint=f"{self.base_url}/pii",
            data=request_dict
        )
        return PIIResponse(**result)

    def batch_evaluate(self, texts: list[str], allowlist: list[str] | None = None, blocklist: list[str] | None = None) -> list[PIIResponse]:
        raise NotImplementedError("Batch evaluation not yet supported") 