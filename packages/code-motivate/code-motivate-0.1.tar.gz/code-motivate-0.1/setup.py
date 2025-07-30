from setuptools import setup, find_packages

setup(
    name="code-motivate",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'code-motivate=motivate.__main__:main',
        ],
    },
    author="Your Name",
    description="A CLI tool that prints motivational quotes for coders",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
)
