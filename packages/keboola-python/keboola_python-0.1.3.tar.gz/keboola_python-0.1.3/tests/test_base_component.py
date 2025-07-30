from keboola_python.base_component import BaseComponent


def test_boom(capsys):
    BaseComponent.boom()
    captured = capsys.readouterr()
    assert "👾💥👾👾👾💥" in captured.out


def test_joom(capsys):
    BaseComponent.joom()
    captured = capsys.readouterr()
    assert "Jim has boomed" in captured.out
