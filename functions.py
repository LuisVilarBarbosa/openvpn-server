#!/usr/bin/python
# coding=utf-8

import os
import re

def is_valid_dns_name(dns_name):
    if not matches_regex("^([0-9a-zA-Z-]+(\.[0-9a-zA-Z-]+)*)$", dns_name):
        return False
    if not matches_regex("^(.{1,63})$", dns_name):
        return False
    dns_name_parts = dns_name.split(".")
    for part in dns_name_parts:
        if matches_regex("^([0-9]+)$", part) or matches_regex("^(-)", part) or matches_regex("(-)$", part):
            return False
    return True

def is_valid_ipv4_address(ipv4_address):
    if not matches_regex("^([0-9]{1,3}(\.[0-9]{1,3}){3})$", ipv4_address):
        return False
    ipv4_address_parts = ipv4_address.split(".")
    for part in ipv4_address_parts:
        int_part = int(part)
        if int_part < 0 or int_part > 255:
            return False
    return True

def is_valid_ipv6_address(ipv6_address):
    if matches_regex("^([0-9a-fA-F]{4}(:[0-9a-fA-F]{4}){4})$", ipv6_address):
        return True
    return False

def is_valid_port(port):
    int_port = int(port)
    min_port = 0
    max_port = 65535
    if matches_regex("^([0-9]{1,5})$", str(port)) and int_port >= min_port and int_port <= max_port:
        return True
    print("Invalid port: " + port)
    print("It should be between " + str(min_port) + " and " + str(max_port) + ".")
    return False

def matches_regex(regex, string):
    if re.match(regex, string, 0) == None:
        return False
    return True

def execute_command(command_array):
    from subprocess import check_call, CalledProcessError
    #print("Executing: " + str(command_array))
    try:
        check_call(command_array)
    except CalledProcessError:
        print("An error occurred while running the following program: " + str(command_array))
        quit()

def replace_text_in_file(original_string, new_string, file_path):
    text = read_file(file_path)
    text = text.replace(original_string, new_string)
    f = open(file_path, 'w')
    f.write(text)
    f.close()

def read_file(file_path):
    f = open(file_path, 'r')
    text = f.read()
    f.close()
    return text

def execute_and_send_input_to_command(command_array, input_to_subprocess):
    from subprocess import Popen, PIPE
    #print("Executing: " + str(command_array))
    p = Popen(command_array, stdin = PIPE)
    p.communicate(input = input_to_subprocess.encode())
    if p.returncode != 0:
        print("An error occurred while running the following program: " + str(command_array))
        quit()

def chmod_recursive(path, mode):
    for root, dirs, files in os.walk(path):
        for d in dirs:
            os.chmod(os.path.join(root, d), mode)
        for f in files:
            os.chmod(os.path.join(root, f), mode)

def decompress_gzip_file(file_path):
    from gzip import GzipFile
    if not file_path.endswith(".gz"):
        raise InvalidArgumentException
    inF = GzipFile(file_path, 'rb')
    data = inF.read()
    inF.close()
    new_file_path = file_path[:len(file_path)-3]
    outF = open(new_file_path, 'wb')
    outF.write(data)
    outF.close()

def makedirs(path, mode = 0o777):
    try:
        os.makedirs(path, mode)
    except FileExistsError:
        pass

def get_command_output(command_array):
    from subprocess import check_output, CalledProcessError
    #print("Executing: " + str(command_array))
    try:
        return str(check_output(command_array))
    except CalledProcessError:
        print("An error occurred while running the following program: " + str(command_array))
        quit()

def get_default_network_device():
    from subprocess import check_output
    ip_route = get_command_output(["ip", "route"])
    ip_route_lines = ip_route.splitlines()
    for line in ip_route_lines:
        if line.find("default") != -1:
            line_parts = line.split(" ")
            dev_found = False
            for line_part in line_parts:
                if dev_found:
                    return line_part
                elif line_part == "dev":
                    dev_found = True
    print("No default network device found.")
    quit()

def move_content(src_folder, dst_folder):
    from shutil import move
    files = os.listdir(src_folder)
    for f in files:
        move(os.path.join(src_folder, f), os.path.join(dst_folder, f))

def verify_python_version():
    from sys import version
    version_number = int(version[:version.find(".")])
    if version_number < 3:
        print("Please use Python3 or higher.")
        quit()
