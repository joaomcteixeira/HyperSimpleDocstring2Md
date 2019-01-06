"""
Hyper Simple Docstring 2 Markdown - A routine to create a single 
    Markdown formatted file containing the documentation DOCSTRINGS
    of a target Python library.
"""
import os
import argparse
import importlib.machinery
import pydoc
import inspect
from pathlib import Path


def goto_link(destination, base_link=""):

    return f"[Go to {destination}]({base_link.rstrip('#')}#{destination})  \n"


def check_thereis_func(func_list):
    return len(func_list) > 0

def add_index_entry(path_, descriptor, spacer="  "):
    
    input(type(path_))
    
    
    index = (
        f"{(len(path_.parents) + 1) * spacer}- "
        f"[{descriptor}... {path_.stem}.()]"
        f"({base_link + path_.stem})\n"
        )
    
    return index

def add_body_header(path_):
    return f"{(len(path_.parents) + 1) * '#'} {path_.stem}.()\n"

def add_body_docstring(docstring):
    
    return doc_string_fmt.format(docstring)

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



# for path, dirs, files in os.walk(rootdir):
    
    # if path.endswith(folders_to_ignore):
        # continue
    
    # folders = path[start:].split(os.sep)
    
    # # ignores sunders and dunders
    # if folders[-1].startswith("_"):
        # continue
    
    # # creates an Index entry for the package (folder)
    # index_ += "{}- [{}/]({})\n".format(
        # (len(folders) - 1) * spacer,
        # folders[-1],
        # base_link + folders[-1],
        # )
    
    # # creates an header for the package (folder)
    # # the package DOCSTRING from __init__.py will be written
    # # under this header
    # body_ += "{} {}/\n".format(len(folders) * "#", folders[-1])
    
    # for file_name in sorted(files):
        
        # if not file_name.endswith(".py") \
                # or file_name.startswith("_") and file_name != "__init__.py":
            # continue
        
        # module_path = os.path.abspath(os.path.join(path, file_name))
        
        # foo = importlib.machinery.SourceFileLoader(
            # file_name,
            # module_path,
            # ).load_module()
        
        # module_docstring = \
            # pydoc.plain(pydoc.render_doc(foo)).split("FILE")[0]
        
        
        
        # if file_name == "__init__.py":
            
            # if args.toplink:
                # body_ += goto_link(base_link, "Index")
            
            # body_ += doc_string_fmt.format(module_docstring)
            # continue
        
        # # creates module subindex and subheader
        # else:
            # index_ += "{}- [{}]({})\n".format(
                # (len(folders) + 1) * spacer,
                # file_name,
                # base_link + file_name.translate(
                    # str.maketrans(dict.fromkeys("."))
                    # ),
                # )
            # body_ += "{} {}\n".format(
                # (len(folders) + 1) * "#",
                # file_name,
                # )
            
            # if args.toplink:
                # body_ += goto_link(base_link, "Index")
            
            # # writes the docstring from module
            # body_ += doc_string_fmt.format(module_docstring)
        
        # # inspects if are classes defined in module
        # class_list = inspect.getmembers(foo, inspect.isclass)
        
        # if len(class_list) > 0:
            
            # [add_DOC(class_name, class_, "class") for class_name, class_ in class_list]
        
        # # inspects if are functions defined in module
        # func_list = inspect.getmembers(foo, inspect.isfunction)
        
        # if len(func_list) > 0:
            
            # [add_DOC(func_name, func, "func") for func_name, func in func_list]
        

# with open(args.output, 'w') as docs_:
    # docs_.write(index_)
    # docs_.write(body_)

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

def get_docstring(path_, base_link=""):
    """
    Returns: (Index, Body)
    """
    input(type(path_))
    file_name = path_.name
    
    index_ = add_index_entry(path_, "module")
    body_ = add_body_header(path_)
    body_ += goto_link("Index", base_link=base_link) if args.toplink else ""
    body_ += add_body_docstring(return_module_docstring(path_))
    
    class_list = inspect.getmembers(foo, inspect.isclass)
    
    return (index_, body_)


def build_documentation(path_):
    
    input(path_)
    
    return get_docstring(path_) 


def return_module_docstring(path_):
    module = importlib.machinery.SourceFileLoader("module", os.fspath(path_.resolve())).load_module()
    return pydoc.plain(pydoc.render_doc(module)).split("FILE")[0]

if __name__ == "__main__":
    
    args = get_args()
    
    index_ = "# Index\n"
    body_ = ""
    spacer = "  "
    doc_string_fmt = """
```
{}
```
"""

    base_link = args.baselink + "#"
    rootdir = args.path.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    
    results = [
        build_documentation(Path(folder).joinpath(file_))
            for folder, _, files in os.walk(rootdir) if valid_folder(folder)
            for file_ in sorted(files) if valid_file(file_)
        ]
    
    print(results)
    
    # for path, dirs, files in os.walk(rootdir):
        
        # if path.endswith(folders_to_ignore):
            # continue
    
        # folders = path[start:].split(os.sep)
        
        # # ignores sunders and dunders
        # if folders[-1].startswith("_"):
            # continue
        
        # for file_ in sorted(files):
            
            # if valid_file(file_):
                
                # index, body = get_docstring(
                    # os.path.abspath(os.path.join(path, file_name)),
                    # base_link=base_link
                    # )
                # index_ += index
                # body_ += body
        
    
        #[get_docstring(file_, base_link=base_link) for file_ in sorted(files) if valid_file(file_)]
    
    # with open(args.output, 'w') as docs_:
        # docs_.write(index_)
        # docs_.write(body_)
