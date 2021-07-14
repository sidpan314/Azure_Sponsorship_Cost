#! /bin/sh

sed -i -e 's/__version__.=.*$/__version__ = "'${VERSION}'"/g' setup.py