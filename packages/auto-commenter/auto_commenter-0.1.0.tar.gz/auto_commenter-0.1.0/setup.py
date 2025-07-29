from setuptools import setup, find_packages

setup(
    name='auto-commenter',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',  # Add other dependencies here
        'pandas',
    ],
    author='veganapa',
    author_email='varmadinesh249@gmail.com',
    description='A Python package for automatically generating docstrings based on function arguments and return types.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Dinesh123527/auto-commenter',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
