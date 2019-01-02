# HyperSimpleDocstring2Md

A Hyper Simple Docstring to Markdown. Creates indexed Markdown files from Python libraries docstrings.

# Why?

There are several packages out there that efficiently take care of the documentation of Python package, those can extract updated docstrings and setup a beautiful web page accordingly. However, a considerable amount of time and effort is required to handle such powerful softwares and keep up to date with the most novel routines.

Yet (in my oppinion), these projects fail to address a specific developers collective: those that thrive, above all, for extreme simplicity, long-term stability and universality.

# Solution

Because I failed to found a solution out there in the _wild_ Internet, I developed **Hyper Simple Docstring 2 Markdown".

This software extracts all DOCSTRINGs from a given Python package using [pydoc](https://docs.python.org/3.7/library/pydoc.html) and hierarchically organizes them in an indexed Mardown file.

The output Mardown file can be directly used as a GitHub wiki page, for example.

# How to use it

Only two arguments are required, it's HYPER SIMPLE:
- the PATH to your Python package
- a base web url to that the index can be linked to the Markdown headers, it will results in `<link>#<header>`

```
$ python hypersimpledocstring2md.py -h

usage: hypersimpledocstring2md.py [-h] [--output OUTPUT] path baselink

Hyper Simple Docstring 2 Markdown - A routine to create a Markdown formatted file
containing the documentation DOCSTRINGS of a target library.

positional arguments:
  path             PATH to Library.
  baselink         The base Web URL where the .md will be hosted toallow Index
                   linking.

optional arguments:
  -h, --help       show this help message and exit
  --output OUTPUT  The OUTPUT Markdown file.
```

# LICENSE

Enjoy!
