from setuptools import setup, find_packages

with open("README.md", 'r', encoding='UTF-8') as fh:
    long_description = fh.read()

setup(
    name="pi_utils",
    version="0.9.2",
    author="dianyao",
    author_email="raiden@dianyao.ai",
    description="pi utils",
    long_description_content_type="text/markdown",
    long_description = long_description,
    packages=find_packages(),
    zip_safe=False,
)