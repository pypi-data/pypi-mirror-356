import pytest

from yib import yconsole


def test_fatal():
    console = yconsole.Console()
    with pytest.raises(SystemExit):
        console.fatal("This is a fatal message.")
