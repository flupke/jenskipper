from jenskipper import utils


def test_split_auth():
    assert utils.split_auth_in_url('http://127.0.0.1/') == \
        ('http://127.0.0.1/', None, None)
    assert utils.split_auth_in_url('http://127.0.0.1:123/') == \
        ('http://127.0.0.1:123/', None, None)
    assert utils.split_auth_in_url('http://foo@127.0.0.1:123/') == \
        ('http://127.0.0.1:123/', 'foo', None)
    assert utils.split_auth_in_url('http://foo:bar@127.0.0.1:123/') == \
        ('http://127.0.0.1:123/', 'foo', 'bar')
