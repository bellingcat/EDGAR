from setuptools import find_packages, setup

def read_requirements(filename: str):
    with open(filename, encoding="utf8") as requirements_file:
        import re

        def fix_url_dependencies(req: str) -> str:
            """Pip and setuptools disagree about how URL dependencies should be handled."""
            m = re.match(
                r"^(git\+)?(https|ssh)://(git@)?github\.com/([\w-]+)/(?P<name>[\w-]+)\.git", req
            )
            if m is None:
                return req
            else:
                return f"{m.group('name')} @ {req}"

        requirements = []
        for line in requirements_file:
            line = line.strip()
            if line.startswith("#") or len(line) <= 0:
                continue
            requirements.append(fix_url_dependencies(line))
    return requirements

VERSION = {}  # type: ignore
with open("edgar_tool/version.py", "r") as version_file:
    exec(version_file.read(), VERSION)

setup(
    name="edgar-tool",
    version=VERSION["VERSION"],
    description="Retrieve corporate and financial data from the SEC  - python API or command line tool.",
    long_description=open("README.md", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Topic :: Office/Business :: Financial",
    ],
    keywords=["scraper", "edgar", "finance", "sec"],
    project_urls={
        "Code": "https://github.com/bellingcat/EDGAR",
    },
    author="Bellingcat",
    author_email="contact-tech@bellingcat.com",
    license="GNU General Public License v3 (GPLv3)",
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"],
    ),
    package_data={"edgar_tool": ["py.typed"]},
    install_requires=read_requirements("requirements.txt"),
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "edgar-tool=edgar_tool.__main__:main",
        ],
    },
)