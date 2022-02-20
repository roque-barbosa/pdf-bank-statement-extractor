import setuptools

setuptools.setup(
    name="bank_crawlers",
    version="0.0.1",
    packages=setuptools.find_packages(),
    install_requires=(
        "click==8.0.1",
        "numpy==1.21.2",
        "pandas==1.3.3",
        "python-dateutil==2.8.2",
        "pytz==2021.1",
        "urllib3==1.26.7",
        "python-decouple==3.4",
        "requests==2.26.0",
        "logzero==1.7.0",
    ),
    entry_points={
        "console_scripts": [
            "bank = cli.core:cli",
        ]
    },
)