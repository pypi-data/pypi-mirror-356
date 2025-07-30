from setuptools import setup, find_packages
import os

# Read the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="prediction-metrics-backtester",
    version="0.1.0",
    author="Nathaniel William Huff",
    author_email="nathanielwilliam117@gmail.com",
    description="A flexible backtesting framework for evaluating trading strategies based on prediction metrics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nawihu/prediction-metrics-backtester",
    project_urls={
        "Bug Reports": "https://github.com/nawihu/prediction-metrics-backtester/issues",
        "Source": "https://github.com/nawihu/prediction-metrics-backtester",
        "Documentation": "https://github.com/nawihu/prediction-metrics-backtester/wiki",
    },
    # Instead of find_packages(), explicitly specify the module
    py_modules=["prediction_metrics_backtesting"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
    ],
    entry_points={
        "console_scripts": [
            "prediction-metrics-backtest=prediction_metrics_backtesting:main",
        ],
    },
    keywords="backtesting trading finance prediction metrics strategy",
    include_package_data=True,
    zip_safe=False,
)
