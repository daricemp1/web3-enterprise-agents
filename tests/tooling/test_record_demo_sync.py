import sys
from pathlib import Path
import pytest
from unittest.mock import AsyncMock, MagicMock

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "_shared" / "scripts"))

from record_agent_demo import wait_for_response_completion

@pytest.mark.asyncio
async def test_wait_for_response_completion_state_machine():
    page = MagicMock()
    
    stop_locator = MagicMock()
    stop_locator.count = AsyncMock(side_effect=[1, 1, 0])
    
    def locator_router(selector):
        return stop_locator
        
    page.locator = MagicMock(side_effect=locator_router)
    
    # Execute with short read_pause for test speed
    await wait_for_response_completion(page, turn_index=1, timeout_seconds=10, read_pause=0.1)
    
    assert stop_locator.count.call_count >= 2
