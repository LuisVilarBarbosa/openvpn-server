#!/usr/bin/python
# coding=utf-8

import functions

def is_valid_dns_name(dns_name):
    return functions.is_valid_dns_name(dns_name)

def is_valid_ipv4_address(ipv4_address):
    return functions.is_valid_ipv4_address(ipv4_address)

def is_valid_ipv6_address(ipv6_address):
    return functions.is_valid_ipv6_address(ipv6_address)

def is_valid_port(port):
    is_valid_port = functions.is_valid_port(port)
    if not is_valid_port:
        print("Invalid port: " + str(port))
        quit()
    return is_valid_port

def matches_regex(regex, string):
    return functions.matches_regex(regex, string)

def execute_command(command_array):
    from subprocess import CalledProcessError
    #print("Executing: " + str(command_array))
    try:
        functions.execute_command(command_array)
    except CalledProcessError:
        print("An error occurred while running the following program: " + str(command_array))
        quit()

def replace_text_in_file(original_string, new_string, file_path):
    return functions.replace_text_in_file(original_string, new_string, file_path)

def read_file(file_path):
    return functions.read_file(file_path)

def write_file(file_path, text):
    return functions.write_file(file_path, text)

def execute_and_send_input_to_command(command_array, input_to_subprocess):
    #print("Executing: " + str(command_array))
    returncode = functions.execute_and_send_input_to_command(command_array, input_to_subprocess)
    if returncode != 0:
        print("An error occurred while running the following program: " + str(command_array))
        quit()

def chmod_recursive(path, mode):
    functions.chmod_recursive(path, mode)

def decompress_gzip_file(file_path):
    functions.decompress_gzip_file(file_path)

def makedirs(path, mode = 0o777):
    functions.makedirs(path, mode)

def get_command_output(command_array):
    from subprocess import CalledProcessError
    #print("Executing: " + str(command_array))
    try:
        return functions.get_command_output(command_array)
    except CalledProcessError:
        print("An error occurred while running the following program: " + str(command_array))
        quit()

def get_default_network_device():
    default_network_device = functions.get_default_network_device()
    if default_network_device == None:
        print("No default network device found.")
        quit()
    else:
        return default_network_device

def move_content(src_folder, dst_folder):
    functions.move_content(src_folder, dst_folder)

def verify_python_version():
    version_number = int(functions.get_python_version())
    if version_number < 3:
        print("Please use Python3 or higher.")
        quit()
