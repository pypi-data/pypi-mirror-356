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

tests_require = [
    'zope.app.wsgi[test]',
    'zope.configuration',
    'zope.testbrowser',
    'zope.testing',
]

setup(
    name='grokcore.formlib',
    version='5.0',
    author='Grok Team',
    author_email='zope-dev@zope.dev',
    url='https://github.com/zopefoundation/grokcore.formlib',
    download_url='https://pypi.org/project/grokcore.formlib',
    description='Grok-like configuration for zope.formlib components',
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
    install_requires=[
        'setuptools',
        'grokcore.component >= 2.1',
        'grokcore.content >= 1.2',
        'grokcore.security >= 1.5',
        'grokcore.view >= 2.0',
        'martian >= 0.13',
        'pytz',
        'zope.container',
        'zope.event',
        'zope.formlib >= 4.3.0',
        'zope.interface',
        'zope.lifecycleevent',
        'zope.publisher',
        'zope.schema',
    ],
    extras_require={'test': tests_require},
)
