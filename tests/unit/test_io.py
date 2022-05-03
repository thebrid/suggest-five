from io import StringIO

from pytest import raises

from suggest_five.io import load_words_from_file


def test_load_words_from_file_yields_nothing_from_empty_file() -> None:
    # Given
    input_file = StringIO()

    # When
    actual_output = list(load_words_from_file(input_file))

    # Then
    assert actual_output == []


def test_load_words_from_file_yields_upper_case_single_word_for_file_with_single_word() -> None:
    # Given
    input_file = StringIO("apple")

    # When
    actual_output = list(load_words_from_file(input_file))

    # Then
    assert actual_output == ["APPLE"]


def test_load_words_from_file_yields_multiple_words() -> None:
    # Given
    input_file = StringIO("apple\nbagel\ncocoa")

    # When
    actual_output = list(load_words_from_file(input_file))

    # Then
    assert actual_output == ["APPLE", "BAGEL", "COCOA"]


def test_load_words_from_file_raises_on_overlong_word() -> None:
    # Given
    input_file = StringIO("banana")

    # When
    # Then
    with raises(ValueError):
        list(load_words_from_file(input_file))
