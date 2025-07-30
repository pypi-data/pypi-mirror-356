from simple_talk.helpers import estimate_speech_duration, text_to_sentences_with_min_duration


def test_estimate_speech_duration() -> None:
    assert estimate_speech_duration("Hello there!") < 1

    assert estimate_speech_duration("Hello there! My name is Bob.") > 1


def test_text_to_sentences_with_min_duration() -> None:
    assert text_to_sentences_with_min_duration("Hello there! My name is Bob.", 1) == [
        "Hello there! My name is Bob.",
    ]

    assert text_to_sentences_with_min_duration("Hello there! My name is Bob.", 0.1) == [
        "Hello there!",
        "My name is Bob.",
    ]
