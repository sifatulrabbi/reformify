from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GPTModels:
    gpt_35 = "gpt-3.5-turbo"
    gpt_35_16k = "gpt-3.5-turbo-16k"
    gpt_4 = "gpt-4"
    gpt_4_32k = "gpt-4-32k"
