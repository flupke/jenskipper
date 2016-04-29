from xml.etree import ElementTree
import urlparse
import copy
import collections

import click


try:
    from lxml import etree
    HAVE_LXML = True
except ImportError:
    HAVE_LXML = False


def clean_xml(text):
    '''
    Clean XML in *text*

    If :mod:`lxml` is available, remove blank text and pretty print it. If
    :mod:`lxml` is not available, return *text* as is.
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


def replace_auth_in_url(url, username, password):
    '''
    Put *username* and *password* in *url*.
    '''
    parsed = urlparse.urlparse(url)
    hostport = _get_hostport(parsed)
    netloc = '%s:%s@%s' % (username, password, hostport)
    replaced = parsed._replace(netloc=netloc)
    return urlparse.urlunparse(replaced)


def split_auth_in_url(url):
    '''
    Extract authentification bits from *url*.

    Return a ``(url_without_auth, username, password)`` tuple.
    '''
    parsed = urlparse.urlparse(url)
    hostport = _get_hostport(parsed)
    without_auth = parsed._replace(netloc=hostport)
    return urlparse.urlunparse(without_auth), parsed.username, parsed.password


def _get_hostport(parsed_url):
    hostport = parsed_url.hostname
    if parsed_url.port is not None:
        hostport += ':%s' % parsed_url.port
    return hostport


def set_path_in_dict(dct, path, value, inplace=False):
    '''
    Set value at *path* in *dct* to *value*.

    *path* is an iterable containing the path to the value. For example
    ``("foo", "bar")`` targets the sub dict "bar" at key "foo" of *dct*.

    By default *dct* is not modfied and a deep copy is returned, unless
    *inplace* is True
    '''
    if inplace:
        cur = ret = dct
    else:
        cur = ret = copy.deepcopy(dct)
    keys = list(path)
    while keys:
        cur_key = keys.pop(0)
        if keys:
            cur = cur.setdefault(cur_key, {})
        else:
            cur[cur_key] = value
    return ret


def deep_merge(dct_a, dct_b, inplace=False):
    '''
    Perform a "deep merge" of *dct_b* into *dct_a*.

    Return the merged result, in a new dict if *inplace* is false, or else in
    *dct_a*.
    '''
    if inplace:
        ret = dct_a
    else:
        ret = copy.deepcopy(dct_a)
    flat_b = flatten_dict(dct_b)
    for path, value in flat_b.items():
        set_path_in_dict(ret, path, value, inplace=True)
    return ret


def flatten_dict(dct):
    '''
    Flatten keys of (possibly nested) *dct*.

    >>> flatten_dict({'a': {'b': 'c'}})
    {('a', 'b'): 'c'}
    '''
    items = _flatten_dict(dct, ())
    return dict(items)


def _flatten_dict(dct, ancestors=()):
    items = []
    for key, value in dct.items():
        path = ancestors + (key,)
        if isinstance(value, collections.Mapping):
            items.extend(_flatten_dict(value, path))
        else:
            items.append((path, value))
    return items
