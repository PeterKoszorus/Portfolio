# Here are the functions for handling the JSON files
import json

# global variable for each function stores relative path to the directory with all JSONs
data_path = "Resources\\Data\\"


# Loads the json for the Ethertypes.json
def load_ethertypes():
    file = open(data_path + "Ethertypes.json", )
    return json.load(file)


# Loads the json for the ServiceAccessPoints.json
def load_sap():
    file = open(data_path + "ServiceAccessPoints.json", )
    return json.load(file)


# Loads the json for the WellKnownPorts.json
def load_ports():
    file = open(data_path + "WellKnownPorts.json", )
    return json.load(file)


# Load the json for the IPProtocols.json
def load_ip_protocols():
    file = open(data_path + "IPProtocol.json", )
    return json.load(file)


# Load the json for the IPProtocols.json
def load_icmp():
    file = open(data_path + "ICMP.json", )
    return json.load(file)
