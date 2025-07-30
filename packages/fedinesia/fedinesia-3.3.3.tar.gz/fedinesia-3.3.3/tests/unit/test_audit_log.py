# ruff: noqa: D103, S101
"""Unit tests for 'AuditLog' class."""

import tempfile
from collections import deque
from datetime import datetime
from datetime import timezone
from pathlib import Path
from typing import Any

import pytest
from freezegun import freeze_time
from minimal_activitypub import Status
from minimal_activitypub import Visibility

from fedinesia.util import AuditLog


@pytest.fixture(scope="function")
def temp_file() -> Any:
    temporary_file = tempfile.NamedTemporaryFile(delete=False)
    yield temporary_file

    temporary_file_path = Path(temporary_file.name)
    temporary_file_path.unlink()
    assert not temporary_file_path.exists()


@pytest.fixture
def plain_log_line() -> str:
    return (
        "2025-01-17 17:31:47 - Removed poll https://mastodon.social/@trwnh/103254193998341330 "
        "created @ 2025-01-17T16:31:47.000000+00:00 with public visibility, 1 attachments. "
        "This status was reblogged 4 times and favourited 5 times. The status was pinned.\n"
    )


@pytest.fixture
def csv_log_line() -> str:
    return (
        '"2025-01-17 17:31:47","poll","https://mastodon.social/@trwnh/103254193998341330",'
        '"2025-01-17 16:31:47+00:00","public","1","4","5","True"\n'
    )


@pytest.fixture
def status() -> Status:
    return {
        "id": "103254193998341330",
        "created_at": "2025-01-17T16:31:47.000000+00:00",
        "in_reply_to_id": "null",
        "in_reply_to_account_id": "null",
        "sensitive": "false",
        "spoiler_text": "",
        "visibility": Visibility.PUBLIC.value,
        "language": "en",
        "uri": "https://mastodon.social/users/trwnh/statuses/103254193998341330",
        "url": "https://mastodon.social/@trwnh/103254193998341330",
        "replies_count": 3,
        "reblogs_count": 4,
        "favourites_count": 5,
        "favourited": True,
        "reblogged": True,
        "muted": "false",
        "bookmarked": True,
        "pinned": True,
        "text": "test",
        "reblog": "null",
        "application": {"name": "Web", "website": "null"},
        "account": {
            "id": "14715",
            "username": "trwnh",
            "acct": "trwnh",
            "display_name": "infinite love ⴳ",
        },
        "media_attachments": [
            {
                "id": "22345792",
                "type": "image",
                "url": "https://files.mastodon.social/media_attachments/files/022/345/792/original/57859aede991da25.jpeg",
                "preview_url": "https://files.mastodon.social/media_attachments/files/022/345/792/small/57859aede991da25.jpeg",
                "remote_url": "null",
                "text_url": "https://mastodon.social/media/2N4uvkuUtPVrkZGysms",
                "meta": {
                    "original": {"width": 640, "height": 480, "size": "640x480", "aspect": 1.3333333333333333},
                    "small": {"width": 461, "height": 346, "size": "461x346", "aspect": 1.3323699421965318},
                    "focus": {"x": -0.27, "y": 0.51},
                },
                "description": "test media description",
                "blurhash": "UFBWY:8_0Jxv4mx]t8t64.%M-:IUWGWAt6M}",
            }
        ],
        "mentions": [],
        "tags": [],
        "emojis": [],
        "card": "null",
        "poll": True,
    }


@freeze_time(datetime(2025, 1, 17, 17, 31, 47, tzinfo=timezone.utc))
def test_plain_audit_log(temp_file, status, plain_log_line) -> None:
    """Test creation of new AuditLog instance."""
    temp_path = Path(temp_file.name)
    (audit_log := AuditLog(audit_log=temp_path.open(mode="at"), style=AuditLog.Style.PLAIN)).begin()
    audit_log.add_entry(status=status)
    audit_log.end()

    with temp_path.open(mode="rt") as audit_file:
        last_line = deque(audit_file, maxlen=1)[0]

    assert last_line == plain_log_line


@freeze_time(datetime(2025, 1, 17, 17, 31, 47, tzinfo=timezone.utc))
def test_csv_audit_log(temp_file, status, csv_log_line) -> None:
    """Test creation of new AuditLog instance."""
    temp_path = Path(temp_file.name)
    (audit_log := AuditLog(audit_log=temp_path.open(mode="at"), style=AuditLog.Style.CSV)).begin()
    audit_log.add_entry(status=status)
    audit_log.end()

    with temp_path.open(mode="rt") as audit_file:
        last_line = deque(audit_file, maxlen=1)[0]

    assert last_line == csv_log_line
