from xml.etree import ElementTree

import click


try:
    from lxml import etree
    HAVE_LXML = True
except ImportError:
    HAVE_LXML = False


def format_xml(text):
    '''
    Format the XML in *text*.
    '''
    text = text.strip()
    if HAVE_LXML:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.fromstring(text, parser)
        return etree.tostring(tree, pretty_print=True, xml_declaration=True,
                              encoding='UTF-8')
    else:
        return text


def unescape_xml(xml):
    tree = ElementTree.fromstring(xml)
    return ElementTree.tostring(tree, encoding='UTF-8', method='xml')


def sechowrap(text, wrap_opts={}, **style):
    text = click.wrap_text(text, **wrap_opts)
    click.secho(text, **style)


def print_jobs_list(label, jobs_names, pad_lines=1, empty_label=None, **style):
    if jobs_names:
        click.secho('\n' * pad_lines, nl=False)
        click.secho('%s\n  %s' % (label, '\n  '.join(jobs_names)), **style)
    elif empty_label:
        click.secho(empty_label)
