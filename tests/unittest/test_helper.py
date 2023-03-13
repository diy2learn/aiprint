from aiprint.helper import str2bool


def test_str2bool():
    assert str2bool("yes")
    assert not str2bool("n")
