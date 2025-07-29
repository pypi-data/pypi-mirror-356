from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r', encoding='utf-8') as fh:
    install_requires = fh.read().splitlines()

setup(
    name='outeai',
    version='1.0.0',
    packages=find_packages(),
    install_requires=install_requires,
    author='OuteAI',
    description='OuteAI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/edwko/OuteAI',
    package_data={
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
