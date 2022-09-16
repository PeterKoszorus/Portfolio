# Main file where everything will be imported
import os
import argparse
from Handlers import Extractor, IPstatistics
from Handlers.Analyzators import AnalyzeTCP, AnalyzeARP, AnalyzeICMP, AnalyzeTFTP
from Handlers.Filters import PIMfilter


# Function which gets the system path
def get_dirname():
    return os.path.dirname(__file__)


def main():

    parser = argparse.ArgumentParser(description="Analyzator pcap suborov first use flag -file than -run "
                                                 "(optional -type),"
                                                 "\nPython 3.8 requirements: pandas, scapy")

    parser.add_argument("-file", "--PcapName", help="Accepts the file name of pcap stored in "
                                                    "Resources.vzorky_na_pcap_analyzu")

    parser.add_argument("-run", "--whatToDo", help="Tells the program what to do, there are two options: "
                                                   "All (prints out info about every frame), "
                                                   "Analyze (analyzes specified communication)")
    parser.add_argument("-type", "--typeOfCommunication", help="If you selected analyze you have to select a type as"
                                                               "wel. Options: http, https, telnet, ssh, ftp-control,"
                                                               "ftp-data, tftp, icmp, arp, pim")

    args = parser.parse_args()

    if args.PcapName:

        frame_extractor = Extractor.FrameLoader(get_dirname(), args.PcapName)

        if frame_extractor.pcap is not None:
            encap_data_list = frame_extractor.load_raw()

            if args.whatToDo == "All":
                valid_ip_for_stats = []

                for encap_data in encap_data_list:
                    encap_data.print_encapsulated_data()
                    if encap_data.packet_header is not None:
                        valid_ip_for_stats.append(encap_data.packet_header)

                ip_stats = IPstatistics.IPStatistics(valid_ip_for_stats)
                ip_stats.top_source()
            elif args.whatToDo == "Analyze":
                list_tcp = ["http", "https", "telnet", "ssh", "ftp-control", "ftp-data"]
                if args.typeOfCommunication:
                    if args.typeOfCommunication in list_tcp:
                        analyzator = AnalyzeTCP.Analyze(encap_data_list, args.typeOfCommunication)
                        if analyzator.selected_data is not None:
                            analyzator.print_analyze_tcp()
                        else:
                            print("In selected pcap there is no communication of chosen type")
                    elif args.typeOfCommunication == "arp":
                        analyzator = AnalyzeARP.Analyze(encap_data_list)
                        if analyzator.communications is not None:
                            analyzator.print_arp()
                        else:
                            print("In selected pcap there is no communication of chosen type")
                    elif args.typeOfCommunication == "icmp":
                        analyzator = AnalyzeICMP.Analyze(encap_data_list)
                        if analyzator.all_icmp is not None:
                            analyzator.print_icmp()
                        else:
                            print("In selected pcap there is no communication of chosen type")
                    elif args.typeOfCommunication == "tftp":
                        analyzator = AnalyzeTFTP.Analyze(encap_data_list)
                        if analyzator.communications is not None:
                            analyzator.print_tftp()
                        else:
                            print("In selected pcap there is no communication of chosen type")
                    elif args.typeOfCommunication == "pim":
                        pim_filter = PIMfilter.Filter(encap_data_list)
                        if pim_filter.selected_data is not None:
                            pim_filter.print_pim()
                        else:
                            print("In selected pcap there is no communication of chosen type")
                else:
                    print("There is no argument for the type of communication you want to analyze "
                          "(try flag -h for help)")

            else:
                print("You have inputted the wrong argument or few arguments (try flag -h for help)")
    else:
        print("You havnt specified the file you want to work with (try flag -h for help)")


if __name__ == '__main__':
    main()
