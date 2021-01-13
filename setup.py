"""setuptools.py"""

import setuptools # type: ignore

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mdtools",
    version="0.0.1",
    author="Yaroslav Pidstryhach",
    description="Tools for markdown wikis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="todo",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'mdlinkcheck=mdtools.linkcheck:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'colorama',
        'numpy',
        'marko'
    ],
    python_requires='>=3.6',
)
