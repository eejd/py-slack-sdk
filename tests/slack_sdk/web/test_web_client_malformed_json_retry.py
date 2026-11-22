from unittest.mock import patch

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.http_retry import default_retry_handlers


def test_malformed_json_200_with_retry_handlers_raises_slack_api_error():
    client = WebClient(token="xoxb-test", retry_handlers=default_retry_handlers())
    response = {"status": 200, "headers": {}, "body": '{"ok": tru'}
    with patch.object(client, "_perform_urllib_http_request_internal", return_value=response):
        try:
            client.api_test()
        except SlackApiError:
            return
    raise AssertionError("expected SlackApiError")
