#!/usr/bin/env python3
# coding=utf-8
"""
mdtree, convert markdown to html with TOC(table of contents) tree and Mermaid diagram support. https://github.com/ltto/mdtree
"""
import sys, os
import markdown
from mdtree.mdutils import clean_list, parse_title, to_bool, to_unicode, utf8
from mdtree.parser import gen_html, prepare_static_files, parse_static_files, adjust_ext_list

_d_static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

__all__ = ["MdTree", "convert_from_file"]


class MdTree(object):
    """
    Python markdown tree tool with Mermaid diagram support
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:
        """
        self.ext_list = [
            "markdown.extensions.meta",
            "markdown.extensions.attr_list",
            "markdown.extensions.tables",
            "markdown.extensions.toc",
            "markdown.extensions.fenced_code",
            "markdown.extensions.codehilite",
            "markdown_mermaidjs",  # Add Mermaid support
        ]

        self.title = kwargs.get("title", "")
        self._html = ""

        self.js_list = kwargs.get("js", [])
        self.css_list = kwargs.get("css", [])
        self.ext_list.extend(kwargs.get("exts", []))
        self.ext_list = list(set(self.ext_list))

        self.by = "text"
        self.filepath = kwargs.get("filepath", None)
        self.base_dir = kwargs.get("base_dir", None)
        self.to64 = kwargs.get("to64", False)

    def adjust_config(self, meta):
        ext_list = meta.get("exts", [])
        css_list = meta.get("css", [])
        js_list = meta.get("js", [])

        self.ext_list = clean_list(list(set(self.ext_list + ext_list)))
        self.ext_list = adjust_ext_list(self.ext_list, ext_list)

        self.css_list = clean_list(list(set(self.css_list + css_list)))
        self.js_list = clean_list(list(set(self.js_list + js_list)))

        self.base_dir = meta.get("base_dir", [None])[0]
        to64_v_list = clean_list(meta.get("to64", [False]))[0]
        self.to64 = self.to64 or to_bool(to64_v_list)

        if self.by == "file" and not self.base_dir:
            self.base_dir = os.path.split(self.filepath)[0]

        self.title = self.title or meta.get("title", [""])[0]

    def parse_md_config(self, source):
        """
        parse exts config from markdown file and update the markdown object

        exts source: https://python-markdown.github.io/extensions/
        :return:
        """
        md1 = markdown.Markdown(extensions=["markdown.extensions.meta"])
        md1.convert(source)
        md_meta = getattr(md1, "Meta", {})

        # recreate an instance of Markdown object
        md2 = markdown.Markdown(extensions=self.ext_list)
        
        # Note: to64 image conversion is disabled for now due to API changes in newer markdown versions
        # This can be re-implemented using a custom processor if needed
        
        return md2, md_meta

    def convert(self, source):
        """
        convert markdown to html with TOC and Mermaid diagram support
        :param str source: contents of markdown file
        :return:
        """
        source = to_unicode(source)

        # parse meta、exts config
        md, md_meta = self.parse_md_config(source)
        self.adjust_config(md_meta)

        md_html = md.convert(source)
        toc = getattr(md, "toc", "")

        # prepare the basic static files
        css_base, js_base = prepare_static_files()

        # get title from init、meta、markdown source
        title = self.title or parse_title(source)

        # try to get more static files from markdown source
        css_more, js_more = parse_static_files(md_meta, self.css_list, self.js_list)

        params = {
            "title": title,
            "content": md_html,
            "css_base": css_base,
            "js_base": js_base,
            "css_more": css_more,
            "js_more": js_more,
            "toc": toc,
        }

        self._html = gen_html(params)
        # Ensure we return a string, not bytes
        if isinstance(self._html, bytes):
            self._html = self._html.decode('utf-8')
        return self._html

    def convert_file(self, spath):
        """
        convert markdown to html with TOC and Mermaid diagram support
        :param str spath: path of source file
        """
        self.by = "file"
        self.filepath = os.path.expanduser(spath)
        self.base_dir = os.path.split(self.filepath)[0]

        with open(spath, 'r', encoding='utf-8') as f:
            mdstring = f.read()

        return self.convert(mdstring)

    def save_file(self, tpath):
        """
        write to file
        :param str tpath: path of target file
        :return:
        """
        html_content = self._html
        if isinstance(html_content, bytes):
            html_content = html_content.decode('utf-8')
        
        with open(tpath, "w", encoding='utf-8') as f:
            f.write(html_content)
        return tpath


# Exported Funcs
def convert_from_file(**kwargs):
    """
    :param dict kwargs:
    :return:
    """
    source = kwargs["source"] or ""
    target = kwargs.get("target") or ""

    mdtree = MdTree(**kwargs)
    html = mdtree.convert_file(source)
    
    if target:
        mdtree.save_file(target)
    else:
        # For stdout, we need bytes
        html_bytes = utf8(html)
        sys.stdout.buffer.write(html_bytes)
    return html

def main():
    """
    Main entry point for command line interface
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="convert markdown to html with TOC(Table of contents) tree and Mermaid diagram support"
    )
    parser.add_argument("source", default="", help="source file, markdown with optional Mermaid diagrams")
    parser.add_argument("-t", "--target", help="Write output to TARGET. Defaults to STDOUT.")
    parser.add_argument("--css", help="more css, http/s links")
    parser.add_argument("--js", help="more js, http/s links")
    parser.add_argument("--title", help="title")
    parser.add_argument("--to64", action="store_true", help="convert local image to base64? (temporarily disabled)")
    
    args = parser.parse_args()
    
    kwargs = {
        "source": args.source,
        "target": args.target,
        "title": args.title or "",
        "css": [args.css] if args.css else [],
        "js": [args.js] if args.js else [],
        "to64": args.to64,
    }
    
    try:
        convert_from_file(**kwargs)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
