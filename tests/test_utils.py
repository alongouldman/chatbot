from bot_utils import extract_number


def test_extract_number():
	assert extract_number('123') == 123
	assert extract_number(' 34 ') == 34
	assert extract_number(' -34 ') == -34
	assert extract_number(' 3.4 ') == 3.4
	assert extract_number(' 000000002 ') == 2
	assert extract_number(' awdads34dasdad ') == 34
	assert extract_number(' awdads-34dasdad ') == -34
	assert extract_number(' awdads-3kh4dasdad ') == -3

