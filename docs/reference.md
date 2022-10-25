# Resources

* Update the Documents
```bash
cd docs
make html
```

* How to run the autodoc setup
```bash
cd docs
sphinx-apidoc -o source ../servicepytan
```

## Documenting Python Packages in Sphinx Tutorial 
https://brendanhasz.github.io/2019/01/05/sphinx.html#autodoc-extension

## Guide to Documenting with Sphinx
https://betterprogramming.pub/auto-documenting-a-python-project-using-sphinx-8878f9ddc6e9

## MyST Parser Docs
https://myst-parser.readthedocs.io/en/latest/sphinx/intro.html#

## Google Style Guide
https://google.github.io/styleguide/pyguide.html

## AutoDoc Reference
https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#module-sphinx.ext.napoleon

# Publishing to PyPi
https://realpython.com/pypi-publish-python-package/
```bash
# Building the Package Files
python setup.py sdist bdist_wheel
# If error: may need pip install wheel

# Testing the Build
twine upload -r testpypi dist/*

# Live Publishing
twine upload dist/*
```