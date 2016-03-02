from xml.etree import ElementTree


try:
    from lxml import etree
    HAVE_LXML = True
except ImportError:
    HAVE_LXML = False


def format_xml(text):
    '''
    Format the XML in *text*.
    '''
    if HAVE_LXML:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.fromstring(text.encode('utf8'), parser)
        return etree.tostring(tree, pretty_print=True, xml_declaration=True,
                              encoding='UTF-8')
    else:
        return text


def unescape_xml(xml):
    tree = ElementTree.fromstring(xml.encode('utf8'))
    return ElementTree.tostring(tree, encoding='UTF-8', method='xml')
