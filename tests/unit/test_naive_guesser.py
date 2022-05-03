from suggest_five.guess_results import GuessResult as GR
from suggest_five.guess_results import GuessResults
from suggest_five.naive_guesser import NaiveGuesser


def test_naive_guesser_returns_first_item_first() -> None:
    # Given
    guesser = NaiveGuesser(["ABACK", "DEFER"])

    # When
    guess = guesser.guess()

    # Then
    assert guess == "ABACK"


def test_naive_guesser_filters_non_matching_items_and_returns_new_first_item() -> None:
    # Given
    guesser = NaiveGuesser(["ABACK", "DEFER"])

    # When
    guesser.train(
        "ABACK",
        GuessResults((GR.INCORRECT, GR.INCORRECT, GR.INCORRECT, GR.INCORRECT, GR.INCORRECT)),
    )
    guess = guesser.guess()

    # Then
    assert guess == "DEFER"
