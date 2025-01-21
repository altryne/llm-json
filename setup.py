from setuptools import setup

setup(
    name="llm-json",
    version="0.1.0",
    packages=["llm_json"],
    install_requires=[],
    description="A JSON library wrapper that gracefully handles markdown-wrapped JSON from LLMs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/altryne/llm-json",
    author="Alex Volkov",
    author_email="alex@alexw.me",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    extras_require={
        'dev': [
            'pytest>=7.0',
        ],
    },
)