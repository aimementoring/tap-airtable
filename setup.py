from setuptools import setup

setup(name='tap-airtable',
      version='0.0.1',
      description='Singer.io tap for extracting data from the Airtable API',
      author='AIME Mentorinng',
      url='https://singer.io',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['services', 'utils'],
      install_requires=[
          'backoff==1.3.2',
          'certifi==2018.11.29',
          'chardet==3.0.4',
          'idna==2.7',
          'jsonschema==2.6.0',
          'pendulum==1.2.0',
          'python-dateutil==2.7.5',
          'pytz==2018.4',
          'pytzdata==2018.7',
          'requests==2.20.1',
          'simplejson==3.11.1',
          'singer-python==5.4.0',
          'six==1.11.0',
          'tzlocal==1.5.1',
          'urllib3==1.24.1'
      ],
      entry_points='''
          [console_scripts]
          tap_airtable=run_taps.py
      ''',
      # packages=['tap_airtable', 'run_taps.py'],
      # package_data = {
      #     'tap_salesforce/schemas': [
      #         # add schema.json filenames here
      #     ]
      # },
      include_package_data=True,
      )
