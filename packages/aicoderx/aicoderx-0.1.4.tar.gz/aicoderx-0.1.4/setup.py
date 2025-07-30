from setuptools import setup, find_packages

setup(
    name="aicoderx",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "transformers",
        "torch",
        "tqdm",  # if used in spinner
    ],
    author="Jay Kilaparthi",
    author_email="jayakeerthk@gmail.com",
    description="Generate executable Python code from natural language prompts using an LLM.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jayyvk/ai-coder",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
