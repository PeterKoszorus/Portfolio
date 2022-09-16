import pandas as pd


class IPStatistics:

    def __init__(self, ip_list):
        self.list_of_source_address = ip_list

    # This method will print out most all source IP addresses in descending order
    def top_source(self):
        ip_list = pd.DataFrame([ip.to_dict() for ip in self.list_of_source_address])
        # ip_list = ip_list.loc[ip_list["protocol"] == "TCP"]
        print("Source Address:   Count: ")
        print(ip_list["source_address"].value_counts())
