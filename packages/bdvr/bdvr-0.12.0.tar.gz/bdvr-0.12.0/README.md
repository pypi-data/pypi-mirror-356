# bdvr, an Customized Blackduck_Vulnerability_report

# Use case:

Project stakeholders want to know which files are affected with vulnerabilities after a Blackduck HUB scan.

# Drawbacks:

The current blackduck generates multiple reports. To fulfill above requirement once has to refer 2 different reports to really able to trace the source files affected.

# Features

1. Produces customized report where we can see vulnerability, OSS name, affected source path details all in one report
2. Color coded

   low risk = no color

   medium risk = Yellow

   High risk = Red

3. Omits all other files which has no vulnerabilities.

### Prerequiites:

Export your environment variable (in linux)
```sh
export BD_URL="https://www.your_blackduck.com" && export BD_TOKEN="YOUR_API_TOKEN"
```

## How to install

```sh

pip install bdvr
```

## Command to run

```sh


bdvr -h
usage: A program to create vulnerability reports for a given project-version [-h] [-z ZIP_FILE_NAME] [-r REPORTS] [--format {CSV}] [-t TRIES] [-s SLEEP_TIME] [--no-verify]
                                                                             [-o]
                                                                             project_name version_name

positional arguments:
  project_name
  version_name

options:
  -h, --help            show this help message and exit
  -z ZIP_FILE_NAME, --zip_file_name ZIP_FILE_NAME
  -r REPORTS, --reports REPORTS
                        Comma separated list (no spaces) of the reports to generate - ['version', 'scans', 'components', 'vulnerabilities', 'source', 'cryptography',
                        'license_terms', 'component_additional_fields', 'project_version_additional_fields', 'vulnerability_matches', 'upgrade_guidance',
                        'license_conflicts']. Default is all reports.
  --format {CSV}        Report format - only CSV available for now
  -t TRIES, --tries TRIES
                        How many times to retry downloading the report, i.e. wait for the report to be generated
  -s SLEEP_TIME, --sleep_time SLEEP_TIME
                        The amount of time to sleep in-between (re-)tries to download the report
  --no-verify           disable TLS certificate verification
  -o                    (Optional) To automatically open the file

#To automatically open the file add -o option
bdvr BD_PROJECT_NAME BD_PROJECT_VERSION

```

## Dependenceis

```sh

Thanks to all authors. As this library uses below modules
pandas = "^1.4.3"
quo = "^2022.8.2"
universal-startfile = "^0.1.3"

```

## Issues

Please send your bugs to dineshr93@gmail.com

## License

[MIT](LICENSE)
