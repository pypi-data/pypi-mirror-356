# ruff: noqa: D103, S101, S106
"""Unit tests for filtering function 'is_video_included'."""

from datetime import datetime
from datetime import timedelta
from datetime import timezone

import pytest
from freezegun import freeze_time
from minimal_activitypub import Status
from minimal_activitypub import Visibility

from fedinesia.config import BotConfig
from fedinesia.config import Configuration
from fedinesia.config import MastodonConfig
from fedinesia.util import should_keep


@pytest.fixture
def config() -> Configuration:
    mastodon_config = MastodonConfig(instance="http://mastodon.social", access_token="toke")
    bot_config = BotConfig(delete_after=30)
    config = Configuration(bot=bot_config, mastodon=mastodon_config)

    return config


@pytest.fixture
def status() -> Status:
    return {
        "id": "103254193998341330",
        "created_at": (datetime.now(tz=timezone.utc) - timedelta(hours=1)).isoformat(),
        "in_reply_to_id": "null",
        "in_reply_to_account_id": "null",
        "sensitive": "false",
        "spoiler_text": "",
        "visibility": "public",
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


@freeze_time(datetime.now(tz=timezone.utc).replace(hour=0), tz_offset=10)
def test_should_keep_age(config, status) -> None:
    """Test should_keep method with attention to age."""
    assert should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc) - timedelta(days=2), config=config)

    status["created_at"] = (datetime.now(tz=timezone.utc) - timedelta(weeks=52)).isoformat()
    assert not should_keep(
        status=status, oldest_to_keep=datetime.now(tz=timezone.utc) - timedelta(days=2), config=config
    )


def test_deleting_bookmarked(config, status) -> None:
    status["bookmarked"] = True
    config.bot.skip_deleting_bookmarked = True
    assert should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)

    config.bot.skip_deleting_bookmarked = False
    assert not should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)


def test_deleting_faved(config, status) -> None:
    config.bot.skip_deleting_faved = True
    assert should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)

    config.bot.skip_deleting_faved = False
    assert not should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)


def test_deleting_pinned(config, status) -> None:
    config.bot.skip_deleting_pinned = True
    assert should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)

    config.bot.skip_deleting_pinned = False
    assert not should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)


def test_deleting_poll(config, status) -> None:
    config.bot.skip_deleting_poll = True
    assert should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)

    config.bot.skip_deleting_poll = False
    assert not should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)


def test_deleting_visibility(config, status) -> None:
    config.bot.skip_deleting_visibility.append(Visibility.PUBLIC)
    assert should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)

    config.bot.skip_deleting_visibility = []
    assert not should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)


def test_deleting_attachments(config, status) -> None:
    config.bot.skip_deleting_media = True
    assert should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)

    config.bot.skip_deleting_media = False
    assert not should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)


def test_deleting_faved_at_least(config, status) -> None:
    config.bot.skip_deleting_faved_at_least = 2
    assert should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)

    config.bot.skip_deleting_faved_at_least = 100
    assert not should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)


def test_deleting_boots_at_least(config, status) -> None:
    config.bot.skip_deleting_boost_at_least = 2
    assert should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)

    config.bot.skip_deleting_boost_at_least = 100
    assert not should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)


def test_enough_reactions(config, status) -> None:
    config.bot.skip_deleting_reactions_at_least = 1
    assert not should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)

    status["pleroma"] = {"test": "no emojis"}
    config.bot.skip_deleting_reactions_at_least = 10
    assert not should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)

    status["pleroma"] = {
        "emoji_reactions": [
            {"emoji": "thumbs up", "count": 5},
            {"emoji": "heart", "count": 2},
        ]
    }
    config.bot.skip_deleting_reactions_at_least = 10
    assert not should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)

    config.bot.skip_deleting_reactions_at_least = 5
    assert should_keep(status=status, oldest_to_keep=datetime.now(tz=timezone.utc), config=config)
