from distutils.core import setup

setup(
    name='gnippy',
    version='0.1.2',
    description='Python library for GNIP.',
    author='Abhinav Ajgaonkar',
    author_email='abhinav316@gmail.com',
    packages=['gnippy'],
    url='http://pypi.python.org/pypi/gnippy/',
    license=open('LICENSE.txt').read(),
    long_description=open('README.txt').read(),
    install_requires=[
        "requests == 1.2.0"
    ]
)
