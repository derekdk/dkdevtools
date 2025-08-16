from dk_sayhi import say_hi
from dk_sayhi.cli import main


def test_say_hi_string():
    assert say_hi("Alice") == "Hi, Alice!"


def test_cli_main(capsys):
    code = main(["--name", "Bob"])
    captured = capsys.readouterr()
    assert code == 0
    assert captured.out.strip() == "Hi, Bob!"
