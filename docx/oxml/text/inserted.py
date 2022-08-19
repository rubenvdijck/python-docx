# encoding: utf-8

"""
Custom element classes related to paragraphs (CT_P).
"""

from ..ns import qn
from ..xmlchemy import BaseOxmlElement, OxmlElement, ZeroOrMore, ZeroOrOne, OptionalAttribute
from ..simpletypes import ST_String


class CT_Ins(BaseOxmlElement):
    """
    ``<w:ins>`` element, containing the properties and text for a paragraph.
    """
    r = ZeroOrMore('w:r')

    author = OptionalAttribute('w:author', ST_String)
    date = OptionalAttribute('w:date', ST_String)

    def clear_content(self):
        """
        Remove all child elements, except the ``<w:pPr>`` element if present.
        """
        for child in self[:]:
            if child.tag == qn('w:pPr'):
                continue
            self.remove(child)
