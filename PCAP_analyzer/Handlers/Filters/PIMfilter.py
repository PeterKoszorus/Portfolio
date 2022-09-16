# This houses the filter for the addition assignment


class Filter:

    def __init__(self, encap_data):
        self.all_encap_data = encap_data
        self.selected_data = self.select_data()

    # This method filter out each PIM frame from the communication
    def select_data(self):
        selected_data = []

        for data in self.all_encap_data:
            if data.packet_header is not None:
                if data.packet_header.protocol == "PIM":
                    selected_data.append(data)

        if selected_data:
            return selected_data
        else:
            return None

    # Prints out each frame of selected type and also the count of it
    def print_pim(self):
        for data in self.selected_data:
            data.print_encapsulated_data()
        print("{}{}".format("Number of PIM frames: ", len(self.selected_data)))
