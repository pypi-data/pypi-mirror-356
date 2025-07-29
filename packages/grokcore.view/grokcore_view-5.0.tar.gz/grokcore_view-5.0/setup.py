import os

from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


long_description = (
    read('README.rst')
    + '\n' +
    read('CHANGES.rst')
)

install_requires = [
    'grokcore.component >= 2.5',
    'grokcore.security',
    'martian >= 1.5',
    'setuptools',
    'zope.browserpage',
    'zope.browserresource >= 3.9',
    'zope.component',
    'zope.contentprovider',
    'zope.interface',
    'zope.pagetemplate',
    'zope.ptresource >= 3.9',
    'zope.publisher',
    'zope.security',
    'zope.traversing',
]

tests_require = [
    'zope.app.appsetup',
    'zope.app.publication',
    'zope.app.wsgi[test]',
    'zope.configuration',
    'zope.container',
    'zope.login',
    'zope.password',
    'zope.principalregistry',
    'zope.securitypolicy',
    'zope.site',
    'zope.testbrowser',
    'zope.testing',
]

publication_require = [
    'zope.app.publication'
]

setup(
    name='grokcore.view',
    version='5.0',
    author='Grok Team',
    author_email='zope-dev@zope.dev',
    url='https://github.com/zopefoundation/grokcore.view',
    download_url='https://pypi.org/project/grokcore.view/',
    description='Grok-like configuration for Zope browser pages',
    long_description=long_description,
    license='ZPL',
    classifiers=[
        'Development Status :: 6 - Mature',
        'Environment :: Web Environment',
        'Framework :: Zope :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.9',
    install_requires=install_requires,
    extras_require={
        'test': tests_require,
        'security_publication': publication_require
    },
)
