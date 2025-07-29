from setuptools import setup, find_packages

setup(
    name="gemini-library",
    version="1.0.0",
    author="Test",
    author_email="test.email@example.com",
    description="Gemini API response handler with Markdown to HTML conversion",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="",  # or leave blank
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
        "markdown",
        "beautifulsoup4"
    ],
    python_requires='>=3.7',
)
