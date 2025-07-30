from setuptools import setup, find_packages

setup(
    name='contextguard',
    version='0.1.0',
    description='Context-aware decorator to prevent repeated API retries using Redis.',
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
