from setuptools import setup

try:
  from pypandoc import convert
  readme = lambda f: convert(f, 'rst')
except:#(IOError, ImportError)
  read_md = lambda f: open(f, 'r').read()

setup(
    name='onemap',
    version='0.2.2.post2',
    author='Ruiwen Chua',
    author_email='ruiwen@thoughtmonkeys.com',
    packages=['onemap'],
    url='https://github.com/ruiwen/onemap',
    license='LICENSE.txt',
    description='Wrapper for the OneMapSG API',
    #long_description=readme,
    keywords=['onemap', 'onemapsg'],
    install_requires=[
        "requests >= 1.2.3"
    ]
)
