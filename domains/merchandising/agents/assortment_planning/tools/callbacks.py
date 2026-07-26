"""Callback that injects the current date into session state so agent
instructions can resolve relative date references (e.g. "last two months",
"this week") against the real invocation-time date instead of the LLM's
training-data notion of "today."

See docs/superpowers/specs/2026-07-25-retail-merchandising-adk-agents-design.md
for why this is a before_agent_callback on the root agent only, not a
before_model_callback duplicated onto every agent: this logical agent's
topology is strictly root -> sub-agents, sub-agents are never invoked as
standalone top-level agents, and all agents in one turn share the same
Session/session.state. A single write here, before root's own first LLM
call (and therefore before any transfer_to_agent into a sub-agent), is
sufficient for every sub-agent's instruction to see it later in the same
turn. If this agent's topology ever allows a sub-agent to run standalone,
this would need to move to a before_model_callback on every agent instead.
"""
from __future__ import annotations

import datetime
from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.genai import types

CURRENT_DATE_STATE_KEY = "temp:current_date"


def set_current_date(callback_context: CallbackContext) -> Optional[types.Content]:
  """Writes today's date into session state as an ISO-8601 string.

  Uses the `temp:` state-key prefix (google.adk.sessions.state.State.TEMP_PREFIX)
  because this value is invocation-scoped and must never be persisted or
  reused across turns/sessions -- it is recomputed on every root-agent
  invocation (i.e. every user turn).
  """
  callback_context.state[CURRENT_DATE_STATE_KEY] = datetime.date.today().isoformat()
  return None
