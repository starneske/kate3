# flake8: noqa
# pylint: skip-file
from setuptools import setup, find_packages

setup(name='kate3',
      version='0.1',
      description='kate3',
      url='http://github.com/Qubeship/kate3',
      author='Hyunji Kim',
      author_email='hyunji@qubeship.io',
      license='MIT',
      packages=find_packages(),
      package_data={'': ['*.ini', '*.json', '*.properties', '*.xml', '*.yaml', '*.yml', '*.config', '*.txt',
                         'templates/*.html',
                         'assets/VERSION',
                         'assets/LICENSE',
                         'assets/README.md',
                         'assets/*.html',
                         'assets/*.js',
                         'assets/*/*.js',
                         'assets/*/*.css',
                         'assets/*/*.gif',
                         'assets/*/*.png',
                         'assets/*/*.ico',
                         'assets/*/*.ttf',
                         ]},
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
