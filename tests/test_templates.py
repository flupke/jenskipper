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
        title, stack, error = templates.extract_jinja_error(sys.exc_info())
    assert title == 'Undefined variable encountered in template'
    assert stack == [
        '  File "%s", line 1' % tpl_path,
        '    My name is {{ name }}',
    ]
    assert error == "'name' is undefined"


def test_extract_jinja_error_syntax_error(data_dir):
    tpl_name = 'template_with_syntax_error.txt'
    try:
        templates.render(unicode(data_dir), tpl_name, {})
    except jinja2.TemplateSyntaxError:
        title, stack, error = templates.extract_jinja_error(sys.exc_info())
    tpl_path = data_dir.join(tpl_name)
    assert title == 'Syntax error in template'
    assert stack == [
        '  File "%s", line 1' % tpl_path,
        '    {{ foo',
    ]
    assert error == \
        "unexpected end of template, expected 'end of print statement'."
