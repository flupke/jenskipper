import sys

import jinja2

from jenskipper import templates


def test_render(data_dir):
    rendered = templates.render(unicode(data_dir), 'template.txt',
                                {'name': 'John'})
    assert rendered == 'My name is John'


def test_render_with_overrides(data_dir):
    rendered = templates.render(unicode(data_dir),
                                'template.txt',
                                {'name': 'John'},
                                context_overrides={'name': 'Jane'})
    assert rendered == 'My name is Jane'


def test_extract_jinja_error_undefined_variable(data_dir):
    tpl_name = 'template.txt'
    tpl_path = data_dir.join(tpl_name)
    try:
        templates.render(unicode(data_dir), tpl_name, {})
    except jinja2.UndefinedError:
        stack, error = templates.extract_jinja_error(sys.exc_info())
    assert stack == [
        '  File "%s", line 1' % tpl_path,
        '    My name is {{ name }}',
    ]
    assert error == "Undefined variable: 'name' is undefined"


def test_extract_jinja_error_syntax_error(data_dir):
    tpl_name = 'template_with_syntax_error.txt'
    try:
        templates.render(unicode(data_dir), tpl_name, {})
    except jinja2.TemplateSyntaxError:
        stack, error = templates.extract_jinja_error(sys.exc_info())
    tpl_path = data_dir.join(tpl_name)
    assert stack == [
        '  File "%s", line 1' % tpl_path,
        '    {{ foo',
    ]
    assert error == "Syntax error: unexpected end of template, expected " \
        "'end of print statement'"


def test_extract_jinja_error_with_fnames_prefix(data_dir):
    tpl_name = 'template.txt'
    try:
        templates.render(unicode(data_dir), tpl_name, {})
    except jinja2.UndefinedError:
        stack, error = templates.extract_jinja_error(sys.exc_info(),
                                                     unicode(data_dir))
    assert stack == [
        '  File "template.txt", line 1',
        '    My name is {{ name }}',
    ]
    assert error == "Undefined variable: 'name' is undefined"
