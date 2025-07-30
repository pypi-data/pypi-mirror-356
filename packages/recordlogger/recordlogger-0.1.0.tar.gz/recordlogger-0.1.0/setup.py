from setuptools import setup, find_packages

setup(
    name='recordlogger',  # Must be unique on PyPI!
    version='0.1.0',
    author='souhardya',
    author_email='dandapatsouhardya2004@gmail.com',
    description='A simple logging utility for recording variable info.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'inspect',
        'os'  # Add any other dependencies your package needs
    ],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
