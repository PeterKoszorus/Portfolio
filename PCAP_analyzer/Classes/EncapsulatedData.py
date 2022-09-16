# EncapsulatedData.py houses the main class for the data which is received from pcap files
import Classes.HeaderClasses.FrameHeader as fh
import Classes.HeaderClasses.PacketHeader as ph
import Classes.HeaderClasses.SegmentHeader as sh
import Classes.HeaderClasses.ARPHeader as ah
from Utilities.HexTools import ToDec


class EncapsulatedData:

    def __init__(self, raw, pos, size):
        self.pos = pos
        self.raw = raw
        self.size = size
        self.frame_type = self.get_type()
        self.on_wire = self.calculate_true_size()
        self.frame_header = fh.Frame(self.raw[:self.frame_header_length()], self.get_type())
        self.arp_header = self.create_arp_header()
        self.packet_header = self.create_packet_header()
        self.segment_header = self.create_segment_header()

    # This method calculates the size of frame transmitted on the wire
    def calculate_true_size(self):
        if self.size >= 64:
            return self.size + 4
        else:
            if self.size + 4 <= 64:
                return 64
            else:
                return self.size + 4

    # This method checks the length/type for the type of frame (Ethernet II, IEEE 802.3 LLC, LCC and SNAP, RAW)
    def get_type(self):
        dec_type = ToDec(self.raw[24:28])

        if dec_type > 1500:
            return "Ethernet II"
        elif self.raw[28:30] == "ff":
            return "IEEE 802.3-RAW"
        elif self.raw[28:30] == "aa":
            return "IEEE 802.3-LLC + SNAP"
        else:
            return "IEEE 802.3-LLC"
            # Maybe have to rework this condition later on have to catch the ISL in tracer29.pcap

    # This method checks the length of the frame header
    def frame_header_length(self):
        if self.get_type() == "Ethernet II":
            return 28
        elif self.get_type() == "IEEE 802.3-RAW" or self.get_type() == "IEEE 802.3-LLC":
            return 34
        elif self.get_type() == "IEEE 802.3-LLC + SNAP":
            return 44

    # This method will return a arp header if nested protocol is ARP
    def create_arp_header(self):
        if self.frame_header.nested_protocol == "ARP (Address Resolution Protocol)":
            return ah.ARPHeader(self.raw[28:84])
        else:
            return None

    # This method will return an packet header object if frame is Ethernet II TCP/UDP/IPV4
    def create_packet_header(self):
        if self.frame_type == "Ethernet II" and self.frame_header.nested_protocol == "Internet IP (IPV4)":
            version = self.raw[28:29]
            ihl = (int(ToDec(self.raw[29:30])) * 4) * 2
            packet_raw = self.raw[28: (28 + ihl)]
            return ph.IpHeader(packet_raw, version, ihl)
        else:
            return None

    # This method will return the segment header object, difference when UDP and when TCP
    def create_segment_header(self):
        if self.packet_header is not None:
            starting_point = self.packet_header.ending_byte
            if self.packet_header.protocol == "UDP":
                return sh.SegmentHeader(self.raw[starting_point: (starting_point + 16)], "UDP")
            elif self.packet_header.protocol == "TCP":
                tcp_hl = (ToDec(self.raw[starting_point + 24: starting_point + 25]) * 4) * 2
                return sh.SegmentHeader(self.raw[starting_point: starting_point + tcp_hl], "TCP")
        else:
            return None

    # This method is charge of printing out the raw frame data in the requested format
    def print_raw(self):
        i: int = 0

        for count, byte in enumerate(self.raw):
            if count % 32 == 0:
                print()
                print("%04x" % i, end=' ')
                i += 16
            if count % 16 == 0:
                print("  ", end='')
            if count % 2 == 0:
                print(" ", end='')
            if "None" not in byte:
                print(byte, end='')

    # This method is responsible for printing out the whole encapsulated data and it's every header
    def print_encapsulated_data(self):
        print('{}{}'.format("Frame number: ", self.pos))
        print("{}{}{}".format("Size of frame (pcap API): ", self.size, " B"))
        print("{}{}{}".format("Size of frame (on wire): ", self.on_wire, " B"))
        self.frame_header.print_frame_header()
        if self.packet_header is not None:
            self.packet_header.print_packet_header()
        if self.segment_header is not None:
            self.segment_header.print_seg_header()
        self.print_raw()
        print()
        print("-------------------------------------------------------------------------------------------")
