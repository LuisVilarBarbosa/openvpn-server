#!/usr/bin/python
# coding=utf-8

import configuration_variables
import functions

if not functions.matches_regex("^([a-zA-Z0-9_-]+)$", configuration_variables.SERVER_NAME):
    print("Invalid name: " + configuration_variables.SERVER_NAME)
    print("Please, do not use spaces or special characters.")
    quit()

if not functions.is_valid_port(configuration_variables.SERVER_PORT):
    quit()

configuration_variables.SERVER_PROTOCOL = configuration_variables.SERVER_PROTOCOL.lower()
if not functions.matches_regex("^(udp|tcp)$", configuration_variables.SERVER_PROTOCOL):
    print("Invalid protocol: " + configuration_variables.SERVER_PROTOCOL)
    quit()

if not functions.is_valid_ipv4_address(configuration_variables.OPENVPN_SUBNET):
    print("Invalid subnet: "  + configuration_variables.OPENVPN_SUBNET)
    quit()

if not functions.is_valid_ipv4_address(configuration_variables.OPENVPN_SUBNET_MASK):
    print("Invalid subnet mask: " + configuration_variables.OPENVPN_SUBNET_MASK)
    quit()

if not functions.matches_regex("^(yes|no)$", configuration_variables.BYPASS_DNS):
    print("Invalid 'bypass-dns' option: " + configuration_variables.BYPASS_DNS)
    quit()

for dns_server in configuration_variables.DNS_SERVERS_ARRAY:
    if not functions.is_valid_ipv4_address(dns_server) and not functions.is_valid_ipv6_address(dns_server):
        print("Invalid DNS server: " + dns_server)
        quit()

configuration_variables.ALLOW_CLIENT_TO_CLIENT = configuration_variables.ALLOW_CLIENT_TO_CLIENT.lower()
if not functions.matches_regex("^(yes|no)$", configuration_variables.ALLOW_CLIENT_TO_CLIENT):
    print("Invalid 'client-to-client' option: " + configuration_variables.ALLOW_CLIENT_TO_CLIENT)
    quit()

configuration_variables.ALLOW_DUPLICATE_CN = configuration_variables.ALLOW_DUPLICATE_CN.lower()
if not functions.matches_regex("^(yes|no)$", configuration_variables.ALLOW_DUPLICATE_CN):
    print("Invalid 'duplicate-cn' option: " + configuration_variables.ALLOW_DUPLICATE_CN)
    quit()

configuration_variables.FIREWALL_MODE = configuration_variables.FIREWALL_MODE.lower()
if not functions.matches_regex("^(limit|allow)$", configuration_variables.FIREWALL_MODE):
    print("Invalid mode: " + FIREWALL_MODE)
    quit()

for client in configuration_variables.CLIENTS_ARRAY:
    if not functions.matches_regex("^([a-zA-Z0-9_-]+)$", client):
        print("Invalid name: " + client)
        print("Please, do not use spaces or special characters.")
        quit()

if len(configuration_variables.CLIENTS_ARRAY) != len(configuration_variables.CLIENTS_PASSWORDS_ARRAY):
    print("The number of clients should be equal to the number of passwords.")
    quit()

for server_address in configuration_variables.SERVER_ADDRESSES_ARRAY:
    if not functions.is_valid_dns_name(server_address) and not functions.is_valid_ipv4_address(server_address)and not functions.is_valid_ipv6_address(server_address):
        print("Invalid address: " + server_address)
        print("It should be a DNS name, an IPv4 address or an IPv6 address.")
        quit()

if len(configuration_variables.SERVER_ADDRESSES_ARRAY) != len(configuration_variables.SERVER_PORTS_FOR_CLIENT_ARRAY):
    print("The number of server addresses should be equal to the number of server ports.")
    quit()
for server_port in configuration_variables.SERVER_PORTS_FOR_CLIENT_ARRAY:
    if not functions.is_valid_port(server_port):
        quit()

configuration_variables.ENABLE_REMOTE_RANDOM = configuration_variables.ENABLE_REMOTE_RANDOM.lower()
if not functions.matches_regex("^(yes|no)$", configuration_variables.ENABLE_REMOTE_RANDOM):
    print("Invalid 'remote-random' option: " + configuration_variables.ENABLE_REMOTE_RANDOM)
    quit()
