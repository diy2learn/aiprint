from aiprint.helper import extract_status, str2bool


def test_str2bool():
    assert str2bool("yes")
    assert not str2bool("n")


def test_extract_status():
    data = {"success": False, "other_field": 123}
    assert extract_status(str(data), pattern="'success': (\w+)") == "False"
