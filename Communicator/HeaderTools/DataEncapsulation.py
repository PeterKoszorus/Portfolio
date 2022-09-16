# This file hold all the functions for creating fragments which will be later on sent
def create_header(flag, num_of_fragments, crc):
    if flag == 0:
        return create_fragment_header(flag)
    if flag == 1:
        # Sending message
        return create_fragment_header(flag, num_of_fragments, crc)
    if flag == 2:
        # Sending file
        return create_fragment_header(flag, num_of_fragments, crc)
    if flag == 3:
        # Informative header
        return create_fragment_header(flag, num_of_fragments, crc)
    if flag == 10:
        # Correct data was received
        return create_fragment_header(flag)
    if flag == 11:
        # Data was corrupted
        return create_fragment_header(flag)
    if flag == 20:
        # Communication ending
        return create_fragment_header(flag)
    if flag == 30:
        # Keep Alive
        return create_fragment_header(flag)


# Function which parses the header info from bytes back to other data types
def parse_header(header):
    # When fragment is without any data
    if len(header) == 8:
        flag = int.from_bytes(header[:1], byteorder="big")
        frag_order_num = int.from_bytes(header[2:4], byteorder="big")
        crc = int.from_bytes(header[4:], byteorder="big")
        return flag, frag_order_num, crc
    # Fragments carries data
    else:
        flag = int.from_bytes(header[:1], byteorder="big")
        frag_order_num = int.from_bytes(header[2:4], byteorder="big")
        crc = int.from_bytes(header[4:8], byteorder="big")
        data = header[8:]
        return flag, frag_order_num, crc, data


# Function which creates a communication init header
def create_fragment_header(flag, num_of_fragments=0, crc=0):

    return flag.to_bytes(1, byteorder="big") + num_of_fragments.to_bytes(3, byteorder="big") + \
           crc.to_bytes(4, byteorder="big")


# if __name__ == '__main__':
#     print(parse_header(create_header(1, 258)))
