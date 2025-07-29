qgispluginreleaser
==========================================

Add-on for zest.releaser for releasing QGIS plugins.

Zest.releaser can be extended, see its `entrypoints documentation
<http://zestreleaser.readthedocs.org/en/latest/entrypoints.html>`_.

What we do:

- We hook into the "release" step and create a zipfile with a version number
  and copy it to the current directory. You can scp it to a server afterwards.

- In the "prerelease" and "postrelease" steps we change the version number in
  the (mandatory) QGIS ``metadata.txt`` file.

Note: a QGIS plugin doesn't have a ``setup.py``, so you'll need to add a
``version.txt`` or ``version.rst`` or ``VERSION`` file so that zest.releaser
recognizes the current directory as a releasable project and so that it can
find the version number somewhere. Simply put the version number ("1.2") by
itself on the first line. A newline at the end is fine.


Installation
------------

You'll have to install it globally (or in a custom virtualenv) as qgis plugins
normally don't have a full python setup.

The plugin checks whether there's a ``metadata.txt`` (lowercase) with a
``qgisMinimumVersion`` string inside it. If found, the plugin runs. Otherwise
it stays out of the way. So it should be safe to install globally.


Development of the plugin
-------------------------

Use ``uv`` for installing the project in development. Some commands::

    $ uv run pytest
    $ pre-commit run --all
