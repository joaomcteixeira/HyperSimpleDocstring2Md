# HyperSimpleDocstring2Md

A Hyper Simple Docstring to Markdown. Creates hierarchically indexed [Markdown](https://en.wikipedia.org/wiki/Markdown) files from [Python](https://www.python.org/) libraries' [docstrings](https://www.python.org/dev/peps/pep-0257/).

# Why?

It is extremely important to maintain software documentation up to date with the latest releases.

There are many packages out there to efficiently handle the documentation of Python projects, those can extract updated docstrings and setup beautiful web pages accordingly. But, such complex tools require a considerable amount of time and effort to master, and developers should thrive to keep up to date with the most novel routines and styles of documentation representation.

Moreover, in my opinion, these projects fail to address a specific collective of developers: those who thrive, above all, for extreme simplicity, long-term stability and universality of their output, in this case software documentation.

# Solution

**Hyper Simple Docstring 2 Markdown** creator was designed to recursively extract DOCSTRINGS from a target Python package and write them to a simple yet organized and indexed Markdown formatted file. It intents to be exactly that, **hyper simple** in both input and output.

The output Mardown file can be directly used as a GitHub wiki page, for example.

## Implementation

It uses Python +3.7 standard libraries, such as [pydoc](https://docs.python.org/3.7/library/pydoc.html) and the [inspect module](https://docs.python.org/3/library/inspect.html).

## Which docstrings are covered?

In the current version, DOCSTRINGS from packages (`__init__.py`), modules, classes and functions are extracted.

# How to use it

No installation is required and you only need to pass **one** argument, **it's HYPER SIMPLE**:
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

This software is licensed under the [Unlicense](https://github.com/joaomcteixeira/HyperSimpleDocstring2Md/blob/master/LICENSE) as a demonstration of my gratitute to the whole Python community that cheerily and altruistically share knowledge on the Web. Thanks to the community.
