from unittest import mock

import notification


def test_routes_to_telegram_when_configured(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123:abc")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "999")

    with mock.patch("notification.requests.post") as post:
        notification.Notification()._send_discord_webhook("http://discord", "hi :moneybag:")

    url = post.call_args.args[0]
    assert url == "https://api.telegram.org/bot123:abc/sendMessage"
    assert post.call_args.kwargs["json"] == {"chat_id": "999", "text": "hi 💰"}


def test_falls_back_to_webhook_without_telegram(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)

    with mock.patch("notification.requests.post") as post:
        notification.Notification()._send_discord_webhook("http://discord", "hi")

    assert post.call_args.args[0] == "http://discord"
