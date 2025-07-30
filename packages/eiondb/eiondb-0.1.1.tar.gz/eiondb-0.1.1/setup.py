from setuptools import setup, find_packages

setup(
    name="eiondb",
    version="0.1.1",
    description="Python SDK for Eion - Shared memory storage for AI agent systems",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Eion Team",
    author_email="contact@eion.ai",
    url="https://github.com/eion/eion-sdk-python",
    license="AGPL-3.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["LICENSE.md"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "pydantic>=2.5.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
        ],
    },
) 