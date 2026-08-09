import sys
from pathlib import Path
import pytest
from unittest.mock import AsyncMock, MagicMock

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "_shared" / "scripts"))

from record_agent_demo import (
    wait_for_response_completion,
    activate_canvas_mode,
    showcase_canvas_presentation
)

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


@pytest.mark.asyncio
async def test_activate_canvas_mode_success():
    page = MagicMock()
    
    tools_button = MagicMock()
    tools_button.is_visible = AsyncMock(return_value=True)
    tools_button.text_content = AsyncMock(return_value="Tools")
    tools_button.click = AsyncMock()
    
    canvas_item = MagicMock()
    canvas_item.is_visible = AsyncMock(return_value=True)
    canvas_item.text_content = AsyncMock(return_value="Canvas")
    canvas_item.click = AsyncMock()
    
    menu_locator = MagicMock()
    menu_locator.count = AsyncMock(return_value=1)
    menu_locator.nth = MagicMock(return_value=canvas_item)
    
    direct_canvas = MagicMock()
    direct_canvas.first.is_visible = AsyncMock(return_value=False)
    
    def locator_router(selector):
        loc = MagicMock()
        if "button:visible:has-text('Canvas')" in selector:
            return direct_canvas
        if ".cdk-overlay-container" in selector:
            return menu_locator
        loc.first = tools_button
        loc.last = tools_button
        loc.count = AsyncMock(return_value=1)
        loc.is_visible = AsyncMock(return_value=True)
        return loc
        
    page.locator = MagicMock(side_effect=locator_router)
    
    res = await activate_canvas_mode(page)
    assert res is True
    assert tools_button.click.called
    assert canvas_item.click.called


@pytest.mark.asyncio
async def test_activate_canvas_mode_graceful_fallback():
    page = MagicMock()
    
    empty_loc = MagicMock()
    empty_loc.first.is_visible = AsyncMock(return_value=False)
    empty_loc.last.is_visible = AsyncMock(return_value=False)
    empty_loc.is_visible = AsyncMock(return_value=False)
    empty_loc.count = AsyncMock(return_value=0)
    
    page.locator = MagicMock(return_value=empty_loc)
    
    res = await activate_canvas_mode(page)
    assert res is False


@pytest.mark.asyncio
async def test_showcase_canvas_presentation_dom_eval():
    page = MagicMock()
    page.evaluate = AsyncMock(return_value=[
        {"x": 750, "y": 995},
        {"x": 922, "y": 995},
        {"x": 1094, "y": 995},
        {"x": 1266, "y": 995},
    ])
    page.mouse.click = AsyncMock()
    
    await showcase_canvas_presentation(page, num_slides=4, slide_pause=0.01)
    assert page.mouse.click.call_count == 4
    page.mouse.click.assert_any_call(750, 995)
    page.mouse.click.assert_any_call(1266, 995)


@pytest.mark.asyncio
async def test_showcase_canvas_presentation_coordinate_fallback():
    page = MagicMock()
    page.evaluate = AsyncMock(side_effect=Exception("DOM eval failed"))
    page.mouse.click = AsyncMock()
    
    await showcase_canvas_presentation(page, num_slides=4, slide_pause=0.01, resolution="1080p")
    assert page.mouse.click.call_count == 4
    page.mouse.click.assert_any_call(750.0, 995.0)
    page.mouse.click.assert_any_call(1266.0, 995.0)


def test_resolution_configs_mapping():
    from _shared.scripts.record_agent_demo import RESOLUTION_CONFIGS
    assert "1080p" in RESOLUTION_CONFIGS
    assert RESOLUTION_CONFIGS["1080p"] == {"width": 1920, "height": 1080}
    assert "720p" in RESOLUTION_CONFIGS
    assert RESOLUTION_CONFIGS["720p"] == {"width": 1280, "height": 720}


@pytest.mark.asyncio
async def test_scroll_to_bottom_prompt_box_success():
    from _shared.scripts.record_agent_demo import scroll_to_bottom_prompt_box
    page = MagicMock()
    page.evaluate = AsyncMock()
    page.mouse.wheel = AsyncMock()
    
    await scroll_to_bottom_prompt_box(page)
    
    assert page.evaluate.called
    assert page.mouse.wheel.call_count >= 5


@pytest.mark.asyncio
async def test_smooth_mouse_scroll_walkthrough_left_pane():
    from _shared.scripts.record_agent_demo import smooth_mouse_scroll_walkthrough
    page = MagicMock()
    page.mouse.move = AsyncMock()
    page.mouse.wheel = AsyncMock()
    
    await smooth_mouse_scroll_walkthrough(page, resolution="1080p")
    
    # Check mouse positioned over left pane (1920 * 0.25 = 480, 1080 * 0.5 = 540)
    page.mouse.move.assert_called_with(480, 540)
    # Check that wheel was called in both negative (up) and positive (down) directions
    wheel_calls = page.mouse.wheel.call_args_list
    assert len(wheel_calls) >= 70
    assert any(c.args[1] < 0 for c in wheel_calls)
    assert any(c.args[1] > 0 for c in wheel_calls)


