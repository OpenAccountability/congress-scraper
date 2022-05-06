from setuptools import setup

from congress.version import version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="congress-scraper",
    packages=["congress"],
    version=version(),
    description="Congress Scraper - A tool to scrape https://congress.gov for information",
    author="Nicholas M. Synovic",
    author_email="nicholas.synovic@gmail.com",
    # license="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ssl.cs.luc.edu/projects/metricsDashboard",
    # project_urls={
    #     "Bug Tracker": "https://github.com/SoftwareSystemsLaboratory/ssl-metrics-git-commits-loc/issues",
    #     "GitHub Repository": "https://github.com/SoftwareSystemsLaboratory/ssl-metrics-git-commits-loc",
    # },
    # keywords=[
    #     "bus factor",
    #     "commits",
    #     "engineering",
    #     "git",
    #     "github",
    #     "issue density",
    #     "issues",
    #     "kloc",
    #     "loyola",
    #     "loyola university chicago",
    #     "luc",
    #     "mining",
    #     "metrics",
    #     "repository",
    #     "repository mining",
    #     "simple",
    #     "software",
    #     "software engineering",
    #     "software metrics",
    #     "software systems laboratory",
    #     "ssl",
    # ],
    # classifiers=[
    #     "Development Status :: 4 - Beta",
    #     "Intended Audience :: Science/Research",
    #     "Intended Audience :: Developers",
    #     "License :: OSI Approved :: BSD License",
    #     "Programming Language :: Python",
    #     "Programming Language :: Python :: 3",
    #     "Programming Language :: Python :: 3.9",
    #     "Programming Language :: Python :: 3 :: Only",
    #     "Topic :: Software Development",
    #     "Topic :: Scientific/Engineering",
    #     "Operating System :: POSIX",
    #     "Operating System :: Unix",
    #     "Operating System :: MacOS",
    # ],
    python_requires=">=3.10",
    install_requires=[
        "bs4",
        "lxml",
        "pandas",
        "progress",
        "requests",
        # "matplotlib",
        # "numpy",
        # "pandas",
        # "progress",
        # "python-dateutil",
        # "scikit-learn",
    ],
    entry_points={
        "console_scripts": [
            "cs-members = congress.members:main",
        ]
    },
)
