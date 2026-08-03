"""Unit tests for the model migration benchmark harness."""
from dataclasses import dataclass
import pytest


@dataclass
class BenchmarkResult:
    model: str
    location: str
    query: str
    latency_seconds: float
    response_text: str
    tool_calls: list[str]


def test_benchmark_result_structure():
    res = BenchmarkResult(
        model="gemini-3.5-flash",
        location="global",
        query="test query",
        latency_seconds=1.25,
        response_text="sample response",
        tool_calls=["ask_data_insights"],
    )
    assert res.model == "gemini-3.5-flash"
    assert res.location == "global"
    assert res.latency_seconds == 1.25
    assert res.tool_calls == ["ask_data_insights"]
