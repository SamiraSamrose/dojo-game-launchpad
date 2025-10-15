# setup.py
from setuptools import setup, find_packages

setup(
    name="dojo-game-launchpad",
    version="1.0.0",
    description="Mobile platform for indie game developers with AI, privacy, and multi-chain payments",
    author="Dojo Game Launchpad Team",
    author_email="team@dojogames.io",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "sqlalchemy>=2.0.23",
        "psycopg2-binary>=2.9.9",
        "pydantic>=2.5.0",
        "openai>=1.3.7",
        "langchain>=0.0.340",
        "chromadb>=0.4.18",
        "starknet-py>=0.18.3",
        "bitcoinlib>=0.6.14",
        "cryptography>=41.0.7",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
            "httpx>=0.25.2",
        ]
    },
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
)
