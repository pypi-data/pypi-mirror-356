from setuptools import setup, find_packages

setup(
    name='randomlite',
    version='0.0.1',
    packages=find_packages(),
    author='sanjay',
    author_email='vksanjay28@gmail.com',
    description='Generate random integers, floats, and lists easily',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/randomgen',  # Optional GitHub link
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
