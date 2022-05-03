import curses as standard_curses
from unittest.mock import MagicMock, call

from pytest import fixture

from suggest_five.guess_results import GuessResult as GR
from suggest_five.guess_results import GuessResults
from suggest_five.ui import UserInterface


@fixture
def screen() -> MagicMock:
    mock_screen = MagicMock(spec=standard_curses.window)
    mock_screen.captured_output = []

    def mock_addstr(row: int, col: int, text: str) -> None:
        highest_row = len(mock_screen.captured_output) - 1

        if row > highest_row:
            mock_screen.captured_output.extend([""] * (row - highest_row))

        row_chars = list(mock_screen.captured_output[row])
        row_length = len(row_chars)

        if row_length < col:
            row_chars.extend([" "] * (col - row_length))

        row_chars[col : col + len(text)] = list(text)
        mock_screen.captured_output[row] = "".join(row_chars)

    mock_screen.addstr.side_effect = mock_addstr
    mock_screen.getkey.side_effect = ["g", "b", "y", "b", "b", "\n"]

    return mock_screen


@fixture
def curses(screen: MagicMock) -> MagicMock:
    mock_curses = MagicMock(spec=standard_curses)
    mock_curses.initscr.return_value = screen
    return mock_curses


def test_ui_initialises_curses(curses: MagicMock, screen: MagicMock) -> None:
    # Given
    # When
    # Then
    with UserInterface(curses):
        curses.initscr.assert_called_once_with()
        curses.noecho.assert_called_once_with()
        curses.cbreak.assert_called_once_with()
        screen.keypad.assert_called_once_with(True)
        screen.addstr.assert_has_calls([call(0, 0, "suggest_five"), call(1, 0, "------------")])

    curses.nocbreak.assert_called_once_with()
    screen.keypad.assert_has_calls([call(True), call(False)])
    curses.echo.assert_called_once_with()
    curses.endwin.assert_called_once_with()


def test_ui_displays_first_guess(curses: MagicMock, screen: MagicMock) -> None:
    # Given
    # When
    with UserInterface(curses) as ui:
        ui.display_guess("ELVIS")

    assert screen.captured_output == ["suggest_five", "------------", "", "ELVIS [          ]"]


def test_ui_gets_and_displays_guess_results(curses: MagicMock, screen: MagicMock) -> None:
    # Given
    # When
    with UserInterface(curses) as ui:
        ui.display_guess("ADEPT")
        guess_results = ui.get_guess_results()

    assert guess_results == GuessResults((GR.CORRECT, GR.INCORRECT, GR.MOVED, GR.INCORRECT, GR.INCORRECT))
    assert screen.captured_output == ["suggest_five", "------------", "", "ADEPT [🟩 ⬛ 🟨 ⬛ ⬛ ]"]


def test_ui_ignores_backspace_on_empty_input(curses: MagicMock, screen: MagicMock) -> None:
    # Given
    # When
    with UserInterface(curses) as ui:
        ui.display_guess("ELVIS")
        screen.getkey.side_effect = ["KEY_BACKSPACE", "y", "y", "g", "y", "g", "\n"]
        ui.get_guess_results()

    assert screen.captured_output == ["suggest_five", "------------", "", "ELVIS [🟨 🟨 🟩 🟨 🟩 ]"]


def test_ui_supports_backspace(curses: MagicMock, screen: MagicMock) -> None:
    # Given
    # When
    with UserInterface(curses) as ui:
        ui.display_guess("ELVIS")
        screen.getkey.side_effect = ["y", "y", "g", "y", "b", "KEY_BACKSPACE", "g", "\n"]
        ui.get_guess_results()

    assert screen.captured_output == ["suggest_five", "------------", "", "ELVIS [🟨 🟨 🟩 🟨 🟩 ]"]
