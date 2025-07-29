from setuptools import setup, find_packages
import os

# Read the PyPI README for the long description
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'PYPI_README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="model-calling",
    version="0.1.0",
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*", "docs", "docs.*"]),
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.23.0",
        "httpx>=0.25.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "examples": [
            "requests>=2.31.0",
            "aiohttp>=3.8.0",
        ]
    },
    author="Wes Jackson",
    author_email="your.email@example.com",  # Update this with your real email
    description="A unified API for calling multiple LLM providers through a consistent, OpenAI-compatible interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="llm, api, ollama, vllm, openai, anthropic, ai, language-model, machine-learning",
    url="https://github.com/yourusername/model-calling",  # Update with your real GitHub URL
    project_urls={
        "Bug Reports": "https://github.com/yourusername/model-calling/issues",
        "Source": "https://github.com/yourusername/model-calling",
        "Documentation": "https://github.com/yourusername/model-calling/tree/main/docs",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "model-calling=model_calling.__main__:main",
        ],
    },
)
