from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

def get_llm(provider: str, **kwargs):
    provider = provider.lower()

    if provider == "openai":
        model = kwargs.pop("model", "gpt-3.5-turbo")
        return ChatOpenAI(model=model, **kwargs)

    elif provider == "anthropic":
        model = kwargs.pop("model", "claude-3-haiku-20240307")
        return ChatAnthropic(model=model, **kwargs)

    elif provider == "google":
        model = kwargs.pop("model", "gemini-1.5-flash")
        return ChatGoogleGenerativeAI(model=model, **kwargs)

    elif provider == "ollama":
        model = kwargs.pop("model", "llama3")
        return ChatOllama(model=model, **kwargs)

    else:
        raise ValueError(f"Unsupported LLM Provider: {provider}")