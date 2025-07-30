from setuptools import setup, find_packages
from pathlib import Path

# Read from README.md
this_directory = Path(__file__).parent
long_description = Path("README.md").read_text(encoding="utf-8")

setup(
    name='contextguard',
    version='0.1.1',
    description='Context-aware decorator to prevent repeated API retries using Redis.',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Important!
    author='Yerram Mahendra Reddy',
    author_email='yerram.mahi@gmail.com',
    packages=find_packages(),
    install_requires=['redis'],
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
