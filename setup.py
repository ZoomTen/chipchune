# /usr/bin/env python

import os
from setuptools import setup


def get_version():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "__meta__",
        os.path.join(os.path.dirname("__file__"), "chipchune", "__init__.py"),
    )
    meta = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(meta)
    return meta.__version__


setup(
    name="chipchune",
    version=get_version(),
    url="https://github.com/zoomten/chipchune",
    description="Library to manipulate various chiptune tracker formats.",
    author="Zumi Daxuya",
    author_email="daxuya.zumi+chipchune@proton.me",
    packages=["chipchune.furnace", "chipchune.famitracker", "chipchune.deflemask"],
    license="MIT",
    python_requires=">=3.8",
    extras_require={"testing": ["coverage", "pytest", "mypy"]},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio :: Editors",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
    ],
)
