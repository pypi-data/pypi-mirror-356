from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="adeptiv-ai-evaluator-sdk",
    version="1.1.2",
    author="Adeptiv-AI",
    author_email="contact@adeptiv-ai.com",
    description="A powerful async SDK for evaluating LLM outputs with conversation support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.18.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
    keywords="llm evaluation ai machine-learning async",
    # project_urls={
    #     "Bug Reports": "https://github.com/adeptiv-ai/evaluator-sdk/issues",
    #     "Documentation": "https://docs.adeptiv-ai.com/sdk",
    #     "Source": "https://github.com/adeptiv-ai/evaluator-sdk",
    # },
)