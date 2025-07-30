# -*- coding: utf-8 -*-
import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fobj:
    requires = [x.strip() for x in fobj.readlines() if x.strip()]

setup(
    name="django-site-warnings",
    version="0.4.1",
    description="记录站点告警信息，提供告警确认等管理功能。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Zhang YiLei",
    maintainer="Zhang YiLei",
    license="Mulan PSL v2",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=[
        "django extentions",
    ],
    install_requires=requires,
    packages=find_packages(
        ".",
        exclude=[
            "django_site_warnings_server",
            "django_site_warnings_example",
            "django_site_warnings_example.migrations",
        ],
    ),
    zip_safe=False,
    include_package_data=True,
)
