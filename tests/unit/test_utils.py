from suggest_five.guess_results import GuessResult as GR
from suggest_five.guess_results import GuessResults
from suggest_five.util import filter_word_list


def test_filter_word_list_keeps_word_if_correct():
    # Given
    word_list = ["BARGE"]
    guess_results = GuessResults((GR.CORRECT, GR.CORRECT, GR.CORRECT, GR.CORRECT, GR.CORRECT))

    # When
    filtered = filter_word_list(word_list, "BARGE", guess_results)

    # Then
    assert filtered == ["BARGE"]


def test_filter_word_list_removes_word_if_word_different_from_correct_guess():
    # Given
    word_list = ["LARGE"]
    guess_results = GuessResults((GR.CORRECT, GR.CORRECT, GR.CORRECT, GR.CORRECT, GR.CORRECT))

    # When
    filtered = filter_word_list(word_list, "BARGE", guess_results)

    # Then
    assert filtered == []


def test_filter_word_list_removes_word_if_character_incorrect_but_matching():
    # Given
    word_list = ["BARGE"]
    guess_results = GuessResults((GR.INCORRECT, GR.CORRECT, GR.CORRECT, GR.CORRECT, GR.CORRECT))

    # When
    filtered = filter_word_list(word_list, "BARGE", guess_results)

    # Then
    assert filtered == []


def test_filter_word_list_removes_word_if_incorrect_character_still_present_in_different_position():
    # Given
    word_list = ["ACORN"]
    guess_results = GuessResults((GR.CORRECT, GR.INCORRECT, GR.INCORRECT, GR.INCORRECT, GR.INCORRECT))

    # When
    filtered = filter_word_list(word_list, "ABACK", guess_results)

    # Then
    assert filtered == []


def test_filter_word_list_keeps_word_if_all_characters_moved():
    # Given
    word_list = ["ELVIS"]
    guess_results = GuessResults((GR.MOVED, GR.MOVED, GR.CORRECT, GR.MOVED, GR.CORRECT))

    # When
    filtered = filter_word_list(word_list, "LIVES", guess_results)

    # Then
    assert filtered == ["ELVIS"]


def test_filter_word_list_removes_word_if_moved_characters_are_not_moved():
    # Given
    word_list = ["DEATH"]
    guess_results = GuessResults((GR.MOVED, GR.MOVED, GR.CORRECT, GR.INCORRECT, GR.MOVED))

    # When
    filtered = filter_word_list(word_list, "DEALT", guess_results)

    # Then
    assert filtered == []


def test_filter_word_list_removes_word_if_too_few_occurrences_of_moved_character():
    # Given
    word_list = ["PURER"]
    guess_results = GuessResults((GR.INCORRECT, GR.MOVED, GR.MOVED, GR.INCORRECT, GR.INCORRECT))

    # When
    filtered = filter_word_list(word_list, "BEECH", guess_results)

    # Then
    assert filtered == []


def test_filter_word_list_keeps_word_if_correct_number_of_occurrences_of_moved_character():
    # Given
    word_list = ["PUREE"]
    guess_results = GuessResults((GR.INCORRECT, GR.MOVED, GR.MOVED, GR.INCORRECT, GR.INCORRECT))

    # When
    filtered = filter_word_list(word_list, "BEECH", guess_results)

    # Then
    assert filtered == ["PUREE"]


def test_filter_word_list_keeps_word_if_correct_number_of_occurrences_of_moved_character2():
    # Given
    word_list = ["ALIGN"]
    guess_results = GuessResults((GR.CORRECT, GR.MOVED, GR.CORRECT, GR.MOVED, GR.INCORRECT))

    # When
    filtered = filter_word_list(word_list, "AGING", guess_results)

    # Then
    assert filtered == ["ALIGN"]


def test_filter_word_list_keeps_word_if_more_occurrences_of_moved_character():
    # Given
    word_list = ["EAAEE"]
    guess_results = GuessResults((GR.INCORRECT, GR.MOVED, GR.MOVED, GR.INCORRECT, GR.INCORRECT))

    # When
    filtered = filter_word_list(word_list, "BEECH", guess_results)

    # Then
    assert filtered == ["EAAEE"]
