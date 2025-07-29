# SPDX-FileCopyrightText: 2024 Red Hat, Inc
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Unit tests for the message schema."""

import pytest
from jsonschema import ValidationError

from .. import messages


class TestMessageV1:
    """A set of unit tests to ensure the schema works as expected."""

    msg_class = messages.MessageV1

    def setup_method(self, method):
        self.minimal_message = {
            "mlist": {"list_name": "infrastructure"},
            "msg": {
                "from": "JD <jd@example.com>",
                "subject": "A sample email",
                "to": "infrastructure@lists.fedoraproject.org",
                "body": "hello world",
            },
        }
        self.full_message = {
            "mlist": {"list_name": "infrastructure"},
            "msg": {
                "from": "Me <me@example.com>",
                "cc": "them@example.com",
                "to": "you@example.com",
                "delivered-to": "someone@example.com",
                "x-mailman-rule-hits": "3",
                "x-mailman-rule-misses": "0",
                "x-message-id-hash": "potatoes",
                "references": "<abc-123@example.com>",
                "in-reply-to": "<abc-123@example.com",
                "message-id": "12345",
                "archived-at": "<http://example.com/12345>",
                "subject": "A sample email",
                "body": "hello world",
            },
        }

    def test_minimal_message(self):
        """
        Assert the message schema validates a message with the minimal number
        of required fields.
        """
        message = self.msg_class(body=self.minimal_message)

        message.validate()

    def test_full_message(self):
        """Assert a message with all fields passes validation."""
        message = self.msg_class(body=self.full_message)

        message.validate()

    def test_missing_fields(self):
        """Assert an exception is actually raised on validation failure."""
        del self.minimal_message["mlist"]
        message = self.msg_class(body=self.minimal_message)

        with pytest.raises(ValidationError):
            message.validate()

    def test_str(self):
        """Assert __str__ produces a human-readable message."""
        expected_str = "Subject: A sample email\nhello world\n"
        message = self.msg_class(body=self.full_message)

        message.validate()
        assert expected_str == str(message)

    def test_summary(self):
        """Assert the summary matches the message subject."""
        message = self.msg_class(body=self.full_message)

        assert "A sample email" == message.summary

    def test_subject(self):
        """Assert the message provides a "subject" attribute."""
        message = self.msg_class(body=self.full_message)

        assert "A sample email" == message.subject

    def test_body(self):
        """Assert the message provides a "body" attribute."""
        message = self.msg_class(body=self.full_message)

        assert "hello world" == message.email_body

    def test_url(self):
        """Assert the message provides a "url" attribute."""
        message = self.msg_class(body=self.full_message)
        assert "http://example.com/12345" == message.url

    def test_agent_name(self):
        """Assert the message provides a "agent_name" attribute."""
        message = self.msg_class(body=self.full_message)
        assert "me" == message.agent_name

    def test_agent_avatar(self):
        """Assert the message provides a "agent_avatar" attribute."""
        message = self.msg_class(body=self.full_message)
        assert (
            "https://seccdn.libravatar.org/avatar/"
            "570ebdf0322c3d5c9680578b437c155933403674cfd50fc70aeebb8f462f7756"
            "?s=64&d=retro" == message.agent_avatar
        )

    def test_usernames(self):
        """Assert the message provides a "usernames" attribute."""
        message = self.msg_class(body=self.full_message)
        assert [] == message.usernames

    def test_packages(self):
        """Assert the message provides a "packages" attribute."""
        message = self.msg_class(body=self.full_message)
        assert [] == message.packages


class TestMessageV2(TestMessageV1):
    """A set of unit tests to ensure the schema works as expected."""

    msg_class = messages.MessageV2

    def setup_method(self, method):
        self.minimal_message = {
            "mailing_list": "infrastructure",
            "from": "JD <jd@example.com>",
            "subject": "A sample email",
            "to": "infrastructure@lists.fedoraproject.org",
            "body": "hello world",
        }
        self.full_message = {
            "mailing_list": "infrastructure",
            "from": "Me <me@example.com>",
            "cc": "them@example.com",
            "to": "you@example.com",
            "delivered-to": "someone@example.com",
            "x-mailman-rule-hits": "3",
            "x-mailman-rule-misses": "0",
            "x-message-id-hash": "potatoes",
            "references": "<abc-123@example.com>",
            "in-reply-to": "<abc-123@example.com",
            "message-id": "12345",
            "archived-at": "<http://example.com/12345>",
            "subject": "A sample email",
            "body": "hello world",
        }

    def test_missing_fields(self):
        """Assert an exception is actually raised on validation failure."""
        del self.minimal_message["body"]
        message = self.msg_class(body=self.minimal_message)

        with pytest.raises(ValidationError):
            message.validate()

    def test_url(self):
        """Assert the message provides a "url" attribute."""
        message = self.msg_class(body=self.full_message)
        assert "http://example.com/12345" == message.url

    def test_agent_name(self):
        """Assert the message provides a "agent_name" attribute."""
        message = self.msg_class(body=self.full_message)
        assert "me" == message.agent_name

    def test_agent_avatar(self):
        """Assert the message provides a "agent_avatar" attribute."""
        message = self.msg_class(body=self.full_message)
        assert (
            "https://seccdn.libravatar.org/avatar/"
            "570ebdf0322c3d5c9680578b437c155933403674cfd50fc70aeebb8f462f7756"
            "?s=64&d=retro" == message.agent_avatar
        )
