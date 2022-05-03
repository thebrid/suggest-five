from os.path import dirname, join
from typing import Iterable
from unittest.mock import MagicMock, call, patch

from click.testing import CliRunner
from pytest import fixture

from suggest_five.__main__ import suggest_five
from suggest_five.guess_results import GuessResult as GR
from suggest_five.guess_results import GuessResults


@fixture
def mock_ui_constructor() -> Iterable[MagicMock]:
    with patch("suggest_five.__main__.UserInterface") as patched:
        yield patched


def test_integration(mock_ui_constructor: MagicMock) -> None:
    # Given
    answers_filename = join(dirname(__file__), "example_answers.txt")
    mock_ui = mock_ui_constructor.return_value.__enter__.return_value
    mock_ui.get_guess_results.side_effect = [
        GuessResults((GR.INCORRECT, GR.INCORRECT, GR.INCORRECT, GR.INCORRECT, GR.INCORRECT)),
        GuessResults((GR.INCORRECT, GR.MOVED, GR.INCORRECT, GR.CORRECT, GR.INCORRECT)),
        GuessResults((GR.MOVED, GR.INCORRECT, GR.INCORRECT, GR.CORRECT, GR.INCORRECT)),
        GuessResults((GR.INCORRECT, GR.INCORRECT, GR.CORRECT, GR.CORRECT, GR.INCORRECT)),
        GuessResults((GR.CORRECT, GR.CORRECT, GR.CORRECT, GR.CORRECT, GR.CORRECT)),
    ]
    runner = CliRunner()

    # When
    result = runner.invoke(suggest_five, ["-a", answers_filename])

    # Then
    assert result.exit_code == 0
    mock_ui_constructor.assert_called_once_with()
    mock_ui.display_guess.assert_has_calls(
        [
            call("ABACK"),
            call("DEFER"),
            call("EXPEL"),
            call("QUEEN"),
            call("SHEET"),
        ]
    )
