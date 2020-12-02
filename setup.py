#!/usr/bin/env python
import setuptools
import sys
import os

assert sys.version_info >= (3, 6, 0), "SnlData requires Python 3.6+"
from pathlib import Path  # noqa E402

CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))  # for setuptools.build_meta


def get_long_description() -> str:
    readme_md = CURRENT_DIR / "README.md"
    with open(readme_md, encoding="utf8") as ld_file:
        return ld_file.read()


USE_MYPYC = False
# To compile with mypyc, a mypyc checkout must be present on the PYTHONPATH
if len(sys.argv) > 1 and sys.argv[1] == "--use-mypyc":
    sys.argv.pop(1)
    USE_MYPYC = True

if USE_MYPYC:
    mypyc_targets = [
        "snldata/client.py",
    ]

    from mypyc.build import mypycify

    opt_level = os.getenv("MYPYC_OPT_LEVEL", "3")
    ext_modules = mypycify(mypyc_targets, opt_level=opt_level)
else:
    ext_modules = []

setuptools.setup(
    name="SnlData",
    version="1.1.0",
    description="A lightweight Python library for Store Norske Leksikon and Lex.dk APIs.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    keywords="API SNL DSD",
    author="DiFronzo",
    author_email="root@vfiles.no",
    url="https://github.com/DiFronzo/SnlData",
    license="GPLv3",
    packages=["snldata"],
    py_modules=["snldata"],
    ext_modules=ext_modules,
    python_requires=">=3.6",
    zip_safe=False,
    install_requires=[
        "requests>=2.22.0",
    ],
    test_suite="tests.test_snldata",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: Norwegian",
        "Natural Language :: Danish",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
