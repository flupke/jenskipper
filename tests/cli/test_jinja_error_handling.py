from click.testing import CliRunner

from jenskipper.cli import main


def test_template_not_found(data_dir):
    repos_dir = str(data_dir.join('repos'))
    runner = CliRunner()
    result = runner.invoke(main.main, ['show', '--jk-dir', repos_dir,
                                       'missing_template'])
    assert result.exit_code == 1
    assert result.output == 'Template not found: no_template.xml\n'


def test_syntax_error(data_dir):
    repos_dir = str(data_dir.join('repos'))
    runner = CliRunner()
    result = runner.invoke(main.main, ['show', '--jk-dir', repos_dir,
                                       'syntax_error'])
    assert result.exit_code == 1
    assert result.output.splitlines() == [
        'Traceback (most recent call last):',
        '',
        '  File "templates/syntax_error.txt", line 1',
        '    {{ foo',
        '',
        "Syntax error: unexpected end of template, expected "
        "'end of print statement'"
    ]


def test_undefined_var(data_dir):
    repos_dir = str(data_dir.join('repos'))
    runner = CliRunner()
    result = runner.invoke(main.main, ['show', '--jk-dir', repos_dir,
                                       'undefined_var'])
    assert result.exit_code == 1
    assert result.output.splitlines() == [
        'Traceback (most recent call last):',
        '',
        '  File "templates/undefined_var.txt", line 1',
        '    {{ foo }}',
        '',
        "Undefined variable: 'foo' is undefined",
    ]
