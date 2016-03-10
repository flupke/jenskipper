import pytest

from jenskipper.cli import decorators
from jenskipper import exceptions


def test_parse_context_vars():
    assert decorators.parse_context_vars(['foo.bar=1', 'baz=2']) == \
        {'foo': {'bar': '1'}, 'baz': '2'}
    with pytest.raises(exceptions.MalformedContextVar) as excinfo:
        decorators.parse_context_vars(['foo'])
    assert str(excinfo.value) == 'foo'
