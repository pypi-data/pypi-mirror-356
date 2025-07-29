# Contributing

Welcome to `cg635-clock-generator` contributor\'s guide.

This document focuses on getting any potential contributor familiarized
with the development processes, but [other kinds of
contributions](https://opensource.guide/how-to-contribute) are also
appreciated.

If you are new to using [git](https://git-scm.com) or have never
collaborated in a project previously, please have a look at
[contribution-guide.org](https://www.contribution-guide.org/). Other
resources are also listed in the excellent [guide created by
FreeCodeCamp](https://github.com/FreeCodeCamp/how-to-contribute-to-open-source)[^1].

Please notice, all users and contributors are expected to be **open,
considerate, reasonable, and respectful**. When in doubt, [Python
Software Foundation\'s Code of
Conduct](https://www.python.org/psf/conduct/) is a good reference in
terms of behavior guidelines.

## Issue Reports

If you experience bugs or general issues with `cg635-clock-generator`,
please have a look on the [issue
tracker](https://gitlab.desy.de/leandro.lanzieri/cg635-clock-generator/-/issues).
If you don\'t see anything useful there, please feel free to fire an
issue report.

Please don\'t forget to include the closed issues in your search.
Sometimes a solution was already reported, and the problem is considered
**solved**.

New issue reports should include information about your programming
environment (e.g., operating system, Python version) and steps to
reproduce the problem. Please try also to simplify the reproduction
steps to a very minimal example that still illustrates the problem you
are facing. By removing other factors, you help us to identify the root
cause of the issue.

## Documentation Improvements

You can help improve `cg635-clock-generator` docs by making them more
readable and coherent, or by adding missing information and correcting
mistakes.

`cg635-clock-generator` documentation uses
[Sphinx](https://www.sphinx-doc.org/en/master/) as its main
documentation compiler. This means that the docs are kept in the same
repository as the project code, and that any documentation update is
done in the same way was a code contribution.

We are using [CommonMark](https://commonmark.org/) format.

When working on documentation changes in your local machine, you can
compile them using `poe`:

    $ uv run poe docs


and use Python\'s built-in web server for a preview in your web browser
(`http://localhost:8000`):


    $ python3 -m http.server --directory 'docs/_build/html'


## Code Contributions

### Submit an issue

Before you work on any non-trivial code contribution it\'s best to first
create a report in the [issue
tracker](https://gitlab.desy.de/leandro.lanzieri/cg635-clock-generator/-/issues)
to start a discussion on the subject. This often provides additional
considerations and avoids unnecessary work.

### Create an environment

Before you start coding, we recommend creating an isolated [virtual
environment](https://realpython.com/python-virtual-environments-a-primer/)
to avoid any problems with your installed Python packages. This can
easily be done via `venv`:

    $ python3 -m venv <PATH TO VENV>
    $ source <PATH TO VENV>/bin/activate

### Clone the repository

1.  Clone this copy to your local disk:

        $ git clone git@gitlab.desy.de:leandro.lanzieri/cg635-clock-generator.git
        $ cd cg635-clock-generator

2.  You should run:

        $ pip install -U pip setuptools -e .

    to be able to import the package under development in the Python
    REPL.

3.  Install `pre-commit`\_:

        $ pip install pre-commit
        $ pre-commit install

    `cg635-clock-generator` comes with a lot of hooks configured to
    automatically help the developer to check the code being written.

### Implement your changes

1.  Create a branch to hold your changes (for this you need an account on
    gitlab.desy.de and developer rights):

        $ git checkout -b my-feature

    and start making changes. Never work on the main branch!

2.  Start your work on this branch. Don\'t forget to add
    [docstrings](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)
    to new functions, modules and classes, especially if they are part
    of public APIs.

3.  Add yourself to the list of contributors in `AUTHORS.md`.

4.  When you're done editing, record your changes in [git](https://git-scm.com) by running:

        $ git add <MODIFIED FILES>
        $ git commit

    Please make sure to see the validation messages from `pre-commit`\_
    and fix any eventual issues. This should automatically use
    [flake8](https://flake8.pycqa.org/en/stable/)/[black](https://pypi.org/project/black/)
    to check/fix the code style in a way that is compatible with the
    project.

    **Important**: Don\'t forget to add unit tests and documentation in case your
    contribution adds an additional feature and is not just a bugfix.

    Moreover, writing a [descriptive commit
    message](https://chris.beams.io/posts/git-commit) is highly
    recommended. In case of doubt, you can check the commit history
    with:

        $ git log --graph --decorate --pretty=oneline --abbrev-commit --all

    to look for recurring communication patterns.


5.  Please check that your changes don\'t break any unit tests with:

        $ uv run poe test

    (after having installed `uv`\_ with `pip install uv` or `pipx`).

    You can also use `poe`\_ to run several other pre-configured tasks
    in the repository. Try `uv run poe` to see a list of the available
    checks.

### Submit your contribution

1.  If everything works fine, push your local branch to GitHub with:

        $ git push -u origin my-feature


2.  Go to the web page of your fork and click \"Create merge request\" to
    send your changes for review.

### Troubleshooting

The following tips can be used when facing problems to build or test the
package:

1.  Make sure to fetch all the tags from the upstream
    [repository](https://gitlab.desy.de/leandro.lanzieri/cg635-clock-generator).
    The command `git describe --abbrev=0 --tags` should return the
    version you are expecting. If you are trying to run CI scripts in a
    fork repository, make sure to push all the tags. You can also try to
    remove all the egg files or the complete egg folder, i.e., `.eggs`,
    as well as the `*.egg-info` folders in the `src` folder or
    potentially in the root of your project.


[^1]: Even though, these resources focus on open source projects and
    communities, the general ideas behind collaborating with other
    developers to collectively create software are general and can be
    applied to all sorts of environments, including private companies
    and proprietary code bases.
