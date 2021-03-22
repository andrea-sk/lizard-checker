# lizard-checker

Check DIF ouput data in a declarative way using a single cli command.

![](https://github.com/andrea-sk/lizard-checker/blob/master/images/cli.gif)

## Install

Clone this repo and install it using `pip`:

```sh
git clone https://github.com/andrea-sk/lizard-checker.git
cd lizard-checker
pip install .
```

## Usage

```sh
$ dif-checker -h
usage: dif-checker [-h] [--export-json] AVRO_PATH CHECKS_FILE

Run tests on .avro DIF file

positional arguments:
  AVRO_PATH      Path of the folder containing .avro files from DIF pipeline
  CHECKS_FILE    .json file containing checks for feeds in AVRO_PATH

optional arguments:
  -h, --help     show this help message and exit
  --export-json  Export .avro feeds in json format for further checks
```

The `dif-checker` command relies on a folder containing `.avro` files and a `.json` listing checks that will be
performed on each feed.

Checks can be expressed with standard Python notation. Also, in case multiple feed-specific transformation apply
to more than one file, it is possible to use UNIX-style path expansion. In the example above the `*eviction*.avro` will
apply to every file containing the _eviction_ keyword (`us-dcm-user-stream-eviction-2021-03-16.avro` and
`gb-dcm-user-stream-eviction-2021-03-16.avro` in my case).

It is possible to use the `common_checks` block to declare tests that will be applied to **all** feeds in the target folder.

```json
{
  "common_checks": [
    "data['sdpSourceTransport'] == 'KAFKA'",
    "data['sdpSourceOrigin']=='DIF'",
    "data['sdpSourceType']=='Pub/Sub'",
    "data['sdpSourceSystemName']=='DCM'"
  ],
  "feeds": [
    {
      "*eviction*.avro": [
        "data['sdpSubjectId']==data['householdId']",
        "data['sdpSourceTerritory']==data['providerTerritory']",
        "data['sdpSourceProvider']==data['provider']",
        "data['sdpSourceProposition']==data['proposition']",
        "data['sdpSourceEventName']=='USER_EVICTION'"
      ]
    },
    {
      "us-dcm-remove-device-2021-03-16.avro": [
        "data['sdpSourceEventName']=='REMOVE_DEVICE'",
        "data['sdpSourceTerritory']==data['providerTerritory']",
        "data['sdpSourceProvider']==data['provider']",
        "data['sdpSourceProposition']==data['proposition']"
      ]
    },
    {
      "gb-dcm-remove-device-2021-03-16.avro": [
        "data['sdpSourceEventName']=='REMOVE_DEVICE'",
        "data['sdpSourceTerritory']==data['providerTerritory']",
        "data['sdpSourceProvider']==data['provider']",
        "data['sdpSourceProposition']==data['proposition']"
      ]
    }
  ]
}
```

## Contributing

After creating a virtual environment you can install the package in edit-mode via pip:

```sh
pip install -e .
```

The repo relies on `pre-commit` hooks to check for code style compliance and format:

```sh
pip
install -r dev-requirements.txt
pre-commit install
```

Now you're all set up.

### Disclaimer

This package (albeit working fine) is a POC and should go through a round of refactoring to make it
easier to work with/extend in the future.
