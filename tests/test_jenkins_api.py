from jenskipper import jenkins_api


def test_list_jobs(data_dir, httpserver):
    json_data = data_dir.join('api_json.json').open().read()
    httpserver.serve_content(json_data)
    jobs = jenkins_api.list_jobs(httpserver.url)
    assert jobs == ['test-project-for-jenskipper']
