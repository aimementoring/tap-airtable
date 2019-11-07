# AIME

![AIME](https://d2ylaz7bdw65jx.cloudfront.net/assets/images/aime-logo.svg)

# Tap Airtable

A repository for Singer and Airtable

To make this Tap work with a Target, clone both projects and follow this instructions:

## TAP project (Airtable)

### To install dependencies on tap project run the commands

```shell
python3 -m venv ~/.virtualenvs/tap-airtable
source ~/.virtualenvs/tap-airtable/bin/activate
pip install -e .
```

## Target project (Example: target-postgres) 

### Clone target-postgres project

```shell
 git clone https://github.com/datamill-co/target-postgres
 cd target-postgres
```

### To install dependencies on target project run the commands

```shell
 python3 -m venv ~/.virtualenvs/target-postgres
 source ~/.virtualenvs/target-postgres/bin/activate
 pip install target-postgres
```

### To run full tap and target action run for a particular Base

Complete the config.json 

```
{
    "metadata_url":"https://api.airtable.com/v2/meta/",
    "records_url":"https://api.airtable.com/v0/",
    "token":"airtable-api-key",
    "base_id": "base-id"
}
```

From the home directory of the project 

```shell
python3 run_taps.py | ~/.virtualenvs/target-postgres/bin/target-postgres --config config.json
```
