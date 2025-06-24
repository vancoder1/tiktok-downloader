import os
import subprocess
from config import PROXY_LIST_FILE
from utils.json_handler import JsonHandler

def retrieve_proxy_list(output_dir="data/", output_filename=PROXY_LIST_FILE):
    """
    Retrieves a proxy list using a cURL command and saves it to a specified directory.

    Args:
        output_dir (str): The directory where the proxy list will be saved.
                          Defaults to data/ directory.
        output_filename (str): The name of the file to save the proxy list to.
                               Defaults to PROXY_LIST_FILE set in constants.py.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directory '{output_dir}' created.")

    # Construct the full output path
    output_path = os.path.join(output_dir, output_filename)

    # The cURL command
    curl_command = [
        "curl",
        "-sL",
        "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.json",
        "-o",
        output_path
    ]

    try:
        # Execute the cURL command
        subprocess.run(curl_command, check=True, capture_output=True, text=True)
        print(f"Proxy list successfully downloaded and saved to '{output_path}'")
    except subprocess.CalledProcessError as e:
        print(f"Error executing cURL command: {e}")
        print(f"Stderr: {e.stderr}")
    except FileNotFoundError:
        print("Error: The 'curl' command was not found. Please ensure cURL is installed and in your system's PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def get_proxy_urls_from_file(json_file_path = "data/" + PROXY_LIST_FILE):
    """
    Reads a JSON file containing a list of proxy objects and returns a list of proxy URLs.

    Args:
        json_file_path (str): The path to the JSON file.
                              Defaults to data/ + PROXY_LIST_FILE.

    Returns:
        list: A list of proxy URLs (strings), or an empty list if an error occurs
              or the file is not found.
    """
    proxy_urls = []
    data = JsonHandler.load_json_file(json_file_path)

    if data is None:
        return []

    if isinstance(data, list):
        for proxy_info in data:
            if isinstance(proxy_info, dict) and "proxy" in proxy_info:
                proxy_urls.append(proxy_info["proxy"])
            else:
                print(f"Warning: Skipping item due to missing 'proxy' key or incorrect format: {proxy_info}")
    else:
        print(f"Error: JSON file at '{json_file_path}' does not contain a list of proxies at the root level.")
        return []

    return proxy_urls