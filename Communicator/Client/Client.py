import socket
import queue
import math
import os.path
import time
import zlib
import random

from HeaderTools import DataEncapsulation
from Exceptions import IncorrectFlagType, CommunicationEnd

# Variable which holds percentage for error occurrence
ERROR = 25


def client():

    VELKOST_REZIE = 0

    connection_options = user_input("connect")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Connection initialization
    try:
        init_msg = DataEncapsulation.create_header(0, None, 0)
        sock.sendto(init_msg, connection_options)
        VELKOST_REZIE += 1

        sock.settimeout(30)
        data, addr = sock.recvfrom(1472)

        # Parsed data indexing: 0 - flag, 1 - frag_order_num, 2 - crc
        parsed_data = DataEncapsulation.parse_header(data)

        if parsed_data[0] == 0:
            print(f"Connection was successfully made with server: {addr}")
        else:
            raise IncorrectFlagType.IncorrectFlagType
    except socket.timeout:
        print("Socket timed out")
        print("Connection wasn't successful")
        sock.close()
        return VELKOST_REZIE
    except IncorrectFlagType.IncorrectFlagType:
        print("The flag wasn't matched")
        print("Connection wasn't successful")
        sock.close()
        return VELKOST_REZIE
    except ConnectionResetError:
        print("Server doesn't listen to communication")
        print("Connection wasn't successful")
        sock.close()
        return VELKOST_REZIE

    # Main client loop
    try:
        while True:

            # Data sending process
            send_process = sending_data(sock, connection_options)
            VELKOST_REZIE += send_process[1]
            if not send_process[0]:
                sock.sendto(DataEncapsulation.create_header(20, None, 0), connection_options)
                VELKOST_REZIE += 1
                sock.settimeout(10)
                sock.recvfrom(1472)

                raise CommunicationEnd.CommunicationEnd

            # Keep Alive
            kp_process = keep_alive(sock, connection_options)
            VELKOST_REZIE += kp_process[1]
            if not kp_process[0]:
                sock.sendto(DataEncapsulation.create_header(20, None, 0), connection_options)
                VELKOST_REZIE += 1
                sock.settimeout(10)
                sock.recvfrom(1472)

                raise CommunicationEnd.CommunicationEnd
    except socket.timeout:
        print("Socket timed out")
        sock.close()
        return VELKOST_REZIE
    except CommunicationEnd.CommunicationEnd:
        print("Communication has been successfully closed")
        sock.close()
        return VELKOST_REZIE
    except ConnectionResetError:
        print("Server doesn't listen to communication")
        sock.close()
        return VELKOST_REZIE


# Function which handles all the whole data sending process
def sending_data(sock, connection_options):
    # Data preparation
    VELKOST_REZIE = 0
    global frag_data, msg  # question for Rudo
    data_info = user_input("data_info")

    if data_info[0] == "Message":

        if data_info[1] == 0:
            if len(data_info[2]) > 1464:
                frag_data = fragment_data(data_info[2], 1464)
            else:
                frag_data = queue.PriorityQueue()
                frag_data.put((0, data_info[2]))
        else:
            frag_data = fragment_data(data_info[2], data_info[1])

        msg = DataEncapsulation.create_header(3, frag_data.qsize(), 0)
    elif data_info[0] == "File":
        file_name = os.path.basename(data_info[2])

        file = open(data_info[2], "rb")
        raw_file = file.read()

        if data_info[1] == 0:
            if len(raw_file) > 1464:
                frag_data = fragment_data(raw_file, 1464)
            else:
                frag_data = queue.PriorityQueue()
                frag_data.put((0, raw_file))
        else:
            frag_data = fragment_data(raw_file, data_info[1])

        data = bytes(file_name, "utf-8")
        header = DataEncapsulation.create_header(3, frag_data.qsize(), zlib.crc32(data))

        msg = header + data

    # Info packet send
    try:
        sock.sendto(msg, connection_options)
        VELKOST_REZIE += 1
        sock.settimeout(60)
        data, addr = sock.recvfrom(1472)

        # Parsed data indexing: 0 - flag, 1 - frag_order_num, 2 - crc, 3 - data (optional)
        parsed_data = DataEncapsulation.parse_header(data)

        if parsed_data[0] != 3:
            raise IncorrectFlagType.IncorrectFlagType
        print("Information header success")

        while not frag_data.empty():

            # Tuple 0 - order number, 1 - data in bytes
            frag_to_send = frag_data.get()

            # Data which is being sent is message
            if data_info[0] == "Message":
                msg = DataEncapsulation.create_header(1, frag_to_send[0], zlib.crc32(frag_to_send[1]))
            # Data which is being sent is File
            if data_info[0] == "File":
                msg = DataEncapsulation.create_header(2, frag_to_send[0], zlib.crc32(frag_to_send[1]))

            # Checking if user wants to simulate errors if yes there is chance that the data will be corrupted
            if data_info[3] == "Yes":
                if random.randint(0, 100) < ERROR:
                    msg = msg + bytearray([1] * len(frag_to_send[1]))
                else:
                    msg = msg + frag_to_send[1]
            elif data_info[3] == "No":
                msg = msg + frag_to_send[1]

            sock.sendto(msg, connection_options)
            VELKOST_REZIE += 1

            # Have to ask about this or look it up
            sock.settimeout(10)
            data, addr = sock.recvfrom(1472)

            # Parsed data indexing: 0 - flag, 1 - frag_order_num, 2 - crc, 3 - data (optional)
            parsed_data = DataEncapsulation.parse_header(data)

            # Fragment was received correctly
            if parsed_data[0] == 10:
                print("------------------------------------------------------------")
                print(f"Fragment num: {frag_to_send[0]} with size: {len(frag_to_send[1])},"
                      f" was received by server correctly")
                print("------------------------------------------------------------")
                continue

            # Fragment was received with error
            if parsed_data[0] == 11:
                frag_data.put(frag_to_send)
                print("------------------------------------------------------------")
                print(f"Fragment num: {frag_to_send[0]} with size: {len(frag_to_send[1])},"
                      f" was corrupted sending it again")
                print("------------------------------------------------------------")
                continue

    except ConnectionResetError:
        print("Server doesn't listen to communication")
        return False, VELKOST_REZIE
    except socket.timeout:
        print("Reply timed out")
        return False, VELKOST_REZIE
    except IncorrectFlagType.IncorrectFlagType:
        print("The flag wasn't matched")
        return False, VELKOST_REZIE

    return True, VELKOST_REZIE


# Function which handles the keep alive process
def keep_alive(sock, connection_options):

    rezia_kp = 0

    print("------------------------------------------------------------")
    print("Starting keep alive if you want to end keep alive press CTRL + C")

    try:
        while True:
            time.sleep(3)
            sock.sendto(DataEncapsulation.create_header(30, None, 0), connection_options)
            rezia_kp += 1

            sock.settimeout(10)
            data, addr = sock.recvfrom(1472)

            # Parsed data indexing: 0 - flag, 1 - frag_order_num, 2 - crc, 3 - data (optional)
            parsed_data = DataEncapsulation.parse_header(data)

            if parsed_data[0] != 30:
                raise IncorrectFlagType.IncorrectFlagType
            print("------------------------------------------------------------")
            print("Keep Alive")

    except IncorrectFlagType.IncorrectFlagType:
        print("Incorrect flag type was received")
        print("Keep alive turning off")
        return False, rezia_kp
    except socket.timeout:
        print("Socket timed out")
        print("Keep alive turning off")
        return False, rezia_kp
    except ConnectionResetError:
        print("Server doesn't listen to communication")
        print("Keep alive turning off")
        return False, rezia_kp
    except KeyboardInterrupt:
        print("Turning off keep alive")
        cont = input("Do you want to send another file or message ? Yes/No ")
        if cont == "Yes":
            # For indicating server that new communication is starting
            sock.sendto(DataEncapsulation.create_header(3, 0, 0), connection_options)
            rezia_kp += 1
            return True, rezia_kp
        if cont == "No":
            return False, rezia_kp


# Function which fragments the data and returns a PQ with the data ordered and fragmented
def fragment_data(data, frag_size):
    frag_num = math.ceil((len(data) / frag_size))
    pq = queue.PriorityQueue()

    count = 0
    start = 0
    end = frag_size

    while count < frag_num:
        pq.put((count, data[start:end]))
        count += 1
        start = end
        end = end + frag_size
        if end > len(data):
            end = len(data)

    return pq


# Function which processes the user input for the ClientSide
def user_input(process):
    if process == "connect":
        print("------------------------------------------------------------")
        ip_address = input("Enter the IP Address of server: ")
        port_number = input("Enter the port number on which the server will listen: ")
        print("------------------------------------------------------------")

        return ip_address, int(port_number)

    if process == "data_info":
        print("------------------------------------------------------------")
        f_type = input("What do you want to send: File/Message ")
        print("Fragment size (MAX 1464) if 0 the fragmentation will be automatically determined")
        frag_size = input("Enter the size of fragments you want the message to be split in: ")
        err = input("Do you want to simulate errors in the communication? Yes/No ")

        if f_type == "Message":
            message = input("Enter the message you want to send: ")
            print("------------------------------------------------------------")
            return f_type, int(frag_size), bytes(message, "utf-8"), err
        if f_type == "File":
            path = input("Enter the absolute path to the file: ")
            print("------------------------------------------------------------")
            while os.path.exists(path) is False:
                print("The file doesn't exist")
                path = input("Enter the absolute path to the file: ")
                print("------------------------------------------------------------")
            return f_type, int(frag_size), path, err


if __name__ == '__main__':
    print("Hello this is a Client")
    client()
