"""Minimal setup.py for compatibility with tools that require it."""

from setuptools import setup

# Workaround for license-file metadata issue
setup(
    license_files = []
)
