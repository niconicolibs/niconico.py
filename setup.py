# niconico.py - setup

from setuptools import setup
from os.path import exists


NAME = "niconico.py"
DESCRIPTION = "ニコニコスクレイピングライブラリ"


if exists("README.md"):
    with open("README.md", "r") as f:
        long_description = f.read()
else:
    long_description = DESCRIPTION


with open(f"{NAME[:-3]}/__init__.py", "r") as f:
    text = f.read()
    version = text.split('__version__ = "')[1].split('"')[0]
    author = text.split('__author__ = "')[1].split('"')[0]


setup(
    name=NAME,
    version=version,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f'https://github.com/tasuren/{NAME}',
    project_urls={
        "Documentation": f"https://{NAME.replace('.', '-')}.readthedocs.io/"
    },
    entry_points={
        "console_scripts": [
            "niconico = niconico.__main__:main"
        ]
    },
    author=author,
    author_email='tasuren@aol.com',
    license='MIT',
    keywords='video download niconico ニコニコ動画',
    packages=["niconico", "niconico.objects"],
    install_requires=["requests", "bs4"],
    python_requires='>=3.8.0',
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Typing :: Typed'
    ]
)