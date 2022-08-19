# encoding: utf-8

from __future__ import absolute_import, division, print_function

import xml.etree.ElementTree as ET

from .constants import MIME_TYPE
from .image import BaseImageHeader
from ..shared import Inches, Length, Mm, Cm, Emu


class Svg(BaseImageHeader):
    """
    Image header parser for SVG images.
    """

    @classmethod
    def from_stream(cls, stream):
        """
        Return |Svg| instance having header properties parsed from SVG image
        in *stream*.
        """
        px_width, px_height = cls._dimensions_from_stream(stream)
        return cls(px_width, px_height, 72, 72)

    @property
    def content_type(self):
        """
        MIME content type for this image, unconditionally `image/svg+xml` for
        SVG images.
        """
        return MIME_TYPE.SVG

    @property
    def default_ext(self):
        """
        Default filename extension, always 'svg' for SVG images.
        """
        return "svg"

    @classmethod
    def _dimensions_from_stream(cls, stream):
        stream.seek(0)
        data = stream.read()
        root = ET.fromstring(data)
        # FIXME: The width could be expressed as '4cm'
        # See https://www.w3.org/TR/SVG11/struct.html#NewDocument
        width_str = root.attrib["width"]
        height_str = root.attrib["height"]
        if width_str.endswith(r'%') and height_str.endswith(r'%'): #%
            vb_lims = str(root.attrib["viewBox"]).split(' ')
            width_scale = float(width_str[:-1]) * 0.01 * 72/96
            height_scale = float(height_str[:-1]) * 0.01 * 72/96
            width = int(width_scale * float(vb_lims[2]))
            height = int(height_scale * float(vb_lims[3]))
        elif width_str.endswith('pt') and height_str.endswith('pt'): #pt
            width = int(float(width_str[:-2]))
            height = int(float(height_str[:-2]))
        elif width_str.endswith('in') and height_str.endswith('in'): #in
            width = int(Inches(float(width_str[:-2])).pt)
            height = int(Inches(float(height_str[:-2])).pt)
        elif width_str.endswith('px') and height_str.endswith('px'): #px
            width = int(width_str[:-2])
            height = int(height_str[:-2])
        elif width_str.endswith('mm') and height_str.endswith('mm'): #mm
            width = int(Mm(float(width_str[:-2])).pt)
            height = int(Mm(float(height_str[:-2])).pt)
        elif width_str.endswith('cm') and height_str.endswith('cm'): #cm
            width = int(Cm(float(width_str[:-2])).pt)
            height = int(Cm(float(height_str[:-2])).pt)
        elif width_str.endswith('em') and height_str.endswith('em'): #emus
            width = int(Emu(float(width_str[:-2])).pt)
            height = int(Emu(float(height_str[:-2])).pt)
        else: # pixels
            width = int(width_str)
            height = int(height_str)

        return width, height
