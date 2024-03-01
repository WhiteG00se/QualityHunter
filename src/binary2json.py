from pathlib import Path
import json
import struct
from utils import parse_template

file_path = "src/armor_converted.am_dat"
file_out = Path(file_path).name + ".json"

file_type = file_path.split(".")[-1]

# Define the structure formats
header_format = '<IHI'
entry_format = '<IhBhBBhhhhBBIbbbbbBBBBhBhBhBhBhBIhhhB'

github_template_url = f"https://raw.githubusercontent.com/Synthlight/MHW-Editor/master/010%20Templates/{file_type}.bt"
datatypes, datanames = parse_template(github_template_url)

# Define the structure sizes
header_size = struct.calcsize(header_format)
entry_size = struct.calcsize(entry_format)


# Function to read the header
def read_header(file):
    header_data = file.read(header_size)
    return struct.unpack(header_format, header_data)


# Function to read an entry
def read_entry(file):
    entry_data = file.read(entry_size)
    return struct.unpack(entry_format, entry_data)


# Open the binary file
with open(file_path, 'rb') as file:
    # Read the header
    json_dict = {}
    header = read_header(file)
    header_dict = {}
    for idx, el in enumerate(header):
        header_dict[datanames[idx]] = el
    json_dict["Header"] = header_dict

    # Read entries
    entries_list = []
    for i in range(header[2]):
        entries = read_entry(file)
        entry_dict = {}
        for idx, entry in enumerate(entries):
            entry_dict[datanames[idx + len(header)]] = entry
        entries_list.append(entry_dict)
    json_dict["Entries"] = entries_list

    with open(file_out, "w") as f:
        json.dump(json_dict, f, indent=4)