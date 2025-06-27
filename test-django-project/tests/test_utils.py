import pytest

from django_models.utils.string import remove_special_characters, remove_accents


@pytest.mark.parametrize(
    "value,expected",
    [
        ("ASDF/!@#/", "ASDF"),
        ("!$%*ASDF", "ASDF"),
        ("[erasdf]", "erasdf"),
        ("{}áéó", "aeo"),
    ],
)
def test_remove_special_characters(value, expected):
    assert remove_special_characters(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("caça", "caca"),
        ("AÉMON", "AEMON"),
        ("{}áéó", "{}aeo"),
        (
            "opá olha o chão coração, não é îsso vó e vô?",
            "opa olha o chao coracao, nao e isso vo e vo?",
        ),
    ],
)
def test_remove_accents(value, expected):
    assert remove_accents(value) == expected
