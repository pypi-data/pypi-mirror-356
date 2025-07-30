# pybloomfilter3

[pybloomfilter3](https://github.com/cavoq/pybloomfiltermmap3) is a maintained fork of [pybloomfiltermmap3](https://github.com/prashnts/pybloomfiltermmap3) by [@prashnts](https://github.com/prashnts).

The goal of `pybloomfilter3` is simple: to provide a fast, simple, scalable, correct library for Bloom filters in Python.

[![Build Status](https://travis-ci.org/cavoq/pybloomfiltermmap3.svg?branch=master)](https://travis-ci.org/cavoq/pybloomfiltermmap3)
[![PyPI](https://img.shields.io/pypi/v/pybloomfilter3.svg)](https://pypi.python.org/pypi/pybloomfilter3)
[![PyPI](https://img.shields.io/pypi/dw/pybloomfilter3.svg)](https://pypi.python.org/pypi/pybloomfilter3)
[![PyPI](https://img.shields.io/pypi/pyversions/pybloomfilter3.svg)](https://pypi.python.org/pypi/pybloomfilter3)

## Why pybloomfilter3?

There are a couple reasons to use this module:

- It natively uses [mmapped files](http://en.wikipedia.org/wiki/Mmap).
- It is fast (see [benchmarks](http://axiak.github.io/pybloomfiltermmap/#benchmarks)).
- It natively does the set things you want a Bloom filter to do.

## Quickstart

After you install, the interface to use is a cross between a file
interface and an ste interface. As an example:

```python
    >>> import pybloomfilter
    >>> fruit = pybloomfilter.BloomFilter(100000, 0.1, '/tmp/words.bloom')
    >>> fruit.update(('apple', 'pear', 'orange', 'apple'))
    >>> len(fruit)
    3
    >>> 'mike' in fruit
    False
    >>> 'apple' in fruit
    True
```

To create an in-memory filter, simply omit the file location:

```python
    >>> fruit = pybloomfilter.BloomFilter(10000, 0.1)
    >>> fruit.add('apple')
    >>> 'apple' in fruit
    True
```

These in-memory filters can be pickled and reloaded:

```python
    >>> import pickle
    >>> pickled_fruit = pickle.dumps(fruit)
    >>> unpickled_fruit = pickle.loads(pickled_fruit)
    >>> 'apple' in unpickled_fruit
    True
```

_Caveat_: it is currently not possible to persist this filter later as an mmap file.

## Docs

Current docs are available at [pybloomfiltermmap3.rtfd.io](https://pybloomfiltermmap3.readthedocs.io/en/latest).

## Install

To install:

```bash
pip install pybloomfilter3
```

and you should be set.

## History and Future

[pybloomfiltermmap](https://github.com/axiak/pybloomfiltermmap) is an excellent Bloom filter implementation for Python 2 by [@axiak](https://github.com/axiak) and contributors. I, [@prashnts](https://github.com/prashnts), made initial changes to add support for Python 3 sometime in 2016 as the current [pybloomfiltermmap3](https://pypi.org/project/pybloomfiltermmap3/) on `PyPI`. Since then, with the help of contributors, there have been incremental improvements and bug fixes while maintaining the API from versions `0.4.x` and below.
[@cavoq](https://github.com/cavoq) forked pybloomfiltermmap3 in 2025 to continue development and maintenance of the library to ensure it remains compatible with the latest Python versions ([pybloomfilter3](https://pypi.org/project/pybloomfiltermmap3/) on `PyPI`).

Some new features and changes were first introduced in version `0.5.0`. From this point on, the goal is to reach stability, as well as add a few more APIs to expand upon the use cases. While we can't guarantee that we won't change the current interface, the transition from versions `0.4.x` and below should be quick one liners. Please open an issue if we broke your build!

Suggestions, bug reports, and / or patches are welcome!

## Contributions and development

When contributing, you should set up an appropriate Python 3 environment and install the dependencies listed in `requirements-dev.txt`.
Package installation depends on a generated `pybloomfilter.c` file, which requires Cython module to be in your current environment.

### Environment setup

```bash
# Creates a virtual env called "env"
python -m venv env

# Activates the created virtual env
source env/bin/activate
```

### Dependencies

```bash
python -m pip install --upgrade pip
pip install cython
```

### Build

```bash
python -m build
```

### Test

```bash
python -m unittest discover -s tests -p "*.py"
```

### Publish

```bash
python -m pip install --upgrade twine
python -m twine upload dist/*.tar.gz
```

## Maintainers

- [David Stromberger](https://github.com/cavoq)
- [Prashant Sinha](https://github.com/prashnts)
- [Vytautas Mizgiris](https://github.com/vmizg)

## License

See the LICENSE file. It's under the MIT License.
