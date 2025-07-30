import pytest
import fakeredis
import time
from contextguard.core import context_guard

r = fakeredis.FakeRedis(decode_responses=True)

@context_guard(lambda x: f"test:{x}", ttl=3, redis_client=r)
def sample_api(x):
    if x == 1:
        raise Exception("Boom")
    return "OK"

def test_failure_then_skip():
    with pytest.raises(Exception):
        sample_api(1)
    result = sample_api(1)
    assert result["status"] == "skipped"
    time.sleep(3)
    with pytest.raises(Exception):
        sample_api(1)

def test_success_skip_enabled():
    @context_guard(lambda x: f"succ:{x}", ttl=3, skip_on_success=True, redis_client=r)
    def hello(x): return f"Hello {x}"

    assert hello("world") == "Hello world"
    result = hello("world")
    assert result["status"] == "skipped"
