from setuptools import find_packages, setup

__version__ = "0.1.0"

core_reqs = [
    "requests",
]

setup(
    name="relevance_connect",
    version=__version__,
    url="https://relevanceai.com/",
    author="Relevance AI",
    author_email="jacky@relevanceai.com",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    setup_requires=["wheel"],
    install_requires=core_reqs,
    package_data={"": ["*.ini"]},
    extras_require=dict(),
    entry_points={
        'console_scripts': [
            'relevance-connect=relevance_connect.cli:main',
        ],
    },
)