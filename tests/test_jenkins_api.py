import pytest

from jenskipper import jenkins_api
from jenskipper import exceptions


def test_list_jobs(data_dir, httpserver):
    json_data = data_dir.join('api_json.json').open().read()
    httpserver.serve_content(json_data)
    jobs = jenkins_api.list_jobs(httpserver.url)
    assert jobs == ['test-project-for-jenskipper']


def test_push_job_config_type_mismatch(httpserver, data_dir):
    body = data_dir.join('push_job_conf_type_error.html').open().read()
    httpserver.serve_content(body, 500)
    with pytest.raises(exceptions.JobTypeMismatch) as excinfo:
        jenkins_api.push_job_config(httpserver.url, 'job_name', '')
    exc = excinfo.value
    assert exc.pushed_type == 'hudson.matrix.MatrixProject'
    assert exc.expected_type == 'hudson.model.FreeStyleProject'
