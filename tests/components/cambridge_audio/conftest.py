"""Cambridge Audio tests configuration."""

from collections.abc import Generator
from unittest.mock import Mock, patch

from aiostreammagic.models import Info
import pytest

from homeassistant.components.cambridge_audio.const import DOMAIN
from homeassistant.const import CONF_HOST

from tests.common import MockConfigEntry, load_fixture
from tests.components.smhi.common import AsyncMock


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Override async_setup_entry."""
    with patch(
        "homeassistant.components.cambridge_audio.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture
def mock_stream_magic_client() -> Generator[AsyncMock]:
    """Mock an Cambridge Audio client."""
    with (
        patch(
            "homeassistant.components.cambridge_audio.StreamMagicClient",
            autospec=True,
        ) as mock_client,
        patch(
            "homeassistant.components.cambridge_audio.config_flow.StreamMagicClient",
            new=mock_client,
        ),
    ):
        client = mock_client.return_value
        client.host = "192.168.20.218"
        client.info = Info.from_json(load_fixture("get_info.json", DOMAIN))
        client.is_connected = Mock(return_value=True)

        yield client


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Mock a config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="Cambridge Audio CXNv2",
        data={CONF_HOST: "192.168.20.218"},
        unique_id="0020c2d8",
    )
