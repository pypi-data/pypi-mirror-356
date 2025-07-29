__version__ = "0.12.0"
import os
from os.path import isfile, join, exists
import pandas
import argparse
import shutil
from pathlib import Path
import sys
import logging
import time
from startfile import startfile
# from blackduck.HubRestApi import HubInstance
from blackduck import Client

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] {%(module)s:%(lineno)d} %(levelname)s - %(message)s"
)
class FailedReportDownload(Exception):
	pass
def list_files_recursive(directory):
    file_paths = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            file_paths.append(full_path)
    return file_paths
version_name_map = {
	'version': 'VERSION',
	'scans': 'CODE_LOCATIONS',
	'components': 'COMPONENTS',
	'vulnerabilities': 'SECURITY',
	'source':'FILES',
	'cryptography': 'CRYPTO_ALGORITHMS',
	'license_terms': 'LICENSE_TERM_FULFILLMENT',
	'component_additional_fields': 'BOM_COMPONENT_CUSTOM_FIELDS',
	'project_version_additional_fields': 'PROJECT_VERSION_CUSTOM_FIELDS',
	'vulnerability_matches': 'VULNERABILITY_MATCH',
	'upgrade_guidance': 'UPGRADE_GUIDANCE',
	'license_conflicts': 'LICENSE_CONFLICTS'
}

all_reports = list(version_name_map.keys())
def empty_directory(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove file or symlink
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove directory and its contents
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def main():



    parser = argparse.ArgumentParser("A program to create vulnerability reports for a given project-version")
    parser.add_argument("project_name")
    parser.add_argument("version_name")
    parser.add_argument("-z", "--zip_file_name", default="reports.zip")
    parser.add_argument('--format', default='CSV', choices=["CSV"], help="Report format - only CSV available for now")
    parser.add_argument('-t', '--tries', default=30, type=int, help="How many times to retry downloading the report, i.e. wait for the report to be generated")
    parser.add_argument('-s', '--sleep_time', default=10, type=int, help="The amount of time to sleep in-between (re-)tries to download the report")
    parser.add_argument('--no-verify', dest='verify', action='store_false', help="disable TLS certificate verification")
    parser.add_argument(
            "-o", action="store_true", help="(Optional) To automatically open the file"
        )

    args = parser.parse_args()
        # Get environment variables
    bd_url = os.getenv("BD_URL").strip()
    bd_token = os.getenv("BD_TOKEN").strip()

    # Check if either is empty or None
    if not bd_url or not bd_token:
        print("Error: BD_URL or BD_TOKEN environment variable is not set or is empty.")
        sys.exit(1)

    def download_report(bd_client, location, filename, retries=args.tries):
        report_id = location.split("/")[-1]
        base_url = bd_client.base_url if bd_client.base_url.endswith("/") else bd_client.base_url + "/"
        download_url = f"{base_url}api/reports/{report_id}"

        logging.info(f"Retrieving report list for {location}")

        if retries:
            response = bd_client.session.get(location)
            report_status = response.json().get('status', 'Not Ready')
            if response.status_code == 200 and report_status == 'COMPLETED':
                response = bd.session.get(download_url, headers={'Content-Type': 'application/zip', 'Accept':'application/zip'})
                if response.status_code == 200:
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    logging.info(f"Successfully downloaded zip file to {filename} for report {report_id}")
                else:
                    logging.error("Failed to download report")
            else:	
                retries -= 1
                logging.debug(f"Failed to retrieve report {report_id}, report status: {report_status}")
                logging.debug(f"Will retry {retries} more times. Sleeping for {args.sleep_time} second(s)")
                time.sleep(args.sleep_time)
                download_report(bd_client, location, filename, retries)
        else:
            raise FailedReportDownload(f"Failed to retrieve report {report_id} after multiple retries")


    bd = Client(base_url=bd_url, token=bd_token, verify=args.verify)

    params = {
        'q': [f"name:{args.project_name}"]
    }
    projects = [p for p in bd.get_resource('projects', params=params) if p['name'] == args.project_name]
    assert len(projects) == 1, f"There should be one, and only one project named {args.project_name}. We found {len(projects)}"
    project = projects[0]

    params = {
        'q': [f"versionName:{args.version_name}"]
    }
    versions = [v for v in bd.get_resource('versions', project, params=params) if v['versionName'] == args.version_name]
    assert len(versions) == 1, f"There should be one, and only one version named {args.version_name}. We found {len(versions)}"
    version = versions[0]

    logging.debug(f"Found {project['name']}:{version['versionName']}")

    reports_l = ['source','vulnerabilities']
    reports_l = [version_name_map[r.lower()] for r in reports_l]

    post_data = {
            'reportFormat': "CSV",
            'locale' : "en_US",
            'versionId': version['_meta']['href'].split("/")[-1],
            'categories': reports_l,
            "includeSubprojects" : True
    }
    version_reports_url = bd.list_resources(version).get('versionReport')
    assert version_reports_url, "Ruh-roh, a version should always have a versionReport resource under it"

    r = bd.session.post(version_reports_url, json=post_data)
    r.raise_for_status()
    location = r.headers.get('Location')
    assert location, "Hmm, this does not make sense. If we successfully created a report then there needs to be a location where we can get it from"

    logging.debug(f"Created version details report for project {args.project_name}, version {args.version_name} at location {location}")
    download_report(bd, location, args.zip_file_name)
    bdreportszip = args.zip_file_name
    open_file = args.o
    print(f"{bdreportszip=}")

    help_text = 'Go to Your Blackduck Project > Generate "Create Version detail report" > checkboxes "Source" and "Vulnerabilities" should be checked and Generate the report.'

    if not exists(bdreportszip):
        print("File not exists", bdreportszip)
        sys.exit()
    if not isfile(bdreportszip):
        print(
            "Its a directory. Please give a zip file output of blackduck",
            bdreportszip,
            err=True,
        )
        print(help_text)
        sys.exit()
    if ".zip" not in bdreportszip:
        print("Its not a zip file", bdreportszip)
        sys.exit()
    full_file_path = Path(bdreportszip).absolute()
    this_dir = Path(full_file_path).parent.__str__()
    filelocation = ""

    if "\\" in bdreportszip or "/" in bdreportszip:
        filelocation = (
            bdreportszip.rsplit("\\", 1)[0]
            if len(bdreportszip.rsplit("\\", 1)[0]) > 0
            else bdreportszip.rsplit("/", 1)[0]
        )
        filename = (
            bdreportszip.rsplit("\\", 1)[1]
            if len(bdreportszip.rsplit("\\", 1)[1]) > 0
            else bdreportszip.rsplit("/", 1)[1]
        )
    else:
        filelocation = this_dir
        filename = bdreportszip

    filename = filename.replace(".zip", "")

    mypath = filelocation + os.path.sep + filename
    os.makedirs(mypath, exist_ok=True)
    empty_directory(mypath)
    shutil.unpack_archive(bdreportszip, mypath)

    print(f"{filelocation=}")
    print(f"{filename=}")
    print(f"{mypath=}")

    exit
    os.chdir(mypath)

    files_list = list_files_recursive(mypath)

    print(files_list)

    isSourcereportPresent = any(f for f in files_list if "source_" in f and ".csv" in f)
    isSecurityreportPresent = any(
        f for f in files_list if "security_" in f and ".csv" in f
    )
    print("Checking files source_ amd security_ prefix are present..")
    if isSourcereportPresent and isSecurityreportPresent:
        print("File with source_ amd security_ prefix are present")
    else:
        print("File with either of source_ amd security_ prefix are not present")
        print(help_text)
        sys.exit()

    onlyfile1 = [
        f
        for f in list_files_recursive(mypath)
        if (
            isfile(join(mypath, f))
            and "source_" in join(mypath, f)
            and join(mypath, f).endswith(".csv")
        )
    ]
    onlyfile2 = [
        f
        for f in list_files_recursive(mypath)
        if (
            isfile(join(mypath, f))
            and "security_" in join(mypath, f)
            and join(mypath, f).endswith(".csv")
        )
    ]
    csv_f = filename + "-vulnerabilities.csv"
    xlsx_f = filename + "-vulnerabilities.xlsx"
    print(onlyfile1)
    print(onlyfile2)

    df1 = pandas.read_csv(onlyfile1[0])
    df2 = pandas.read_csv(onlyfile2[0])

    df = pandas.merge(
        df1, df2, how="inner", on=["Component id", "Version id", "Origin id"]
    )
    columns = [
        "Component id",
        "Version id",
        "Origin id",
        "Component origin version name_x",
        "Match content",
        "Usage",
        "Adjusted",
        "Component policy status",
        "Overridden By",
        "Origin name",
        "Origin name id",
        "Snippet Review status",
        "Scan",
        "Path",
        "Used by",
        "Component name_y",
        "Component version name_y",
        "Component origin name",
        "Component origin id",
        "Component origin version name_y",
        "Remediation status",
        "Remediation target date",
        "Remediation actual date",
        "Remediation comment",
        "URL",
        "Project path",
        "Overall score",
        "CWE Ids",
        "Reachable",
    ]
    df.drop(columns, inplace=True, axis=1)
    df = df[
        [
            "Component name_x",
            "Component version name_x",
            "Match type_x",
            "Match type_y",
            "Archive Context and Path",
            "Archive context",
            "Vulnerability id",
            "Security Risk",
            "Description",
            "Published on",
            "Updated on",
            "Base score",
            "Exploitability",
            "Impact",
            "Vulnerability source",
            "Solution available",
            "Workaround available",
            "Exploit available",
            "CVSS Version",
        ]
    ]

    def highlight_risk(row):
        if row["Security Risk"] == "HIGH":
            return ["background-color: red"] * len(row)
        elif row["Security Risk"] == "MEDIUM":
            return ["background-color: yellow"] * len(row)
        else:
            return ["background-color: white"] * len(row)

    df = df.style.apply(highlight_risk, axis=1)
    df.to_excel(xlsx_f)

    if not exists(xlsx_f):
        print("Output Excel File Not there")
        sys.exit()
    output_file = join(mypath, xlsx_f)
    print("Check the output in: " + output_file)

    if open_file:
        startfile(output_file)


if __name__ == "__main__":
    main()
