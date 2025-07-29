import pytest

from meta_agent.services.guardrail_router import GuardrailModelRouter


class MockAdapter:
    def __init__(self):
        self.prompts: list[str] = []

    async def invoke(self, prompt: str, context=None) -> str:
        self.prompts.append(prompt)
        return f"{prompt}:ok"


@pytest.mark.asyncio
async def test_router_selects_model():
    a1 = MockAdapter()
    a2 = MockAdapter()
    router = GuardrailModelRouter({"a": a1, "b": a2}, default_model="a")

    res = await router.invoke("hi", model="b")

    assert res == "hi:ok"
    assert a2.prompts == ["hi"]
    assert not a1.prompts


@pytest.mark.asyncio
async def test_guardrails_called_in_order():
    adapter = MockAdapter()
    router = GuardrailModelRouter({"a": adapter}, default_model="a")
    order: list[str] = []

    async def input_guardrail(prompt: str):
        order.append(f"in:{prompt}")

    async def output_guardrail(output: str):
        order.append(f"out:{output}")

    router.add_input_guardrail(input_guardrail)
    router.add_output_guardrail(output_guardrail)

    res = await router.invoke("test")

    assert res == "test:ok"
    assert order == ["in:test", "out:test:ok"]


@pytest.mark.asyncio
async def test_unknown_model_raises():
    adapter = MockAdapter()
    router = GuardrailModelRouter({"a": adapter}, default_model="a")
    with pytest.raises(ValueError):
        await router.invoke("hi", model="missing")


def test_router_init_requires_adapters():
    with pytest.raises(ValueError):
        GuardrailModelRouter({}, default_model="a")


def test_router_init_requires_valid_default():
    with pytest.raises(ValueError):
        GuardrailModelRouter({"a": MockAdapter()}, default_model="b")


@pytest.mark.asyncio
async def test_input_guardrail_exception_propagates():
    adapter = MockAdapter()
    router = GuardrailModelRouter({"a": adapter}, default_model="a")

    async def bad_guard(_prompt: str):
        raise RuntimeError("bad")

    router.add_input_guardrail(bad_guard)

    with pytest.raises(RuntimeError):
        await router.invoke("x")
    assert not adapter.prompts


@pytest.mark.asyncio
async def test_output_guardrail_exception_propagates():
    adapter = MockAdapter()
    router = GuardrailModelRouter({"a": adapter}, default_model="a")

    async def bad_guard(_output: str):
        raise RuntimeError("bad")

    router.add_output_guardrail(bad_guard)

    with pytest.raises(RuntimeError):
        await router.invoke("x")
