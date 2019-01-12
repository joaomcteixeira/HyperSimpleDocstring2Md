"""
Hyper Simple Docstring 2 Markdown - A routine to create a single
    Markdown formatted file containing the documentation DOCSTRINGS
    of a target Python library. Fully based on Python standard library.
"""
import os
import sys
import argparse
import itertools as it
import importlib.machinery
import inspect
import pydoc
from pathlib import Path

_descriptors = [
    "class",
    "method",
    "function",
    ]


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
        and not(file_name.startswith("_")) or file_name == "__init__.py"
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
    
    # 6 is the Markdown subheader limit
    # 5 and not 6 because of spacer + 1 in gen_index_doc
    if spacer >= 5:
        spacer = 5
    
    doc = add_header(
        title,
        spacer=spacer + 1,
        )
    
    doc += goto_link(base_link, "Index") if toplink else ""
    
    doc += read_docstring(object_)
    
    return index, doc

    
def gen(name_, object_, doc_list, spacer=1, **kwargs):
    """
    Recursive function.
    """
    
    spacer += 1
    
    doc_list.append(gen_index_doc(name_, object_, spacer=spacer, **kwargs))
    
    _ = list(
        filter(
            lambda x: not(x[0].startswith("_")),
            inspect.getmembers(object_)
            ),
        ) or [("1", "2")]
    
    for name_, obj_ in _:
        
        whatis = [
            inspect.isclass(obj_),
            inspect.ismethod(obj_),
            inspect.isfunction(obj_),
            ]
        
        if any(whatis):
            gen(
                name_,
                obj_,
                doc_list,
                spacer=spacer,
                **{
                    **kwargs,
                    "descriptor": list(it.compress(_descriptors, whatis))[0],
                    },
                )
    else:
        return doc_list


def get_documentation(
        module_abs_path,
        spacer=1,
        base_link="",
        toplink=True,
        index="",
        documentation="",
        ):
    
    module = load_module(module_abs_path)
    
    if module_abs_path.name == "__init__.py":
        title = module_abs_path.parent.name
        descriptor = "package"
        spacer = spacer - 1
    
    else:
        title = module_abs_path.name
        descriptor = "module"
        spacer = spacer
    
    index_, doc_ = list(
        zip(
            *gen(
                title,
                module,
                [],
                spacer=spacer,
                base_link=base_link,
                toplink=toplink,
                descriptor=descriptor,
                )
            )
        )
    
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
            spacer=len(Path(folder[folder.find(rootlib):]).parents) - 1,
            base_link=base_link,
            toplink=toplink,
            )
        for folder, _, files in os.walk(rootdir) if valid_folder(folder)
        for file_ in sorted(files) if valid_file(file_)
        ]
    
    index, docs = list(zip(*lib_docs))
    
    with open(args.output, 'w') as output:
        output.write("# Index\n" + "".join(index))
        output.write("".join(docs))
    
    print(f"* Saved: {args.output}")
