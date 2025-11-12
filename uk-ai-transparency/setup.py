from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="uk-ai-transparency",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="UK Government AI Decision Transparency Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    install_requires=[
        "pandas>=2.1.0",
        "streamlit>=1.28.0",
        "plotly>=5.17.0",
        "numpy>=1.24.0",
    ],
    entry_points={
        'console_scripts': [
            'uk-ai-dashboard=src.transparency_dashboard:main',
        ],
    },
)
