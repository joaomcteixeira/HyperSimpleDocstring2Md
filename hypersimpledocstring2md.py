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
    "--output",
    default="docs.md",
    help="The OUTPUT Markdown file. Defaults to 'docs.md'.",
    )

args = ap.parse_args()

index_ = ""
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

folders_to_ignore = (
    "__pycache__",
    )

for path, dirs, files in os.walk(rootdir):
    
    if path.endswith(folders_to_ignore):
        continue
    
    folders = path[start:].split(os.sep)
    
    # ignores sunders and dunders
    if folders[-1].startswith("_"):
        continue
    
    # creates an Index entry for the package (folder)
    index_ += "{}- [{}/]({})\n".format(
        (len(folders) - 1) * spacer,
        folders[-1],
        base_link + folders[-1],
        )
    
    # creates an header for the package (folder)
    # the package DOCSTRING from __init__.py will be written
    # under this header
    body_ += "{} {}/\n".format(len(folders) * "#", folders[-1])
    
    for file_name in sorted(files):
        
        if not file_name.endswith(".py") \
                or file_name.startswith("_") and file_name != "__init__.py":
            continue
        
        module_path = os.path.abspath(os.path.join(path, file_name))
        
        foo = importlib.machinery.SourceFileLoader(
            file_name,
            module_path,
            ).load_module()
        
        module_docstring = \
            pydoc.plain(pydoc.render_doc(foo)).split("FILE")[0]
        
        if file_name == "__init__.py":
            body_ += doc_string_fmt.format(module_docstring)
            continue
        
        # creates module subindex and subheader
        else:
            index_ += "{}- [{}]({})\n".format(
                (len(folders) + 1) * spacer,
                file_name,
                base_link + file_name,
                )
            body_ += "{} {}\n".format(
                (len(folders) + 1) * "#",
                file_name,
                )
            
            # writes the docstring from module
            body_ += doc_string_fmt.format(module_docstring)
        
        # inspects if are classes defined in module
        class_list = inspect.getmembers(foo, inspect.isclass)
        
        if len(class_list) > 0:
            
            for class_name, class_ in class_list:
                
                class_doc = pydoc.plain(pydoc.render_doc(class_))
                
                index_ += "{}- [class {}.()]({})\n".format(
                    (len(folders) + 2) * spacer,
                    class_name,
                    base_link + class_name,
                    )
                
                body_ += "{} class {}.()\n".format(
                    (len(folders) + 2) * "#",
                    class_name,
                    )
                
                body_ += doc_string_fmt.format(class_doc)
        
        # inspects if are functions defined in module
        func_list = inspect.getmembers(foo, inspect.isfunction)
        
        if len(func_list) > 0:
            
            for func_name, func in func_list:
                
                funcdoc = pydoc.plain(pydoc.render_doc(func))
                
                index_ += "{}- [func {}.()]({})\n".format(
                    (len(folders) + 2) * spacer,
                    func_name,
                    base_link + func_name,
                    )
                body_ += "{} func {}.()\n".format(
                    (len(folders) + 2) * "#",
                    func_name,
                    )
                
                body_ += doc_string_fmt.format(funcdoc)
        

with open(args.output, 'w') as docs_:
    docs_.write(index_)
    docs_.write(body_)
