from dataclasses import dataclass

@dataclass
class LLMOption:
    name: str
    provider: str
    model_id: str
    description: str

# Available models configuration
AVAILABLE_MODELS = {
    "groq-llama": LLMOption(
        name="Groq LLaMA",
        provider="groq",
        model_id="llama3-groq-70b-8192-tool-use-preview",
        description="Fast & Best performance for general use"
    ),
    "groq-llama-2": LLMOption(
        name="Groq LLaMA 3.2",
        provider="groq",
        model_id="llama-3.2-11b-text-preview",
        description="Balanced performance for general use"
    ),
}