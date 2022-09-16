# FrameHeader.py handles the frame header of the encapsulated data
import Handlers.JsonExtractor as je


# Frame object class
class Frame:

    def __init__(self, frame_header, type_of_frame):
        self.frame_header = frame_header
        self.dmac = self.destination_mac()
        self.smac = self.source_mac()
        self.type = type_of_frame
        self.nested_protocol = self.get_nested_protocol()

    # This method separates Destination mac address from the rest of frame_header
    def destination_mac(self):
        return self.frame_header[:12]

    # This method separates Source mac address from the rest of frame_header
    def source_mac(self):
        return self.frame_header[12:24]

    # This method will get the nested protocol of IEEE 802.3 or Ethernet II
    def get_nested_protocol(self):

        if self.type == "Ethernet II":
            ethertypes = je.load_ethertypes()
            for protocol in ethertypes:
                if protocol == self.frame_header[24:28]:
                    return ethertypes[protocol]

        if self.type == "IEEE 802.3-RAW":
            return "IPX"

        sap = je.load_sap()

        if self.type == "IEEE 802.3-LLC":
            for protocol in sap:
                if protocol == self.frame_header[28:30]:
                    return sap[protocol]

        if self.type == "IEEE 802.3-LLC + SNAP":
            for protocol in sap:
                if protocol == self.frame_header[40:44]:
                    return sap[protocol]

    # This method is responsible for printing out the information about the frame header
    def print_frame_header(self):
        print("FRAME HEADER INFORMATION")
        print("Destination MAC address: " + self.dmac[:2] + ":" + self.dmac[2:4] + ":" + self.dmac[4:6] +
              ":" + self.dmac[6:8] + ":" + self.dmac[8:10] + ":" + self.dmac[10:12])
        print("Source MAC address: " + self.smac[:2] + ":" + self.smac[2:4] + ":" + self.smac[4:6] +
              ":" + self.smac[6:8] + ":" + self.smac[8:10] + ":" + self.smac[10:12])
        print("{}{}".format("Type of frame: ", self.type))
        print("{}{}".format("Nested protocol: ", self.nested_protocol))
