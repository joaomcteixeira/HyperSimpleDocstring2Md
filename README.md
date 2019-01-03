# HyperSimpleDocstring2Md

A Hyper Simple Docstring to Markdown. Creates indexed Markdown files from Python libraries docstrings.

# Why?

There are several packages out there to efficiently handle the documentation of Python projects, those can extract updated docstrings and setup a beautiful web pages accordingly. However, a considerable amount of time and effort is required to handle such powerful software tools and keep up to date with the most novel routines.

Yet (in my oppinion), these projects fail to address a specific collective developers: those that thrive, above all, for extreme simplicity, long-term stability and universality.

# Solution

Because I failed to found a solution out there in the _wild_ Internet, I developed **Hyper Simple Docstring 2 Markdown" creator.

This software extracts DOCSTRINGs from a given Python package using [pydoc](https://docs.python.org/3.7/library/pydoc.html) and the [inspect module](https://docs.python.org/3/library/inspect.html) and hierarchically organizes them in an indexed Mardown file.

The output Mardown file can be directly used as a GitHub wiki page, for example.

## Which docstrings are covered?

So far, hierarchical docstrings index is created for packages (`__init__.py`), modules, classes and functions.

# How to use it

Only one argument is required, it's HYPER SIMPLE:
- the PATH to your Python package

```
python hypersimpledocstring2md.py <PATH TO YOUR LIBRARY>
```

This will generate a `docs.md` file that can be directly used to create a GitHub wiki page, for example.

## but there are also additional features

For example:

- you can add a base web url in order to link the index with the Markdown headers, it will result in `<link>#<header>`

```
$ python hypersimpledocstring2md.py -h

python hypersimpledocstring2md.py -h
usage: hypersimpledocstring2md.py [-h] [--baselink baselink] [--output OUTPUT]
                                  path

Hyper Simple Docstring 2 Markdown - A routine to create a Markdown formatted
file containing the documentation DOCSTRINGS of a target library.

positional arguments:
  path                 PATH to Library.

optional arguments:
  -h, --help           show this help message and exit
  --baselink baselink  The base Web URL where the .md will be hosted toallow
                       Index linking.
  --output OUTPUT      The OUTPUT Markdown file.

```

# LICENSE

Enjoy!
