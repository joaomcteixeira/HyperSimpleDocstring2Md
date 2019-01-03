"""
Hyper Simple Docstring 2 Markdown - A routine to create a Markdown formatted
    file containing the documentation DOCSTRINGS of a target library.
"""
import pydoc
import os
import importlib.machinery
import argparse
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
        "allow Index linking."
        ),
    )

ap.add_argument(
    "--output",
    default="docs.md",
    help="The OUTPUT Markdown file.",
    )

args = ap.parse_args()

index_ = ""
body_ = ""
spacer = "  "
doc_string_ = """
```
{}
```

"""

base_link = args.baselink + "#"
rootdir = args.path.rstrip(os.sep)
start = rootdir.rfind(os.sep) + 1

for path, dirs, files in os.walk(rootdir):
    
    if path.endswith("__pycache__"):
        continue
    
    folders = path[start:].split(os.sep)
    
    if folders[-1].startswith("_"):
        continue
    
    index_ += "{}- [{}/]({})\n".format(
        (len(folders) - 1) * spacer,
        folders[-1],
        base_link + folders[-1],
        )
    
    body_ += "{} {}/\n".format(len(folders) * "#", folders[-1])
    
    for file_ in sorted(files):
        
        if not file_.endswith(".py") \
                or file_ != "__init__.py" and file_.startswith("_"):
            continue
        
        file_base_name = file_.split(".")[0]
        
        module_path = os.path.abspath(os.path.join(path, file_))
        
        foo = importlib.machinery.SourceFileLoader(
            file_base_name,
            module_path,
            ).load_module()
        
        module_docstring = \
            pydoc.plain(pydoc.render_doc(foo)).split("FUNCTIONS")[0]
        
        if file_ == "__init__.py":
            body_ += doc_string_.format(module_docstring)
            continue
        
        else:
            index_ += "{}- [{}]({})\n".format(
                (len(folders) + 1) * spacer,
                file_base_name,
                base_link + file_base_name,
                )
            body_ += "{} {}\n\n".format(
                (len(folders) + 1) * "#",
                file_base_name,
                )
            body_ += doc_string_.format(module_docstring)
        
        func_list = inspect.getmembers(foo, inspect.isfunction)
        
        if len(func_list) > 0:
            
            for func_name, func in func_list:
                
                funcdoc = pydoc.plain(pydoc.render_doc(func))
                index_ += "{}- [{}.()]({})\n".format(
                    (len(folders) + 2) * spacer,
                    func_name,
                    base_link + func_name,
                    )
                body_ += "{} {}.()\n\n".format(
                    (len(folders) + 2) * "#",
                    func_name,
                    )
                
                body_ += doc_string_.format(funcdoc)
        

with open(args.output, 'w') as docs_:
    docs_.write(index_)
    docs_.write(body_)
