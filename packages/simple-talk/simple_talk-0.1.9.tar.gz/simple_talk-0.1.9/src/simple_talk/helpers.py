from extratools_core.seq import add_until
from extratools_text import text_to_sentences
from textstat import syllable_count

# https://www.researchgate.net/publication/235971274_A_cross-Language_Perspective_on_Speech_Information_Rate
ENGLISH_AVERAGE_SYLLABLES_PER_SECOND = 6.19


def estimate_speech_duration(text: str) -> float:
    return syllable_count(text) / ENGLISH_AVERAGE_SYLLABLES_PER_SECOND


def text_to_sentences_with_min_duration(
    text: str,
    min_duration: float = 1,
    *,
    buffer: float = 0.2,
) -> list[str]:
    sentences: list[str] = text_to_sentences(text)

    def cond(sentence: str) -> bool:
        return estimate_speech_duration(sentence.strip()) >= min_duration * (1 + buffer)

    return add_until(sentences, cond, op=lambda x, y: f"{x} {y}")
