"""
AvaTax Software Development Kit for Python.

   Copyright 2022 Avalara, Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

   Avalara Shipping Verification only
   API for evaluating transactions against direct-to-consumer Beverage Alcohol shipping regulations.
   This API is currently in beta.
"""

from setuptools import setup, find_namespace_packages 

NAME = "Avalara.SDK"
VERSION = "25.6.0"

REQUIRES = [
    "urllib3 >= 1.25.3",
    "python-dateutil",
    "pydantic",
    "setuptools >= 21.0.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="Avalara Unified SDK",
    author="Jonathan Wenger",
    author_email="jonathan.wenger@avalara.com",
    url="",
    keywords=["OpenAPI", "OpenAPI-Generator", "Avalara Unified SDK"],
    python_requires=">=3.6",
    install_requires=REQUIRES,
    # Use find_namespace_packages to pick up directories without __init__.py
    packages=find_namespace_packages(include=["Avalara.*"], exclude=["test", "tests"]),
    include_package_data=True,
    long_description="""\
    SDK for Avalara Services for client use.   # noqa: E501
    """
)