# HyperSimpleDocstring2Md

A Hyper Simple Docstring to Markdown. Creates hierarchically indexed [Markdown](https://en.wikipedia.org/wiki/Markdown) files from Python libraries [docstrings](https://www.python.org/dev/peps/pep-0257/).

# Why?

It is of extreme importance to maintain software documentation up to date with the latest releases.

There are several packages out there to efficiently handle the documentation of Python projects, those can extract updated docstrings and setup a beautiful web pages accordingly. However, a considerable amount of time and effort is required to handle such powerful software tools and keep up to date with the most novel routines and styles.

Yet (in my oppinion), these projects fail to address a specific collective of developers: those that thrive, above all, for extreme simplicity, long-term stability and universality.

# Solution

**Hyper Simple Docstring 2 Markdown** creator intents to be exactly that, _hyper simple_.

It extracts DOCSTRINGs recursively from a given Python package using [pydoc](https://docs.python.org/3.7/library/pydoc.html) and the [inspect module](https://docs.python.org/3/library/inspect.html) and hierarchically organizes them in one indexed Mardown file.

The output Mardown file can be directly used as a GitHub wiki page, for example.

## Which docstrings are covered?

In the current version, DOCSTRINGS from packages (`__init__.py`), modules, classes and functions are extracted.

# How to use it

Only one argument is required, **it's HYPER SIMPLE**:
- the PATH to your Python package

```
python hypersimpledocstring2md.py <PATH TO YOUR LIBRARY>
```

This will recursively read your library and generate a `docs.md` file containing all referred docstrings in an organized manner.

## but there are also additional features

For example:

- you can add a base web url in order to link the index with the Markdown headers, it will result in `<link>#<header>`, very useful for GitHub pages.

```
$ python hypersimpledocstring2md.py -h
usage: hypersimpledocstring2md.py [-h] [--baselink baselink] [--output OUTPUT]
                                  path

Hyper Simple Docstring 2 Markdown - A routine to create a single Markdown
formatted file containing the documentation DOCSTRINGS of a target Python
library.

positional arguments:
  path                 PATH to Library.

optional arguments:
  -h, --help           show this help message and exit
  --baselink baselink  The base Web URL where the .md will be hosted toallow
                       Index-Header linking. Defaults to no link.
  --output OUTPUT      The OUTPUT Markdown file. Defaults to 'docs.md'.
```

## examples

HyperSimpleDocstring2Md is used to generate the Tauren-MD's documentation, [take a look](https://github.com/joaomcteixeira/Tauren-MD/wiki/Modules-Documentation). 

# LICENSE

This software is licensed under the Unlicense as a demonstration of my gratitute for all those skills learned over the years by reading others free tutorials on Internet. Thanks to the community.
