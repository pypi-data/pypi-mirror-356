from dotenv import load_dotenv
from datetime import datetime
from pprint import pprint as pp
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging
import os
import pytz
import requests
import sys
import typer
import warnings

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
    response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"))  # type: ignore
    sidecar_list = response.json()["sidecars"]
    sidecar_sorted = sorted(sidecar_list, key=lambda x: x["node_name"])
    if not silent:
        for sidecar in sidecar_sorted:
            print(
                f"{sidecar['node_name']}\tID: {sidecar['node_id']}\tLast_Seen: {sidecar['last_seen']}"
            )
    return sidecar_sorted


@app.command()
def list_configurations():
    """
    List Sidecar Configurations
    """
    api_url = graylog_address + "/api/sidecar/configurations"  # type: ignore
    print(f"Making request to {api_url}")
    headers = {"Accept": "application/json"}
    response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"))  # type: ignore
    configuration_list = response.json()["configurations"]
    configuration_sorted = sorted(configuration_list, key=lambda x: x["name"])
    for configuration in configuration_sorted:
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
    response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"))  # type: ignore
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
    response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"))  # type: ignore
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
def get_configuration(
    configuration_id: str,
    silent: bool = typer.Option(
        False, "--silent", "-s", help="Silent mode. No output."
    ),
):
    """
    Get details for a configuration
    """
    api_url = graylog_address + "/api/sidecar/configurations/" + configuration_id  # type: ignore
    if not silent:
        print(f"Making request to {api_url}")
    headers = {"Accept": "application/json"}
    response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"))  # type: ignore
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
    response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"))  # type: ignore
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
    response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"))  # type: ignore
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
        response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"))  # type: ignore
        if not silent:
            pp(response.json())
        # print("Attempting to create Sidecar object with this json data.")
        sidecar = Sidecar(**response.json())
        # print("Sidecar object created.")
        matching_sidecar_objects.append(sidecar)
    return matching_sidecar_objects


@app.command()
def apply_configuration_sidecars(search_string: str, tag_id: str):
    """
    Apply a Configuration to Sidecars that contain the search string

    Arguments:

    search_string: A substring that matches one or more sidecar hostnames.

    tag_id: The tag used to locate the configuration to be applied
    """
    api_url = graylog_address + "/api/sidecars/all"  # type: ignore
    headers = {"Accept": "application/json"}
    response = requests.get(api_url, headers=headers, auth=(graylog_token, "token"))  # type: ignore
    sidecar_list = response.json()["sidecars"]
    sidecar_sorted = sorted(sidecar_list, key=lambda x: x["node_name"])
    matching_sidecars = []
    for sidecar in sidecar_sorted:
        if search_string.lower() in sidecar["node_name"].lower():
            matching_sidecars.append(sidecar)
            print(
                f"{sidecar['node_name']}\tID: {sidecar['node_id']}\tLast_Seen: {sidecar['last_seen']}"
            )
    if len(matching_sidecars) == 0:
        print("No matching sidecars found.")
        return
    configurations = list_configurations_by_tag(tag_id, silent=True)
    if len(configurations) == 0:
        print("No matching configurations found.")
        return
    print(
        f"Matching configuration found available for tag.\n"
        f"Name: {configurations[0]['name']} ID: {configurations[0]['id']}"
    )
    print("\n")
    input(
        "The Configuration will be applied to the above sidecars, press CTRL + C to abort."
    )
    config_id = configurations[0]["id"]
    config_details = get_configuration(config_id, silent=True)
    collector_id = config_details["collector_id"]
    request_origin = "ansible.ufginsurance.com"
    for sidecar in matching_sidecars:
        api_url = graylog_address + "/api/sidecars/" + sidecar["node_id"]  # type: ignore
        print(f"Making request to {api_url}")
        headers = {"Accept": "application/json", "X-Requested-By": request_origin}
        json_data = {
            "nodes": [
                {
                    "node_id": sidecar["node_id"],
                    "assignments": [
                        {
                            "configuration_id": config_id,
                            "collector_id": collector_id,
                            "assigned_from_tags": [],
                        }
                    ],
                }
            ]
        }
        response = requests.put(
            api_url,
            headers=headers,
            auth=(graylog_token, "token"),  # type: ignore
            json=json_data,
        )
        print(response.status_code)
        print(response.text)
        breakpoint()
