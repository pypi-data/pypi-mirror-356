from meta_agent.template_creator import TemplateCreator, validate_template
from meta_agent.template_schema import (
    IOContract,
    TemplateMetadata,
    TemplateCategory,
    TemplateComplexity,
)
from meta_agent.template_registry import TemplateRegistry


def _meta() -> TemplateMetadata:
    return TemplateMetadata(
        slug="demo",
        title="Demo Template",
        description="Simple demo",
        intended_use="demo",
        io_contract=IOContract(input="text", output="text"),
        tools=[],
        guardrails=[],
        model_pref="gpt3",
        category=TemplateCategory.CONVERSATION,
        complexity=TemplateComplexity.BASIC,
        created_by="tester",
        semver="0.1.0",
        last_test_passed="2024-01-01T00:00:00Z",
        tags=["demo"],
    )


def test_validate_template_success() -> None:
    ok, err = validate_template("hello {{ name }}")
    assert ok and err == ""


def test_validate_template_failure() -> None:
    ok, err = validate_template("{% for x in %}")
    assert not ok and err


def test_creator_register(tmp_path) -> None:
    reg = TemplateRegistry(base_dir=tmp_path)
    creator = TemplateCreator(reg)
    path = creator.create(_meta(), "hi {{name}}", version="0.1.0")
    assert path
    assert reg.load_template("demo") == "hi {{name}}"
