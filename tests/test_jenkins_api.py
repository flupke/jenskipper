from jenskipper import jenkins_api


def test_list_jobs(data_dir, httpserver):
    json_data = data_dir.join('api_json.json').open().read()
    httpserver.serve_content(json_data)
    jobs = jenkins_api.list_jobs(httpserver.url)
    assert jobs == ['test-project-for-jenskipper']


def test_split_auth():
    assert jenkins_api.split_auth('http://127.0.0.1/') == \
        ('http://127.0.0.1/', None, None)
    assert jenkins_api.split_auth('http://127.0.0.1:123/') == \
        ('http://127.0.0.1:123/', None, None)
    assert jenkins_api.split_auth('http://foo@127.0.0.1:123/') == \
        ('http://127.0.0.1:123/', 'foo', None)
    assert jenkins_api.split_auth('http://foo:bar@127.0.0.1:123/') == \
        ('http://127.0.0.1:123/', 'foo', 'bar')
