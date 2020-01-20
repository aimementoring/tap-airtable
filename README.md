![AIME](https://d2ylaz7bdw65jx.cloudfront.net/assets/images/aime-logo.svg)

# Tap Airtable

[Singer](https://www.singer.io/) tap that extracts data from a [MySQL](https://www.mysql.com/) database and produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md).

To make this Tap work with a Target, clone both projects and follow this instructions:

## Usage

This section dives into basic usage of `tap-mysql` by walking through extracting
data from a table. It assumes that you can connect to and read from a MySQL
database.

### Install

```bash
python3 -m venv ~/.virtualenvs/tap-airtable
source ~/.virtualenvs/tap-airtable/bin/activate
pip install -e .
```


### Create the configuration file


| Configuration Key   | Description                                                                                              |
|---------------------|----------------------------------------------------------------------------------------------------------|
| metadata_url        | Airtable metadata URL, at the time of the update: "https://api.airtable.com/v2/meta/"                    |
| records_url         | Airtable content URL, at the time of the update: "https://api.airtable.com/v0/"                          |
| token               | Airtable Token                                                                                           |
| base_id             | Airtable base ID to export                                                                               |
| selected_by_default | Default for every table in the base. If set to true, all of the tables in the schema will be syncronized |
| remove_emojis       | Filter out emojis from the scyncronization                                                               |


#### Configuration file example


```json
{
    "metadata_url":"https://api.airtable.com/v2/meta/",
    "records_url":"https://api.airtable.com/v0/",
    "token":"airtable_token",
    "base_id": "airtable_base_id",
    "selected_by_default": true,
    "remove_emojis": false
}
```


### Discovery mode

The tap can be invoked in discovery mode to find the available tables and
columns in the database:

```bash
$ tap-airtable --config config.json --discover

```

A discovered catalog is output, with a JSON-schema description of each table. A
source table directly corresponds to a Singer stream.

The `selected-by-default` fields is used to enable the sync of the tables. If set to 'true', all of the tables will be 
selected in the `properties.json` 



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
    "base_id": "base-id",
    "selected_by_default": true
}
```

From the home directory of the project 

```shell
tap-airtable -c config.json --properties properties.json | ~/.virtualenvs/target-postgres/bin/target-postgres 
```
