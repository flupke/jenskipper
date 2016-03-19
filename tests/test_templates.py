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
