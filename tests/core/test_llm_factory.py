import pytest
from app.core.llm_factory import get_llm

def test_get_llm_openai(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "fake-test-key")

    llm = get_llm("openai")

    assert llm.__class__.__name__ == "ChatOpenAI"

def test_get_llm_anthropic(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fake-test-key")

    llm = get_llm("anthropic")

    assert llm.__class__.__name__ == "ChatAnthropic"

def test_get_llm_google(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "fake-test-key")

    llm = get_llm("google")

    assert llm.__class__.__name__ == "ChatGoogleGenerativeAI"

def test_get_llm_ollama():
    llm = get_llm("ollama")

    assert llm.__class__.__name__ == "ChatOllama"

def test_get_llm_unsupported():
    with pytest.raises(ValueError, match="Unsupported LLM Provider: hal9000"):
        get_llm("hal9000")