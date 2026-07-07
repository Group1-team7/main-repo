import re

_ZERO_WIDTH = re.compile("[\u200b\u200c\u200d\ufeff]")


def clean_contract_text(contract_text: str) -> str:
    """Normalize pasted text while preserving clause-friendly line breaks."""
    # TODO[PERSON-2]: Add Arabic normalization only after testing against sample contracts.
    text = _ZERO_WIDTH.sub("", contract_text or "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    text = "\n".join(line for line in lines if line)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
