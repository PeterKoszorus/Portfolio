import socket
import queue
import time
import zlib
import os

from HeaderTools import DataEncapsulation
from Exceptions import CommunicationEnd, IncorrectStart


def server():
    connection_options = user_input("connect")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.bind(connection_options)

    # Connection initialization
    try:
        print("---------")
        print("Listening")
        print("---------")

        sock.settimeout(60)
        data, addr = sock.recvfrom(1472)
        print("received msg: %s" % data)
        print(f"Massage came from: {addr}")

        # Sending back the exactly same init frame to establish connection
        sock.sendto(data, addr)

        print("Communication was successfully initialized")

    except socket.timeout:
        print("Socket timed out")
        print("Connection wasn't successful")
        sock.close()
        return
    except ConnectionResetError:
        print("Client doesn't listen to communication")
        print("Connection wasn't successful")
        sock.close()
        return

    # Data receiving process
    receive_data(sock)


# Function which will handle data receiving
def receive_data(sock):

    global file_name, dir_path  # Otazka zasa na ruda

    received_data = queue.PriorityQueue()

    try:

        # Handling the info packet here so the user has more time to input all the details on the client side
        sock.settimeout(60)
        data, addr = sock.recvfrom(1472)

        # Parsed data indexing: 0 - flag, 1 - frag_order_num, 2 - crc, 3 - data (optional)
        parsed_data = DataEncapsulation.parse_header(data)

        # Info header handling
        if parsed_data[0] == 3:

            expected_frag_count = parsed_data[1]
            new_data = True

            # This means file will be transmitted
            if len(parsed_data) == 4:
                if not check_crc(parsed_data[2], parsed_data[3]):
                    # Check the crc, this doesn't have any effect in the info header
                    sock.sendto(data, addr)
                    pass
                file_name = parsed_data[3].decode("utf-8")
                dir_path = user_input("file_path")

            print("------------------------------------------------------------")
            print(f"Info packet successfully received expected num. of fragments: " +
                  f"{parsed_data[1]}")
            print("------------------------------------------------------------")

            sock.sendto(data, addr)
        else:
            raise IncorrectStart.IncorrectStart
        while True:
            sock.settimeout(10)
            data, addr = sock.recvfrom(1472)

            # Parsed data indexing: 0 - flag, 1 - frag_order_num, 2 - crc, 3 - data (optional)
            parsed_data = DataEncapsulation.parse_header(data)

            # Beginning of new data sending process
            if parsed_data[0] == 3:
                receive_data(sock)
                return

            # Message, File receiving handling
            if (parsed_data[0] == 1 or parsed_data[0] == 2) and new_data:
                print("------------------------------------------------------------")
                print(f"Server received a fragment num: {parsed_data[1]}, and with the size of {len(parsed_data[3])}")

                if not check_crc(parsed_data[2], parsed_data[3]):
                    print(f"Fragment num: {parsed_data[1]} was received with error")
                    sock.sendto(DataEncapsulation.create_header(11, None, 0), addr)
                    continue

                print(f"Fragment num: {parsed_data[1]} was received successfully")
                sock.sendto(DataEncapsulation.create_header(10, None, 0), addr)
                received_data.put((parsed_data[1], parsed_data[3]))

                if received_data.qsize() == expected_frag_count:
                    if parsed_data[0] == 1:
                        process_message(received_data)
                    elif parsed_data[0] == 2:
                        process_file(received_data, file_name, dir_path)
                        pass
                    expected_frag_count = -1
                    new_data = False
                    received_data = queue.PriorityQueue()

            # Communication ending
            if parsed_data[0] == 20:
                sock.sendto(data, addr)
                raise CommunicationEnd.CommunicationEnd

            # Keep alive
            if parsed_data[0] == 30:
                print("Keep Alive")
                sock.sendto(data, addr)

    except socket.timeout:
        print("Client connection timed out")
        sock.close()
        return
    except ConnectionResetError:
        print("Client stopped listening to communication")
        sock.close()
        return
    except CommunicationEnd.CommunicationEnd:
        print("Communication is being ended by client")
        sock.close()
        return
    except IncorrectStart.IncorrectStart:
        print("Sending process didn't start with the info header")
        sock.close()
        return


# Function which processes the received message
def process_message(pq):

    final_msg = pq.get()[1].decode("utf-8")

    while not pq.empty():
        final_msg = final_msg + pq.get()[1].decode("utf-8")

    print("------------------------------------------------------------")
    print("The received msg is:")
    print(final_msg)


# Function which processes the received file
def process_file(pq, f_name, d_name):

    file_content = pq.get()[1]

    while not pq.empty():
        file_content = file_content + pq.get()[1]

    path = os.path.join(d_name, f_name)
    file = open(path, "wb")
    file.write(file_content)

    print("------------------------------------------------------------")
    print(f"File with the name: {f_name} is saved in {d_name}")


# Function which checks the crc
def check_crc(received_crc, data):
    new_crc = zlib.crc32(data)

    if received_crc == new_crc:
        return True
    else:
        return False


# Function which processes the user input for the ClientSide
def user_input(process):

    if process == "connect":
        print("------------------------------------------------------------")
        ip_address = input("Enter the IP Address of client: ")
        port_number = input("Enter the port number on which the communication will arrive: ")
        print("------------------------------------------------------------")

        return ip_address, int(port_number)
    if process == "file_path":
        print("------------------------------------------------------------")
        file_path = input("Enter a directory where the file will be stored: ")
        print("------------------------------------------------------------")
        while os.path.exists(file_path) is False:
            print("The directory doesn't exist")
            file_path = input("Enter a directory where the file will be stored: ")
            print("------------------------------------------------------------")

        return file_path


if __name__ == '__main__':
    print("Hello this is Server")
    server()
