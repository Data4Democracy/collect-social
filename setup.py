from setuptools import setup, find_packages

setup(name='collect_social',
      packages=find_packages(),
      zip_safe=False,
      license='MIT',
      install_requires=['facepy',
'dataset',
'tweepy',
'pytest==3.0.6',
'coverage',
'pytest-cov==2.4.0']
      )
