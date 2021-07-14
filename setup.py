from setuptools import setup, find_packages

__version__ = "1.2.3"

setup(
    name="canalyzer",
    version=__version__,
    author="Jose Truyol",
    author_email="jose.truyol@indimin.com",
    description=(
        "Azure subscription monthly price analyzer. Ideal for a Sponsorship account"
    ),
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points="""
        [console_scripts]
        canalyzer=canalyzer.analyzer.__main__:analyze
        markdown_to_html=canalyzer.markdown_to_html.__main__:main
        canalyzer_smtp=canalyzer.smtp.__main__:main
    """,
)
