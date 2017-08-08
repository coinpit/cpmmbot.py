from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='pymmbot',
    version='0.0.1',
    description='Python marketmaker bot',
    long_description=readme(),
    url='https://github.com/githubuser/pymmbot',
    download_url='https://github.com/githubuser/pymmbot/tarball/0.0.1',
    author='coinpit',
    author_email='info@coinpit.io',
    license='GPLv3',
    keywords=['?'],
    packages=['pymmbot'],
    install_requires=[
        'pytest>=2.9.2',
        'nose==1.3.7',
        'sphinx>=1.4.5',
        'urllib3',
        'socketIO_client',
        'pynacl',
        'requests',
        'websocket-client',
        'easydict',
        'sinon',
        'freezegun'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)
