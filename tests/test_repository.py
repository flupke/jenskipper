import pytest

from jenskipper import repository
from jenskipper import exceptions


def test_get_current_repository(data_dir):
    base_dir = data_dir.join('repos')
    from_dir = base_dir.join('subdir')
    assert repository.search_base_dir(str(from_dir), data_dir) == base_dir
    assert repository.search_base_dir(str(base_dir), data_dir) == base_dir
    with pytest.raises(exceptions.RepositoryNotFound) as exc:
        assert repository.search_base_dir(str(data_dir), data_dir) is None
        assert exc.from_dir == data_dir
