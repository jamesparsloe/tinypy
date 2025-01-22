import pytest
from tinypy.parser import parse


@pytest.mark.parametrize(
    "source",
    [
        "10 + 1",
        "(10 + 1)",
        "((10 + (1 + (1 + 10))))",
        "10 + 2.9 * 4 / 3.4 - 1.2 + 1",
        "(10.7 + 3.1) * 2",
    ],
)
def test_parse_doesnt_crash(source: str):
    expr = parse(source)
