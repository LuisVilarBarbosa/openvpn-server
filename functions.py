#!/usr/bin/python3
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
        if matches_regex("^([0-9]+)$", part) or matches_regex("^(-.*)", part) or matches_regex("(.*-)$", part):
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
    str_port = str(port)
    min_port = 0
    max_port = 65535
    if matches_regex("^([0-9]{1,5})$", str_port) and int_port >= min_port and int_port <= max_port:
        return True
    return False

def matches_regex(regex, string):
    if re.match(regex, string, 0) == None:
        return False
    return True

def execute_command(command_array, input_to_subprocess = None, collect_output = False):
    from subprocess import Popen, PIPE, STDOUT, CalledProcessError
    if input_to_subprocess == None:
        input_channel = None
    else:
        input_channel = PIPE
        input_to_subprocess = input_to_subprocess.encode()
    if collect_output:
        output_channel = PIPE
    else:
        output_channel = None
    p = Popen(command_array, stdin = input_channel, stdout = output_channel, stderr = output_channel)
    out, err = p.communicate(input = input_to_subprocess)
    if out != None:
        out = out.decode()
    if err != None:
        err = err.decode()
    if p.returncode != 0:
        raise CalledProcessError(p.returncode, command_array, out, err)
    return out, err

def replace_text_in_file(original_string, new_string, file_path):
    from errors import ReplacementError
    text = read_file(file_path)
    occurrences = text.count(original_string)
    if occurrences == 0:
        raise ReplacementError(file_path)
    text = text.replace(original_string, new_string)
    write_file(file_path, text)
    return occurrences

def read_file(file_path):
    f = open(file_path, 'r')
    text = f.read()
    f.close()
    return text

def write_file(file_path, text):
    f = open(file_path, 'w')
    f.write(text)
    f.close()

def chmod_recursive(path, mode):
    for root, dirs, files in os.walk(path):
        os.chmod(root, mode)
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

def get_default_network_device():
    from subprocess import check_output
    out, err = execute_command(command_array = ["ip", "route"], collect_output = True)
    ip_route = out
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
    return None

def move_content(src_folder, dst_folder):
    from shutil import move
    files = os.listdir(src_folder)
    for f in files:
        move(os.path.join(src_folder, f), os.path.join(dst_folder, f))

def get_python_version():
    from sys import version
    version_number = int(version[:version.find(".")])
    return version_number
