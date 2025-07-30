#!/usr/bin/env python3
# coding=utf-8
import sys
import re
import os
import base64

RE_REMOTEIMG = re.compile('^(http|https):.+')

_meta_data_fence_pattern = re.compile(r'^---[\ \t]*\n', re.MULTILINE)
_meta_data_pattern = re.compile(
    r'^(?:---[\ \t]*\n)?(.*:\s+>\n\s+[\S\s]+?)(?=\n\w+\s*:\s*\w+\n|\Z)|([\S\w]+\s*:(?! >)[ \t]*.*\n?)(?:---[\ \t]*\n)?',
    re.MULTILINE)


def unique_list(alist):
    return list(set(alist))


def clean_list(alist):
    """
    clean items
    :param list alist: a list
    :return:
    """
    alist = list(map(lambda x: str(x).strip(), alist))
    alist = list(filter(lambda x: x != "", alist))
    return unique_list(alist)


def get_first(alist):
    rlist = clean_list(alist) or [None]
    return rlist[0]


def to_bool(value):
    if isinstance(value, (list, tuple)):
        value = value[0]
    value = str(value)
    if value.strip() in [0, None, "None", "False", "", "0"]:
        return False
    return True


# Simplified for Python 3 only
def utf8(value):
    """Converts a string argument to a byte string.

    If the argument is already a byte string or None, it is returned unchanged.
    Otherwise it must be a unicode string and is encoded as utf8.
    """
    if isinstance(value, (bytes, type(None))):
        return value
    if not isinstance(value, str):
        raise TypeError(
            "Expected bytes, unicode, or None; got %r" % type(value)
        )
    return value.encode("utf-8")


def to_unicode(value):
    """Converts a string argument to a unicode string.

    If the argument is already a unicode string or None, it is returned
    unchanged.  Otherwise it must be a byte string and is decoded as utf8.
    """
    if isinstance(value, (str, type(None))):
        return value
    if not isinstance(value, bytes):
        raise TypeError(
            "Expected bytes, unicode, or None; got %r" % type(value)
        )
    return value.decode("utf-8")


def recursive_unicode(obj):
    """Walks a simple data structure, converting byte strings to unicode.

    Supports lists, tuples, and dictionaries.
    """
    if isinstance(obj, dict):
        return dict((recursive_unicode(k), recursive_unicode(v)) for (k, v) in obj.items())
    elif isinstance(obj, list):
        return list(recursive_unicode(i) for i in obj)
    elif isinstance(obj, tuple):
        return tuple(recursive_unicode(i) for i in obj)
    elif isinstance(obj, bytes):
        return to_unicode(obj)
    else:
        return obj


def convert_img_to_b64(src, base_dir=None):
    if RE_REMOTEIMG.match(src):
        return src

    src = os.path.expanduser(src)
    if base_dir:
        base_dir = os.path.expanduser(base_dir)
        src = os.path.join(base_dir, src)

    if not os.path.exists(src):
        raise ValueError("file does not exists on: %s" % src)

    ext = "png"
    if os.path.splitext(src)[1] in [".jpg", "jpeg"]:
        ext = "jpeg"

    with open(src, "rb") as f:
        data = f.read()

    img_data = base64.b64encode(data).decode('utf-8')
    res = "data:image/%s;base64,%s" % (ext, img_data)
    return res


# 简化的图片处理类，不依赖于老版本的ImagePattern
class ImageCheckPattern:
    def __init__(self, base_dir, md_inst=None):
        self.__base_dir = base_dir
        self.md = md_inst

    def handleMatch(self, m, data):
        # 简化的处理，直接处理图片src
        # 这个方法在新版本中可能不会被调用，但保留以兼容性
        pass


def parse_title(mdstring):
    """
    get title
    """

    if mdstring.startswith("---"):
        fence_splits = re.split(_meta_data_fence_pattern, mdstring, maxsplit=2)
        if len(fence_splits) >= 3:
            metadata_content = fence_splits[1]
            match = re.findall(_meta_data_pattern, metadata_content)
            if match:
                mdstring = fence_splits[2]

    mdstring = mdstring.lstrip("\n").lstrip(" ")
    head_pattern1 = re.compile(r'^ *(#{1}) *([^\n\n]+?) *#* *(?:\n+|$)')
    m = re.match(head_pattern1, mdstring)
    if m:
        return m.group(2).strip()

    head_pattern2 = re.compile(r'^ *([^\n]+?) *\n *=+ *(?:\n+|$)')
    m = re.match(head_pattern2, mdstring)
    if m:
        return m.group(1).strip()

    return ""
