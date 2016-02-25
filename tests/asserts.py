from lxml import etree


def assert_xml_strings_equal(xml_text_1, xml_text_2):
    xml_text_1 = _normalize_xml(xml_text_1)
    xml_text_2 = _normalize_xml(xml_text_2)
    assert xml_text_1 == xml_text_2


def _normalize_xml(text):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.fromstring(text, parser)
    return etree.tostring(tree, pretty_print=True, xml_declaration=True,
                          encoding='UTF-8')
