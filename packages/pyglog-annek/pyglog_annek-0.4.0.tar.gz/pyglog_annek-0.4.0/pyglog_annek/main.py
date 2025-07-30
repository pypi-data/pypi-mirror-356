from dotenv import load_dotenv
from datetime import datetime
from pprint import pprint as pp
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging
import json
import os
import pytz
import requests
import sys
import typer
import warnings
from urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning) # type: ignore

# Load environment
load_dotenv()

# Instantiate instance
app = typer.Typer()

graylog_address = os.getenv("GRAYLOG_ADDR")
graylog_token = os.getenv("GRAYLOG_TOKEN")

if graylog_address is None or graylog_token is None:
    print("You must set GRAYLOG_ADDR and GRAYLOG_TOKEN or define them in a .env file.")
    sys.exit(1)


warnings.filterwarnings("ignore", category=DeprecationWarning)

logname = "pyglog.log"

logging.basicConfig(
    filename=logname,
    filemode="a",
    format="%(asctime)s.%(msecs)d %(name)s %(levelname)s -- %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger("pyglog")
logger.info("Starting Pyglog the Graylog CLI in Python")


class Assignment(BaseModel):
    assigned_from_tags: List[str]
    collector_id: str
    configuration_id: str


class NodeDetails(BaseModel):
    collector_configuration_directory: str
    ip: str
    log_file_list: Optional[List[str]] = None
    metrics: Dict
    operating_system: str
    status: Dict
    tags: List[str]


class Sidecar(BaseModel):
    active: bool
    assignments: list[Assignment]
    collectors: None
    last_seen: datetime
    node_details: NodeDetails
    node_id: str
    node_name: str
    sidecar_version: str


def time_parser(time_string):
    """Parses the time string into a datetime object"""
    try:
        parts = time_string.split(".")
        dt = parts[0]
        offset = parts[1].split("-")
        time_string = dt + "_" + "-" + offset[1]
        format_data = "%Y-%m-%dT%H:%M:%S_%z"
        time_obj = datetime.strptime(time_string, format_data)
        return time_obj
    except (ValueError, IndexError) as e:
        logger.error("Error parsing time string: %s", time_string)
        logger.error("Assigning epoch date")
        logger.error("Error: %s", e)
        time_obj = datetime.fromtimestamp(0, pytz.utc)
        return time_obj


def check_sidecar_has_config(sidecar, config_id):
    """Checks if the sidecar has the configuration"""
    for assignment in sidecar["assignments"]:
        if assignment["configuration_id"] == config_id:
            return True
    return False


@app.callback()
def callback():
    """
    A CLI for Graylog API calls

    You must set GRAYLOG_ADDR and GRAYLOG_TOKEN or define them in a .env file.

    Example:

    GRAYLOG_ADDR="https://graylog.example.com"

    GRAYLOG_TOKEN="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    """


@app.command()
def list_sidecars(
    silent: bool = typer.Option(
        False, "--silent", "-s", help="Silent mode. No output."
    ),
):
    """
    List Sidecars
    """
    api_url = graylog_address + "/api/sidecars/all"  # type: ignore
    if not silent:
        print(f"Making request to {api_url}")
    headers = {"Accept": "application/json"}
    response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"), verify=False)  # type: ignore
    sidecar_list = response.json()["sidecars"]
    sidecar_sorted = sorted(sidecar_list, key=lambda x: x["node_name"])
    if not silent:
        for sidecar in sidecar_sorted:
            print(
                f"{sidecar['node_name']}\tID: {sidecar['node_id']}\tLast_Seen: {sidecar['last_seen']}"
            )
    return sidecar_sorted


@app.command()
def list_configurations(
    silent: bool = typer.Option(
        False, "--silent", "-s", help="Silent mode. No output."
    ),
):
    """
    List Sidecar Configurations
    """
    api_url = graylog_address + "/api/sidecar/configurations"  # type: ignore
    if not silent:
        print(f"Making request to {api_url}")
    headers = {"Accept": "application/json"}
    response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"), verify=False)  # type: ignore
    configuration_list = response.json()["configurations"]
    configuration_sorted = sorted(configuration_list, key=lambda x: x["name"])
    for configuration in configuration_sorted:
        if not silent:
            print(
                f"{configuration['name']:<40} ID: {configuration['id']:<30} Tags: {str(configuration['tags']):<15}"
            )
    return configuration_sorted


@app.command()
def list_configurations_by_tag(
    tag: str,
    silent: bool = typer.Option(
        False, "--silent", "-s", help="Silent mode. No output."
    ),
):
    """
    List Sidecar Configurations associated with tag

    Arguments:

    tag: The name of the tag.
    """
    api_url = graylog_address + "/api/sidecar/configurations"  # type: ignore
    if not silent:
        print(f"Making request to {api_url}")
    headers = {"Accept": "application/json"}
    response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"), verify=False)  # type: ignore
    configuration_list = response.json()["configurations"]
    configuration_sorted = sorted(configuration_list, key=lambda x: x["name"])
    tag_match = []
    for configuration in configuration_sorted:
        if len(configuration["tags"]) == 0:
            continue
        else:
            for t in configuration["tags"]:
                if tag.lower() == t.lower():
                    tag_match.append(configuration)
                    if not silent:
                        print(
                            f"{configuration['name']:<40} ID: {configuration['id']:<30} Tags: {str(configuration['tags']):<15}"
                        )
    return tag_match


@app.command()
def list_matching_sidecars(search_string: str):
    """
    List Sidecars that contain the search string

    Arguments:

    search_string: A substring that matches one or more sidecar hostnames.
    """
    api_url = graylog_address + "/api/sidecars/all"  # type: ignore
    print(f"Making request to {api_url}")
    headers = {"Accept": "application/json"}
    response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"), verify=False)  # type: ignore
    sidecar_list = response.json()["sidecars"]
    sidecar_sorted = sorted(sidecar_list, key=lambda x: x["node_name"])
    matching_sidecars = []
    for sidecar in sidecar_sorted:
        if search_string in sidecar["node_name"]:
            matching_sidecars.append(sidecar)
            print(
                f"{sidecar['node_name']}\tID: {sidecar['node_id']}\tLast_Seen: {sidecar['last_seen']}"
            )
    return matching_sidecars


@app.command()
def get_configuration_by_id(
    configuration_id: str,
    silent: bool = typer.Option(
        False, "--silent", "-s", help="Silent mode. No output."
    ),
):
    """
    Get details for a configuration by ID.
    """
    api_url = graylog_address + "/api/sidecar/configurations/" + configuration_id  # type: ignore
    if not silent:
        print(f"Making request to {api_url}")
    headers = {"Accept": "application/json"}
    response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"), verify=False)  # type: ignore
    result = response.json()
    if not silent:
        pp(result)
    return result

@app.command()
def get_configuration_by_tag(
    configuration_tag: str,
    silent: bool = typer.Option(
        False, "--silent", "-s", help="Silent mode. No output."
    ),
):
    """
    Get details for a configuration by tag name.
    """
    configurations = list_configurations(silent=True)
    for configuration in configurations:
        if configuration_tag.lower() in configuration["tags"]:
            configuration_id = configuration["id"]
            break
    if configuration_id is None:
        print("No matching configuration found.")
        return
    api_url = graylog_address + "/api/sidecar/configurations/" + configuration_id  # type: ignore
    if not silent:
        print(f"Making request to {api_url}")
    headers = {"Accept": "application/json"}
    response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"), verify=False)  # type: ignore
    result = response.json()
    if not silent:
        pp(result)
    return result

@app.command()
def get_sidecar_by_id(sidecar_id: str):
    """
    Get sidecar by ID
    """
    api_url = graylog_address + "/api/sidecars/" + sidecar_id  # type: ignore
    headers = {"Accept": "application/json"}
    response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"), verify=False)  # type: ignore
    result = response.json()
    pp(result)
    return result


@app.command()
def get_sidecar_details(
    search_string: str,
    silent: bool = typer.Option(
        False, "--silent", "-s", help="Silent mode. No output."
    ),
):
    """
    Get details for Sidecars that match the search string

    Arguments:

    search_string: A string that matches sidecar hostnames.
    """
    api_url = graylog_address + "/api/sidecars/all"  # type: ignore
    headers = {"Accept": "application/json"}
    response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"), verify=False)  # type: ignore
    sidecar_list = response.json()["sidecars"]
    sidecar_sorted = sorted(sidecar_list, key=lambda x: x["node_name"])
    matching_sidecars = []
    matching_sidecar_objects = []
    for sidecar in sidecar_sorted:
        if search_string.lower() in sidecar["node_name"].lower():
            matching_sidecars.append(sidecar)
            if not silent:
                print(
                    f"{sidecar['node_name']}\tID: {sidecar['node_id']}\tLast_Seen: {sidecar['last_seen']}"
                )
    if len(matching_sidecars) == 0:
        if not silent:
            print("No matching sidecars found.")
        return
    for sidecar in matching_sidecars:
        api_url = graylog_address + "/api/sidecars/" + sidecar["node_id"]  # type: ignore
        if not silent:
            print(f"Making request to {api_url}")
        headers = {"Accept": "application/json"}
        response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"), verify=False)  # type: ignore
        if not silent:
            pp(response.json())
        sidecar = Sidecar(**response.json())
        matching_sidecar_objects.append(sidecar)
    return matching_sidecar_objects


@app.command()
def apply_configuration_sidecars(search_string: str, tag_id: str,
                                     noconfirm: bool = typer.Option(
        False, "--no-confirm", help="Do not prompt for confirmation."
    ),
                                 ):
    """
    Apply a Configuration to Sidecars with a hostname that contains the search string.

    Arguments:

    search_string: A substring that matches one or more sidecar hostnames.

    tag_id: The tag used to locate the configuration to be applied
    """
    api_url = graylog_address + "/api/sidecars/all"  # type: ignore
    headers = {"Accept": "application/json"}
    response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"), verify=False)  # type: ignore
    configurations = list_configurations_by_tag(tag_id, silent=True)
    if len(configurations) == 0:
        print("No matching configurations found.")
        return
    print(
        f"\n"
        f"Matching configuration found available for tag.\n"
        f"Name: {configurations[0]['name']} ID: {configurations[0]['id']}"
    )
    print("\n")
    config_id = configurations[0]["id"]
    config_details = get_configuration_by_id(config_id, silent=True)
    collector_id = config_details["collector_id"]
    request_origin = "ansible.ufginsurance.com"
    sidecar_list = response.json()["sidecars"]
    sidecar_sorted = sorted(sidecar_list, key=lambda x: x["node_name"])
    matching_sidecars = []
    for sidecar in sidecar_sorted:
        if search_string.lower() in sidecar["node_name"].lower():
            matching_sidecars.append(sidecar)
    if len(matching_sidecars) == 0:
        print("No matching sidecars found.")
        return
    to_remove = []
    for sidecar in matching_sidecars:
        if check_sidecar_has_config(sidecar, config_id):
            print(
                f"Sidecar {sidecar['node_name']} already has the configuration applied, skipping."
            )
            to_remove.append(sidecar)
    for sidecar in to_remove:
        matching_sidecars.remove(sidecar)
    if len(matching_sidecars) == 0:
        print("\nAll listed sidecars already have that configuration applied.")
        return
    for sidecar in matching_sidecars:
        print(
            f"{sidecar['node_name']}\tID: {sidecar['node_id']}\tLast_Seen: {sidecar['last_seen']}"
        )
    if not noconfirm:
        input(
            "\nThe Configuration will be applied to the above sidecars, press CTRL + C to abort."
        )
    for sidecar in matching_sidecars:
        api_url = graylog_address + "/api/sidecars/configurations"# + sidecar["node_id"] + "/assignments" # type: ignore
        print(f"Making request to {api_url}")
        headers = {"Accept": "application/json", "X-Requested-By": request_origin}
        print(f"Applying configuration to {sidecar['node_name']}")
        collector_id = configurations[0]["collector_id"]
        config_id = configurations[0]["id"]
        config_dict = {'assigned_from_tag': [], 'collector_id': collector_id, 'configuration_id': config_id}
        sidecar['assignments'].append(config_dict)
        data = {"nodes": [{"node_id": sidecar['node_id'],
                           "assignments": [{
                               "collector_id": collector_id,
                               "configuration_id": config_id
                           }]}]}
        response = requests.put(
            api_url,
            headers=headers,
            auth=(graylog_token, "token"),  # type: ignore
            json=data,
            verify=False,
        )
        print(response.status_code)
        print(response.text)


@app.command()
def remove_configuration_sidecars(search_string: str, tag_id: str,
                                     noconfirm: bool = typer.Option(
        False, "--no-confirm", help="Do not prompt for confirmation."
    ),
                                 ):
    """
    Remove a Configuration to Sidecars with a hostname that contains the search string.

    Arguments:

    search_string: A substring that matches one or more sidecar hostnames.

    tag_id: The tag used to locate the configuration to be applied
    """
    api_url = graylog_address + "/api/sidecars/all"  # type: ignore
    headers = {"Accept": "application/json"}
    response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"), verify=False)  # type: ignore
    configurations = list_configurations_by_tag(tag_id, silent=True)
    if len(configurations) == 0:
        print("No matching configurations found.")
        return
    print(
        f"\n"
        f"Matching configuration found available for tag.\n"
        f"Name: {configurations[0]['name']} ID: {configurations[0]['id']}"
    )
    print("\n")
    config_id = configurations[0]["id"]
    request_origin = "ansible.ufginsurance.com"
    sidecar_list = response.json()["sidecars"]
    sidecar_sorted = sorted(sidecar_list, key=lambda x: x["node_name"])
    matching_sidecars = []
    for sidecar in sidecar_sorted:
        if search_string.lower() in sidecar["node_name"].lower():
            matching_sidecars.append(sidecar)
    if len(matching_sidecars) == 0:
        print("No matching sidecars found.")
        return
    to_remove = []
    for sidecar in matching_sidecars:
        if not check_sidecar_has_config(sidecar, config_id):
            print(
                f"Sidecar {sidecar['node_name']} does not have the configuration applied, skipping."
            )
            to_remove.append(sidecar)
    for sidecar in to_remove:
        matching_sidecars.remove(sidecar)
    if len(matching_sidecars) == 0:
        print("\nNone of the listed sidecars have that configuration applied.")
        return
    for sidecar in matching_sidecars:
        print(
            f"{sidecar['node_name']}\tID: {sidecar['node_id']}\tLast_Seen: {sidecar['last_seen']}"
        )
    if not noconfirm:
        input(
            "\nThe Configuration will be removed from the above sidecars, press CTRL + C to abort."
        )
    for sidecar in matching_sidecars:
        api_url = graylog_address + "/api/sidecars/configurations" # + sidecar["node_id"]  # type: ignore
        print(f"Making request to {api_url}")
        headers = {"Accept": "application/json", "X-Requested-By": request_origin}
        print(f"Removing configuration from {sidecar['node_name']}")
        config_id = configurations[0]["id"]
        removed = 0
        for assignment in sidecar['assignments']:
            if (assignment['configuration_id'] == config_id):
                sidecar['assignments'].remove(assignment)
                removed += 1
        if removed == 0:
            print(f"Configuration not applied to {sidecar['node_name']}.")
            print("Configuration not found, or configuration was assigned via local tag.")
            break
        data = {"nodes": [{"node_id": sidecar['node_id'],
                           "assignments": sidecar['assignments']}]}
        response = requests.put(
            api_url,
            headers=headers,
            auth=(graylog_token, "token"),  # type: ignore
            json=data,
            verify=False,
        )
        print(response.status_code)
        print(response.text)
