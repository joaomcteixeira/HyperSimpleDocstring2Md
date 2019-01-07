"""
docstring goes here
"""
import os
import sys
import argparse
import importlib.machinery
import inspect
import pydoc
from pathlib import Path


def get_args():
    ap = argparse.ArgumentParser(description=__doc__)
    
    ap.add_argument(
        "path",
        metavar="path",
        type=str,
        help="PATH to Library.",
        )
    
    ap.add_argument(
        "--baselink",
        metavar="baselink",
        type=str,
        default="",
        help=(
            "The base Web URL where the .md will be hosted to"
            "allow Index-Header linking. Defaults to no link."
            ),
        )
    
    ap.add_argument(
        "--toplink",
        metavar="toplink",
        type=str,
        default=True,
        help=(
            "Adds a quick link to the Index bellow each header."
            " Defaults to True."
            ),
        )
    
    ap.add_argument(
        "--output",
        default="docs.md",
        help="The OUTPUT Markdown file. Defaults to 'docs.md'.",
        )
    
    return ap.parse_args()


def valid_folder(path_):
    """
    Returns True if path_.match any of the conditions. False otherwise.
    
    conditions assigned:
        - "_*"
    """
    
    # ignores dunders, __pycache__
    conditions = (
        "_*",
        )
    
    p = Path(path_)
    
    return not(any(p.match(condition) for condition in conditions))


def valid_file(file_name):
    """
    Returns True if file_name matches the condition assigned.
    False otherwise.
    """
    
    condition = (
        file_name.endswith(".py")
        or not(file_name.startswith("_") and file_name != "__init__.py")
        )
    
    return condition


def load_module(path_):
    """
    Loads module from Path object.
    
    Returns the module
    """
    module = importlib.machinery.SourceFileLoader(
        path_.stem,
        os.fspath(path_.resolve())
        )
    
    return module.load_module()


def goto_link(base_link, where):
    
    return f"[Go to {where}]({base_link.rstrip('#')}#{where})\n"


def add_index(title, descriptor="", base_link="", spacer=0):
    
    to_strip = ('()')
    to_translate = str.maketrans(dict.fromkeys("."))
    
    index = (
        f"{spacer * '  '}- "
        f"[{descriptor}... {title}]"
        f"({base_link + title.rstrip(to_strip).translate(to_translate)})\n"
        )
    
    return index


def add_header(title, spacer=1):
    """
    Adds Markdown header based on module_path (pathlib.Path object).
    Defines subheaders based on Path.parents
    
    Path("package/subpackage/module.py")
    
    ## module.py
    
    """
    
    return f"{spacer * '#'} {title}\n"


def read_docstring(object_):
    """
    Returns object docstring without the FILE information.
    """
    
    fmt = "```\n{}\n```\n"
    
    docs = pydoc.plain(pydoc.render_doc(object_)).split("FILE")[0].rstrip()
    
    return fmt.format(docs)


def gen_index_doc(
        title,
        object_,
        spacer=1,
        base_link="",
        descriptor="",
        toplink=False,
        ):
    
    index = add_index(
        title,
        spacer=spacer,
        base_link=base_link,
        descriptor=descriptor,
        )
    
    doc = add_header(
        title,
        spacer=spacer + 1,
        )
    
    doc += goto_link(base_link, "Index") if toplink else ""
    
    doc += read_docstring(object_)
    
    return index, doc


def get_index_doc(preds, base_link="", toplink=False):
    
    list_of_index_doc_tuples = [
        gen_index_doc(
            p[0] + "()",
            p[1],
            spacer=spcr,
            base_link=base_link,
            descriptor=dscrptr,
            toplink=toplink,
            )
        for dscrptr, spcr, pred in preds
        for p in pred if not(p[0].startswith("_"))
        ] + [("", "")]
    return list_of_index_doc_tuples


def get_documentation(
        module_abs_path,
        spacer=1,
        base_link="",
        toplink=True,
        ):
    
    module = load_module(module_abs_path)
    
    if module_abs_path.name == "__init__.py":
        title = module_abs_path.parent.name
        descriptor = "package"
    
    else:
        title = module_abs_path.name
        descriptor = "module"
        spacer += 1
    
    index, documentation = gen_index_doc(
        title,
        module,
        spacer=spacer - 1,
        base_link=base_link,
        descriptor=descriptor,
        toplink=toplink,
        )
    
    predictors = [
        ("class", spacer, inspect.getmembers(module, inspect.isclass)),
        ("func", spacer, inspect.getmembers(module, inspect.isfunction)),
        ]
    
    are_pred = list(filter(lambda x: bool(x[-1]), predictors))
    
    index_, doc_ = list(zip(
        *get_index_doc(are_pred, base_link=base_link, toplink=toplink)
        )) if any(are_pred) else ([""], [""])
    
    index += "".join(index_)
    documentation += "".join(doc_)
    
    return index, documentation


if __name__ == "__main__":
    
    args = get_args()
    
    base_link = args.baselink + "#"
    toplink = args.toplink
    rootdir = Path(args.path).resolve()
    rootlib = rootdir.name
    
    sys.path.append(os.fspath(rootdir.parent))
    
    lib_docs = [
        get_documentation(
            Path(folder).joinpath(file_),
            spacer=len(Path(folder[folder.find(rootlib):]).parents),
            base_link=base_link,
            toplink=toplink,
            )
        for folder, _, files in os.walk(rootdir) if valid_folder(folder)
        for file_ in sorted(files) if valid_file(file_)
        ]
    
    index, docs = list(zip(*lib_docs))
        
    with open(args.output, 'w') as output:
        output.write("".join(index))
        output.write("".join(docs))
    
    print(f"* Saved: {args.output}")
