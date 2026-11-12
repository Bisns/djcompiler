
DjCompiler
==========

DjCompiler is a python package that compiles the django project to a C language project which gives more performance and more security since the original code is hidden.

Compatibility
-------------

* Python:

  - 3.8
  - 3.9
  - 3.10
  - 3.11
  - 3.12
  - 3.13

Installation
------------

``pip install djcython``

Usage
-----
* run ``djcompiler help`` to see available commands.
* run ``djcompiler compile`` to compile the django project.
* run ``djcompiler buildfile`` to generate a config file.
* run ``djcompiler buildpy`` to generate a python script that compiles the project when run.

Configuration
-------------

Lists in ``.djcompiler`` accept space-separated values on one line or indented
continuation lines. Both formats can be mixed::

    project_name=MyProject
    other_files_needed=
        manage.py
        .env
        myapp/models.py
    other_dirs_needed=
        static
        templates
    ignored_files=manage.py models.py
    ignored_dirs=venv build

Blank lines and full-line ``#`` comments are allowed. The four list options are
``other_files_needed``, ``other_dirs_needed``, ``ignored_files`` and
``ignored_dirs``. Each value is separated by whitespace; paths containing spaces
are not supported. An empty list option produces an empty list.

Future Features
===============
