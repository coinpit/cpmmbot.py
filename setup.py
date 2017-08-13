from os.path import join, isfile
from shutil import copyfile

from setuptools import setup

setup(
    name='pymmbot',
    version='0.0.1',
    description='Python marketmaker bot',
    long_description='Coinpit market maker bot with hedging',
    url='https://github.com/githubuser/pymmbot',
    download_url='https://github.com/githubuser/pymmbot/tarball/0.0.1',
    author='coinpit',
    author_email='info@coinpit.io',
    license='MIT',
    keywords=['?'],
    packages=['pymmbot'],
    install_requires=[
        'pytest>=2.9.2',
        'nose==1.3.7',
        'sphinx>=1.4.5',
        'urllib3',
        'socketIO_client',
        'pycparser',
        'pynacl',
        'requests',
        'websocket-client',
        'easydict',
        'sinon',
        'freezegun',
        'future'
    ]
)

if not isfile('settings.py'):
  copyfile(join('pymmbot', 'bot_settings.py'), 'settings.py')
print("\n**** \nImportant!!!\nEdit settings.py before starting the bot.\n****")
