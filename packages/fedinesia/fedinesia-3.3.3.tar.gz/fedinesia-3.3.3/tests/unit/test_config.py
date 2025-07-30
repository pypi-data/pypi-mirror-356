# ruff: noqa: D103, S101, S105, S106
"""Unit tests for 'BotConfig' and 'MastodonConfig' classes."""

from fedinesia.config import BotConfig
from fedinesia.config import MastodonConfig


def test_default_bot_configuration() -> None:
    """Test creation of Configuration class."""
    config = BotConfig(delete_after=12)

    assert config.delete_after == 12
    assert not config.skip_deleting_pinned
    assert not config.skip_deleting_faved
    assert not config.skip_deleting_bookmarked
    assert not config.skip_deleting_poll
    assert not config.skip_deleting_media
    assert config.skip_deleting_faved_at_least == 0
    assert config.skip_deleting_boost_at_least == 0
    assert config.skip_deleting_reactions_at_least == 0
    assert isinstance(config.skip_deleting_visibility, list)
    assert len(config.skip_deleting_visibility) == 0


def test_default_mastodon_config() -> None:
    config = MastodonConfig(instance="instance", access_token="token")

    assert config.instance == "instance"
    assert config.access_token == "token"
