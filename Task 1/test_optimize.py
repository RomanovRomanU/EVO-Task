from collections import namedtuple
import pytest
import main


DATA = {
    'languages': {
        'python': {
            'latest_version': '3.6',
            'site': 'http://python.org',
        },
        'rust': {
            'latest_version': '1.17',
            'site': 'https://rust-lang.org',
        },
    },
    'animals': ['cow', 'penguin'],
}


def test_languages_simple():
    template = 'Python version: {languages[python][latest_version]}'
    new_data = main.optimize_data(template, DATA)

    # Always check that formatted string matches
    formatted = template.format(**DATA)
    optimized = template.format(**new_data)
    assert formatted == optimized

    assert new_data == {
        'languages': {'python': {'latest_version': '3.6'}},
    }


def test_languages_two_keys():
    template = (
        'Python version: {languages[python][latest_version]}\n'
        'Python site: {languages[python][site]}\n'
        'Rust version: {languages[rust][latest_version]}\n'
    )
    new_data = main.optimize_data(template, DATA)

    # Always check that formatted string matches
    formatted = template.format(**DATA)
    optimized = template.format(**new_data)
    assert formatted == optimized

    assert new_data == {
        'languages': {
            'python': {
                'latest_version': '3.6',
                'site': 'http://python.org',
            },
            'rust': {'latest_version': '1.17'},
        },
    }


@pytest.mark.xfail(reason="Advanced test. Optional to implement")
def test_list_keys():
    template = 'Second animal: {animals[2]}'
    new_data = main.optimize_data(template, DATA)

    # Always check that formatted string matches
    formatted = template.format(**DATA)
    optimized = template.format(**new_data)
    assert formatted == optimized

    assert new_data == {
        'animals': [None, 'penguin'],
    }


@pytest.mark.xfail(reason="Advanced test. Optional to implement")
def test_objects():

    Rectangle = namedtuple("Rectangle", "width", "height")

    data = {
        'small_rect': Rectangle(1, 2),
        'big_square': Rectangle(200, 100),
    }

    template = 'Rect width: {small_rect.width}'
    new_data = main.optimize_data(template, data)

    # Always check that formatted string matches
    formatted = template.format(**data)
    optimized = template.format(**new_data)
    assert formatted == optimized

    assert new_data == {
        # We don't strip attributes from the objects, so rectangle is full
        'small_rect': Rectagle(1, 2),
    }
