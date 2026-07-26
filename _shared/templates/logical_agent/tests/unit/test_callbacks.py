"""Unit tests for the before_agent_callback that injects today's date into
session state.
"""
from unittest.mock import MagicMock
from unittest.mock import patch

from tools.callbacks import CURRENT_DATE_STATE_KEY
from tools.callbacks import set_current_date


@patch("tools.callbacks.datetime")
def test_set_current_date_writes_iso_date_to_temp_state(mock_datetime):
    mock_datetime.date.today.return_value.isoformat.return_value = "2026-07-26"
    mock_context = MagicMock()
    mock_context.state = {}

    result = set_current_date(mock_context)

    assert mock_context.state[CURRENT_DATE_STATE_KEY] == "2026-07-26"
    assert result is None


def test_set_current_date_uses_the_temp_prefix_so_it_is_never_persisted():
    # google.adk.sessions.state.State.TEMP_PREFIX == "temp:" -- values under this
    # prefix are invocation-scoped and never written back to persistent session
    # storage, which matters because this value must be recomputed every turn,
    # never reused from a stale session.
    assert CURRENT_DATE_STATE_KEY.startswith("temp:")


@patch("tools.callbacks.datetime")
def test_set_current_date_does_not_short_circuit_the_agent_turn(mock_datetime):
    # Returning non-None from a before_agent_callback would skip the agent's own
    # LLM call entirely (ADK treats a returned Content as the final response) --
    # this callback must always return None.
    mock_datetime.date.today.return_value.isoformat.return_value = "2026-07-26"
    mock_context = MagicMock()
    mock_context.state = {}

    assert set_current_date(mock_context) is None
