import pytest

from models import Category


def test_categories():
	cat = Category('ביטוח', 'vital and reoccuring')
	assert cat.name == 'ביטוח'
	assert cat.type == 'vital and reoccuring'


def test_wrong_category():
	with pytest.raises(AssertionError):
		Category('random', 'random')
