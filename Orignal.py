import socket
call_sign = "KE7DHQ"

HOST = "127.0.0.1"  # The server's hostname or IP address
HARDLINE_PORT = 9012  # The port used by the server
RADIO_PORT = 9020

def get_header(function_id, openlst_length, ccds_length, hardline, apid=0): #function_id is the function id of the command
    packet = b''
    if hardline != 'y' and hardline != 'yes':
        packet += int(8809).to_bytes(2, byteorder='big') #OPENLSTSTARTSEQ

        packet += int(openlst_length).to_bytes(1, byteorder='big') #OPENLSTLENGTH

        packet += int(10960).to_bytes(2, byteorder='big') #OPENLSTDESTINATION

        packet += int(0).to_bytes(2, byteorder='big') #OPENLSTSEQNUM

        packet += int(0).to_bytes(1, byteorder='big') #OPENLSTSYSTEMBYTE

        string_bytes = call_sign.encode('utf-8') #converting the callsign
        packet += string_bytes #CALLSIGN

    packet += int(892270675).to_bytes(4, byteorder='big') #DORASYNCBYTES

    packet += int(apid).to_bytes(2, byteorder='big') #CCSDSVER + CCSDSTYPE + CCSDSSHF + CCSDSAPID

    seq_flags_and_seq = (3 & 0b11) << 14 | (0 & 0b11111111111111) #SEQFLAGS + SEQ
    packet += seq_flags_and_seq.to_bytes(2, byteorder='big') #CCSDSSEQ

    print("CCSDSLENGTH: ", ccds_length)
    packet += int(ccds_length).to_bytes(2, byteorder='big') #CCSDSLENGTH

    packet += int(function_id).to_bytes(1, byteorder='big') #FUNCTIONID

    return packet

def schedule_command(hardline):
    execution_timestamp = int(input("execution timestamp: ")) # input would look like: "1000"
    apid = int(input("APID: ")) # input would look like: "1"
    function_id = int(input("function id: ")) # input would look like: "4"
    command_payload = input("command payload: ") # input would look like: "5523"    
    command_payload = bytes.fromhex(command_payload) #converting the command payload to bytes

    openlst_length = 264 / 8 + len(command_payload)
    print("openlst_length: ", openlst_length)

    CCSDSLENGTH = (96 / 8 + len(command_payload)) - 1

    packet = get_header(3, openlst_length, CCSDSLENGTH, hardline) #5 is the function id of the command

    packet += int(execution_timestamp).to_bytes(8, byteorder='big') #Execution_Timestamp

    packet += int(apid).to_bytes(2, byteorder='big') #APID

    packet += int(function_id).to_bytes(1, byteorder='big') #FUNCTION_ID

    packet += command_payload #COMMAND_PAYLOAD
    print(''.join(f'{byte:02x} ' for byte in packet))

    return packet

def run_bash_command(hardline):
    return_output = int(input("return output: ")) # input would look like: "0" for no output, "1" for output
    command_payload = input("command: ") # input would look like: "ls -l"    
    command_payload = command_payload.encode("utf-8") #converting the command payload to bytes

    openlst_length = 184 / 8 + len(command_payload)
    print("openlst_length: ", openlst_length)

    CCSDSLENGTH = (16 / 8 + len(command_payload)) - 1

    packet = get_header(9, openlst_length, CCSDSLENGTH, hardline) # 9 is the function id of the command

    packet += int(return_output).to_bytes(1, byteorder='big') #FUNCTION_ID

    packet += command_payload #COMMAND_PAYLOAD
    print(''.join(f'{byte:02x} ' for byte in packet))
    
    return packet

def i2c_raw_command(hardline):
    i2c_address = input("i2c address: ") # input would look like: "0x1E"
    i2c_address = bytes.fromhex(i2c_address)
    bytes_to_return = int(input("bytes to return: ")) # input would look like: "1"
    i2c_command = input("i2c data: ") # input would look like: "5523"
    i2c_command = bytes.fromhex(i2c_command) #converting the i2c data to bytes

    openlst_length = 208 / 8 + len(i2c_command)
    print("openlst_length: ", openlst_length)

    CCSDSLENGTH = (40 / 8 + len(i2c_command)) - 1

    packet = get_header(4, openlst_length, CCSDSLENGTH, hardline) # 4 is the function id of the command

    packet += bytes.fromhex("00") + i2c_address #I2C_ADDRESS
    packet += int(bytes_to_return).to_bytes(2, byteorder='big') #I2C_BYTES_TO_RETURN

    packet += i2c_command #I2C_DATA
    print(''.join(f'{byte:02x} ' for byte in packet))

    return packet


def adcs_set_config(hardline):
    cube_acp_set_id = int(input("cube_acp_set_id: "))
    config_data = input("config_data: ")
    config_data = bytes.fromhex(config_data)

    openlst_length = 184 / 8 + len(config_data)
    print("openlst_length: ", openlst_length)

    CCSDSLENGTH = (1 + len(config_data))

    packet = get_header(16, openlst_length, CCSDSLENGTH, hardline, apid=2) # 4 is the function id of the command

    packet += cube_acp_set_id.to_bytes(1, 'big')
    packet += config_data

    print(''.join(f'{byte:02x} ' for byte in packet))

    return packet


def file_burst_transfer_request(hardline):
    file_bytes_offset = int(input("file_bytes_offset: "))
    length = int(input("length: "))
    segment_length = int(input("segment_length: "))
    acknowledgements = int(input("acknowledgements (0 for no, 1 for yes): "))
    file_path = input("file path: ")
    file_path = file_path.encode("utf-8")

    openlst_length = 40 + len(file_path)
    print("openlst_length: ", openlst_length)

    CCSDSLENGTH = (18 + len(file_path))

    packet = get_header(18, openlst_length, CCSDSLENGTH, hardline, apid=0)

    packet += file_bytes_offset.to_bytes(8, 'big')
    packet += length.to_bytes(8, 'big')
    packet += segment_length.to_bytes(1, 'big')
    packet += acknowledgements.to_bytes(1, 'big')
    packet += file_path

    print(''.join(f'{byte:02x} ' for byte in packet))

    return packet


def file_upload_packet(hardline):
    file_path = input("file_path: ")
    file_path = file_path.encode("utf-8")
    file_path_length = len(file_path)

    file_data = input("file_data: ") # input would look like: "5523"
    file_data = bytes.fromhex(file_data) #converting the i2c data to bytes

    # 4 bytes for path name length, then dynamic
    openlst_length = 26 + file_path_length + len(file_data)
    print("openlst_length: ", openlst_length)

    CCSDSLENGTH = (4 + file_path_length + len(file_data))

    packet = get_header(26, openlst_length, CCSDSLENGTH, hardline, apid=0)

    packet += file_path_length.to_bytes(4, 'big')
    packet += file_path
    packet += file_data

    print(''.join(f'{byte:02x} ' for byte in packet))

    return packet


def ls_files_from_directory(hardline):
    file_path = input("file_path: ")
    file_path = file_path.encode("utf-8")

    # 4 bytes for path name length, then dynamic
    openlst_length = 22 + len(file_path)
    print("openlst_length: ", openlst_length)

    CCSDSLENGTH = len(file_path)

    packet = get_header(22, openlst_length, CCSDSLENGTH, hardline, apid=0)

    packet += file_path

    print(''.join(f'{byte:02x} ' for byte in packet))

    return packet


def get_file_size(hardline):
    file_path = input("file_path: ")
    file_path = file_path.encode("utf-8")

    # 4 bytes for path name length, then dynamic
    openlst_length = 22 + len(file_path)
    print("openlst_length: ", openlst_length)

    CCSDSLENGTH = len(file_path)

    packet = get_header(27, openlst_length, CCSDSLENGTH, hardline, apid=0)

    packet += file_path

    print(''.join(f'{byte:02x} ' for byte in packet))

    return packet


def main():
    print("1. Schedule Command")
    print("2. Run Bash Command")
    print("3. I2C Raw Command")
    print("4. adcs_set_config")
    print("5. file_burst_transfer_request")
    print("6. file_upload_packet")
    print("7. ls_files_from_directory")
    print("8. get_file_size")
    choice = int(input("Enter your choice: "))
    hardline = input("Send over hardline?: ")

    packet = b''
    if choice == 1:
        packet = schedule_command(hardline)
    elif choice == 2:
        packet = run_bash_command(hardline)
    elif choice == 3:
        packet = i2c_raw_command(hardline)
    elif choice == 4:
        packet = adcs_set_config(hardline)
    elif choice == 5:
        packet = file_burst_transfer_request(hardline)
    elif choice == 6:
        packet = file_upload_packet(hardline)
    elif choice == 7:
        packet = ls_files_from_directory(hardline)
    elif choice == 8:
        packet = get_file_size(hardline)
    else:
        print("Invalid choice")


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if hardline == 'y' or hardline == 'yes':
            print("send over hardline")
            s.connect((HOST, HARDLINE_PORT))
            s.sendto(packet, (HOST, HARDLINE_PORT))
            s.close()
        else:
            s.connect((HOST, RADIO_PORT))
            s.sendto(packet, (HOST, RADIO_PORT))
            s.close()
    
main()