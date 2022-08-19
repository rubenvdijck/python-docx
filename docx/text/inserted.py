# encoding: utf-8

"""
Paragraph-related proxy types.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..enum.style import WD_STYLE_TYPE
from .parfmt import ParagraphFormat
from .run import Run
from ..shared import Parented


class Inserted(Parented):
    """
    Proxy object wrapping ``<w:ins>`` element.
    """
    def __init__(self, ins, parent):
        super(Inserted, self).__init__(parent)
        self._ins = self._element = ins

    def add_run(self, text=None, style=None):
        """
        Append a run to this paragraph containing *text* and having character
        style identified by style ID *style*. *text* can contain tab
        (``\\t``) characters, which are converted to the appropriate XML form
        for a tab. *text* can also include newline (``\\n``) or carriage
        return (``\\r``) characters, each of which is converted to a line
        break.
        """
        r = self._ins.add_r()
        run = Run(r, self)
        if text:
            run.text = text
        if style:
            run.style = style
        return run

    def clear(self):
        """
        Return this same paragraph after removing all its content.
        Paragraph-level formatting, such as style, is preserved.
        """
        self._ins.clear_content()
        return self

    @property
    def runs(self):
        """
        Sequence of |Run| instances corresponding to the <w:r> elements in
        this paragraph.
        """
        return [Run(r, self) for r in self._ins.r_lst]


    @property
    def text(self):
        """
        String formed by concatenating the text of each run in the paragraph.
        Tabs and line breaks in the XML are mapped to ``\\t`` and ``\\n``
        characters respectively.

        Assigning text to this property causes all existing paragraph content
        to be replaced with a single run containing the assigned text.
        A ``\\t`` character in the text is mapped to a ``<w:tab/>`` element
        and each ``\\n`` or ``\\r`` character is mapped to a line break.
        Paragraph-level formatting, such as style, is preserved. All
        run-level formatting, such as bold or italic, is removed.
        """
        text = ''
        for run in self.runs:
            text += run.text
        return text

    @text.setter
    def text(self, text):
        self.clear()
        self.add_run(text)

    @property
    def author(self):
        """
        A member of :ref:`WdTabLeader` specifying a repeating character used
        as a "leader", filling in the space spanned by this tab. Assigning
        |None| produces the same result as assigning `WD_TAB_LEADER.SPACES`.
        Read/write.
        """
        return self._ins.author

    @author.setter
    def author(self, value):
        self._ins.author = value

    @property
    def date(self):
        """
        A member of :ref:`WdTabLeader` specifying a repeating character used
        as a "leader", filling in the space spanned by this tab. Assigning
        |None| produces the same result as assigning `WD_TAB_LEADER.SPACES`.
        Read/write.
        """
        return self._ins.date

    @date.setter
    def date(self, value):
        self._ins.date = value
