from unittest.mock import patch

import pytest

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.http_retry import default_retry_handlers


@pytest.mark.parametrize("body", ['{"ok": tru', "not json at all"])
@pytest.mark.parametrize("with_retry", [True, False])
def test_non_json_200_raises_slack_api_error(body, with_retry):
    retry_handlers = default_retry_handlers() if with_retry else []
    client = WebClient(token="xoxb-test", retry_handlers=retry_handlers)
    response = {"status": 200, "headers": {}, "body": body}
    with patch.object(client, "_perform_urllib_http_request_internal", return_value=response):
        with pytest.raises(SlackApiError) as exc_info:
            client.api_test()
    assert "Received a response in a non-JSON format" in str(exc_info.value)
    assert body in str(exc_info.value)
