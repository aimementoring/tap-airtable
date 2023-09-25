from setuptools import setup, find_packages

setup(name='tap-airtable',
      version='0.0.3',
      description='Singer.io tap for extracting data from the Airtable API',
      author='hotglue & AIME Mentoring',
      url='https://singer.io',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_airtable'],
      install_requires=[
          'airtable-python==0.1.1',
          'backoff==1.3.2',
          'certifi==2018.11.29',
          'chardet==3.0.4',
          'idna==2.7',
          'jsonschema==2.6.0',
          'pendulum==1.2.0',
          'python-dateutil==2.7.5',
          'pytz==2018.4',
          'pytzdata==2018.7',
          'requests==2.26',
          'simplejson==3.11.1',
          'singer-python==5.4.0',
          'six==1.11.0',
          'tzlocal==1.5.1',
          'urllib3==1.24.2',
      ],
      entry_points='''
          [console_scripts]
          tap-airtable=tap_airtable:main
      ''',
      packages=find_packages(),
      include_package_data=True,
      )
