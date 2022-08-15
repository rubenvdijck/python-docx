# encoding: utf-8

"""
Custom element classes related to paragraphs (CT_P).
"""

from ..ns import qn
from ..xmlchemy import BaseOxmlElement, OxmlElement, ZeroOrMore, ZeroOrOne


class CT_Ins(BaseOxmlElement):
    """
    ``<w:ins>`` element, containing the properties and text for a paragraph.
    """
    r = ZeroOrMore('w:r')

    def clear_content(self):
        """
        Remove all child elements, except the ``<w:pPr>`` element if present.
        """
        for child in self[:]:
            if child.tag == qn('w:pPr'):
                continue
            self.remove(child)
