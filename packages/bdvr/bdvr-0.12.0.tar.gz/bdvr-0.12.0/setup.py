# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bdvr']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.3,<2.0.0', 'universal-startfile>=0.1.3,<0.2.0']

entry_points = \
{'console_scripts': ['bdvr = bdvr:main']}

setup_kwargs = {
    'name': 'bdvr',
    'version': '0.12.0',
    'description': "customized report generated from set of blackduck reports that gives 'color coded vulnerabilities', and 'source paths' including 'direct' and 'indirect dependencies' details all in one report",
    'long_description': '# bdvr, an Customized Blackduck_Vulnerability_report\n\n# Use case:\n\nProject stakeholders want to know which files are affected with vulnerabilities after a Blackduck HUB scan.\n\n# Drawbacks:\n\nThe current blackduck generates multiple reports. To fulfill above requirement once has to refer 2 different reports to really able to trace the source files affected.\n\n# Features\n\n1. Produces customized report where we can see vulnerability, OSS name, affected source path details all in one report\n2. Color coded\n\n   low risk = no color\n\n   medium risk = Yellow\n\n   High risk = Red\n\n3. Omits all other files which has no vulnerabilities.\n\n### Prerequiites:\n\nExport your environment variable (in linux)\n```sh\nexport BD_URL="https://www.your_blackduck.com" && export BD_TOKEN="YOUR_API_TOKEN"\n```\n\n## How to install\n\n```sh\n\npip install bdvr\n```\n\n## Command to run\n\n```sh\n\n\nbdvr -h\nusage: A program to create vulnerability reports for a given project-version [-h] [-z ZIP_FILE_NAME] [-r REPORTS] [--format {CSV}] [-t TRIES] [-s SLEEP_TIME] [--no-verify]\n                                                                             [-o]\n                                                                             project_name version_name\n\npositional arguments:\n  project_name\n  version_name\n\noptions:\n  -h, --help            show this help message and exit\n  -z ZIP_FILE_NAME, --zip_file_name ZIP_FILE_NAME\n  -r REPORTS, --reports REPORTS\n                        Comma separated list (no spaces) of the reports to generate - [\'version\', \'scans\', \'components\', \'vulnerabilities\', \'source\', \'cryptography\',\n                        \'license_terms\', \'component_additional_fields\', \'project_version_additional_fields\', \'vulnerability_matches\', \'upgrade_guidance\',\n                        \'license_conflicts\']. Default is all reports.\n  --format {CSV}        Report format - only CSV available for now\n  -t TRIES, --tries TRIES\n                        How many times to retry downloading the report, i.e. wait for the report to be generated\n  -s SLEEP_TIME, --sleep_time SLEEP_TIME\n                        The amount of time to sleep in-between (re-)tries to download the report\n  --no-verify           disable TLS certificate verification\n  -o                    (Optional) To automatically open the file\n\n#To automatically open the file add -o option\nbdvr BD_PROJECT_NAME BD_PROJECT_VERSION\n\n```\n\n## Dependenceis\n\n```sh\n\nThanks to all authors. As this library uses below modules\npandas = "^1.4.3"\nquo = "^2022.8.2"\nuniversal-startfile = "^0.1.3"\n\n```\n\n## Issues\n\nPlease send your bugs to dineshr93@gmail.com\n\n## License\n\n[MIT](LICENSE)\n',
    'author': 'dineshr93gmail.com',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
