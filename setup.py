try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Asynchronous python wrapper to Bose SoundTouch API',
    'author': 'Wagner Sartori Junior',
    'url': 'https://github.com/trunet/aiobosest',
    'download_url': 'https://github.com/trunet/aiobosest',
    'author_email': 'wsartori@wsartori.com',
    'version': '0.0.3',
    'install_requires': ['aiohttp>=1.1.4', 'lxml>=3.6.4', 'zeroconf>=0.17.6'],
    'setup_requires': ['pytest-runner', 'sphinx'],
    'tests_require': ['pytest-asyncio', 'pytest-pep8', 'pytest'],
    'packages': ['aiobosest', 'aiobosest.helpers'],
    'license': 'GPLv3',
    'scripts': [],
    'name': 'aiobosest',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.5',
        'Topic :: Home Automation',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
}

setup(**config)
