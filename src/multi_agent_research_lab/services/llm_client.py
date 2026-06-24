"""LLM client abstraction.

Production note: agents should depend on this interface instead of importing an SDK directly.
"""

from dataclasses import dataclass

from multi_agent_research_lab.core.errors import StudentTodoError


@dataclass(frozen=True)
class LLMResponse:
    content: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float | None = None


class LLMClient:
    """Provider-agnostic LLM client skeleton."""

    total_tokens_used: int = 0

    def complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        """Return a model completion."""
        import os
        import time

        if not hasattr(self.__class__, "pipeline"):
            import torch
            from transformers import pipeline
            model_id = os.getenv("OPENAI_MODEL", "Qwen/Qwen2.5-1.5B-Instruct")
            print(f"Loading local model {model_id} via transformers...")
            
            self.__class__.pipeline = pipeline(
                "text-generation", 
                model=model_id, 
                device_map="auto", 
                torch_dtype=torch.float16
            )

        try:
            prompt = f"System: {system_prompt}\nUser: {user_prompt}\nAssistant:"
            
            # Approximate tokens for input
            tokenizer = self.__class__.pipeline.tokenizer
            input_tokens = len(tokenizer.encode(prompt))
            
            res = self.__class__.pipeline(
                prompt, 
                max_new_tokens=512, 
                return_full_text=False,
                pad_token_id=tokenizer.eos_token_id
            )
            output_text = res[0]["generated_text"].strip()
            
            # Approximate tokens for output
            output_tokens = len(tokenizer.encode(output_text))
            
            # Track class level tokens
            self.__class__.total_tokens_used += (input_tokens + output_tokens)
            
            return LLMResponse(
                content=output_text,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=0.0,
            )
        except Exception as e:
            raise RuntimeError(f"LLM request failed: {str(e)}")
