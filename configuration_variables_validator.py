#!/usr/bin/python
# coding=utf-8

import configuration_variables
import functions
import ui

def validate_configuration_variables():
    validate_server_name()
    validate_server_port()
    validate_server_protocol()
    validate_openvpn_subnet()
    validate_openvpn_subnet_mask()
    validate_bypass_dns()
    validate_dns_servers_array()
    validate_allow_client_to_client()
    validate_allow_duplicate_cn()
    validate_firewall_mode()
    validate_clients_array()
    validate_enable_clients_passwords_array()
    validate_server_addresses_array()
    validate_server_ports_for_client_array()
    validate_enable_remote_random()

def validate_server_name():
    if not functions.matches_regex("^([a-zA-Z0-9_-]+)$", configuration_variables.SERVER_NAME):
        print("Invalid name: " + configuration_variables.SERVER_NAME)
        print("Please, do not use spaces or special characters.")
        quit()

def validate_server_port():
    ui.is_valid_port(configuration_variables.SERVER_PORT)

def validate_server_protocol():
    configuration_variables.SERVER_PROTOCOL = configuration_variables.SERVER_PROTOCOL.lower()
    if not functions.matches_regex("^(udp|tcp)$", configuration_variables.SERVER_PROTOCOL):
        print("Invalid protocol: " + configuration_variables.SERVER_PROTOCOL)
        quit()

def validate_openvpn_subnet():
    if not functions.is_valid_ipv4_address(configuration_variables.OPENVPN_SUBNET):
        print("Invalid subnet: "  + configuration_variables.OPENVPN_SUBNET)
        quit()

def validate_openvpn_subnet_mask():
    if not functions.is_valid_ipv4_address(configuration_variables.OPENVPN_SUBNET_MASK):
        print("Invalid subnet mask: " + configuration_variables.OPENVPN_SUBNET_MASK)
        quit()

def validate_bypass_dns():
    if not functions.matches_regex("^(yes|no)$", configuration_variables.BYPASS_DNS):
        print("Invalid 'bypass-dns' option: " + configuration_variables.BYPASS_DNS)
        quit()

def validate_dns_servers_array():
    for dns_server in configuration_variables.DNS_SERVERS_ARRAY:
        if not functions.is_valid_ipv4_address(dns_server) and not functions.is_valid_ipv6_address(dns_server):
            print("Invalid DNS server: " + dns_server)
            quit()

def validate_allow_client_to_client():
    configuration_variables.ALLOW_CLIENT_TO_CLIENT = configuration_variables.ALLOW_CLIENT_TO_CLIENT.lower()
    if not functions.matches_regex("^(yes|no)$", configuration_variables.ALLOW_CLIENT_TO_CLIENT):
        print("Invalid 'client-to-client' option: " + configuration_variables.ALLOW_CLIENT_TO_CLIENT)
        quit()

def validate_allow_duplicate_cn():
    configuration_variables.ALLOW_DUPLICATE_CN = configuration_variables.ALLOW_DUPLICATE_CN.lower()
    if not functions.matches_regex("^(yes|no)$", configuration_variables.ALLOW_DUPLICATE_CN):
        print("Invalid 'duplicate-cn' option: " + configuration_variables.ALLOW_DUPLICATE_CN)
        quit()

def validate_firewall_mode():
    configuration_variables.FIREWALL_MODE = configuration_variables.FIREWALL_MODE.lower()
    if not functions.matches_regex("^(limit|allow)$", configuration_variables.FIREWALL_MODE):
        print("Invalid mode: " + FIREWALL_MODE)
        quit()

def validate_clients_array():
    for client in configuration_variables.CLIENTS_ARRAY:
        if not functions.matches_regex("^([a-zA-Z0-9_-]+)$", client):
            print("Invalid name: " + client)
            print("Please, do not use spaces or special characters.")
            quit()

def validate_enable_clients_passwords_array():
    if len(configuration_variables.CLIENTS_ARRAY) != len(configuration_variables.ENABLE_CLIENTS_PASSWORDS_ARRAY):
        print("The number of clients should be equal to the number of password activation options.")
        quit()
    for i in range(len(configuration_variables.ENABLE_CLIENTS_PASSWORDS_ARRAY)):
        configuration_variables.ENABLE_CLIENTS_PASSWORDS_ARRAY[i] = configuration_variables.ENABLE_CLIENTS_PASSWORDS_ARRAY[i].lower()
        enable_password = configuration_variables.ENABLE_CLIENTS_PASSWORDS_ARRAY[i]
        if not functions.matches_regex("^(yes|no)$", enable_password):
            print("Invalid 'enable password' option: " + enable_password)
            quit()

def validate_server_addresses_array():
    for server_address in configuration_variables.SERVER_ADDRESSES_ARRAY:
        if not functions.is_valid_dns_name(server_address) and not functions.is_valid_ipv4_address(server_address)and not functions.is_valid_ipv6_address(server_address):
            print("Invalid address: " + server_address)
            print("It should be a DNS name, an IPv4 address or an IPv6 address.")
            quit()

def validate_server_ports_for_client_array():
    if len(configuration_variables.SERVER_ADDRESSES_ARRAY) != len(configuration_variables.SERVER_PORTS_FOR_CLIENT_ARRAY):
        print("The number of server addresses should be equal to the number of server ports.")
        quit()
    for server_port in configuration_variables.SERVER_PORTS_FOR_CLIENT_ARRAY:
        ui.is_valid_port(server_port)

def validate_enable_remote_random():
    configuration_variables.ENABLE_REMOTE_RANDOM = configuration_variables.ENABLE_REMOTE_RANDOM.lower()
    if not functions.matches_regex("^(yes|no)$", configuration_variables.ENABLE_REMOTE_RANDOM):
        print("Invalid 'remote-random' option: " + configuration_variables.ENABLE_REMOTE_RANDOM)
        quit()
