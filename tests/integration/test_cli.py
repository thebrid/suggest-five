from subprocess import check_output


def test_cli():
    command = ["suggest_five"]
    output = check_output(command)
    assert output == b"suggest_five\n------------\n\nSuggested word: CRANE\n"
