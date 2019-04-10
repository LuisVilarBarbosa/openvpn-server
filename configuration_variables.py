#!/usr/bin/python3
# coding=utf-8

# OpenVPN server installation script parameter settings

# How to use this file

# This file is designed to define a
# set of variables, which are below,
# that will be used to configure the
# OpenVPN server. Each variable has
# a description to help understanding
# its importance.
# Please, only update the values inside
# quotation marks.

# The name used to identify the specific OpenVPN server.
# Do not use spaces or special characters.
SERVER_NAME = "server"

# The port used by the OpenVPN server. 1194 and 1195 are
# the default ports.
# Be sure that the port is not in use.
SERVER_PORT = "1194"

# The protocol used by the OpenVPN server. It can be either
# UDP or TCP.
SERVER_PROTOCOL = "udp"

# The VPN subnet for OpenVPN to draw client addresses from.
# The server will take the first IPv4 address for itself,
# the rest will be made available to clients. Each client
# will be able to reach the server using the first IPv4
# address of the subnet.
OPENVPN_SUBNET = "10.8.0.0"
OPENVPN_SUBNET_MASK = "255.255.255.0"
OPENVPN_SUBNET_MASK_IN_BITS = "24"

# The ability to force all traffic to be redirected through
# the OpenVPN.
# Indicate 'yes' to redirect all traffic or indicate 'no'
# otherwise.
REDIRECT_ALL_TRAFFIC = "yes"

# The ability to block outside DNS servers on the client and
# only allow those provided by the OpenVPN server.
# If REDIRECT_ALL_TRAFFIC is set to 'no', this option should
# also be set to 'no'.
# Indicate 'yes' to block outside DNS servers or indicate 'no'
# otherwise.
BYPASS_DNS = "yes"

# The DNS servers provided to OpenVPN clients.
# All the IP addresses must be inside the square brackets and
# each IP address must be inside quotation marks and separated
# from the others by a comma and a space.
# You can provide as many DNS servers you want. Two are already
# defined for example purposes and refer to the public DNS
# servers provided by opendns.com.
DNS_SERVERS_ARRAY = ["208.67.222.222", "208.67.220.220"]

# The ability for OpenVPN clients to "see" each other.
# By default, clients will only see the server.
# To force clients to only see the server, you will also need
# to appropriately firewall the server's TUN/TAP interface.
# Indicate 'yes' to allow clients to "see" each other or
# indicate 'no' otherwise.
ALLOW_CLIENT_TO_CLIENT = "no"

# The ability to have multiple clients connected with the same
# certificate/key files or common names. This is recommended
# only for testing purposes. For production use, each client
# should have its own certificate/key pair.
# Indicate 'yes' to allow multiple clients connected with the same
# certificate/key files or common names or indicate 'no' otherwise.
ALLOW_DUPLICATE_CN = "no"

# The firewall protection mode you want to use to open access
# to OpenSSH and OpenVPN servers. It can be 'limit' or 'allow'.
# 'limit' protects the machine, but 'allow' is better when
# there are multiple connections in a short amount of time.
FIREWALL_MODE = "limit"

# The names of the different OpenVPN clients.
# Be sure that these client names are unique among all the OpenVPN
# servers installed on the machine or the old clients of any server
# with the same client name will be replaced by the new ones.
# All the names must be inside the square brackets and each name
# must be inside quotation marks and separated from the others
# by a comma and a space.
# Do not use spaces or special characters.
# You can create as many clients you want. Two are already
# defined for example purposes.
CLIENTS_ARRAY = ["client1", "client2"]

# The ability to activate the use of passwords for the different
# OpenVPN clients.
# These passwords are an extra security measure so that if
# someone has access to the certificate/key pair of a client,
# the password will also be needed to perform the connection.
# The password will be asked during the installation process.
# All the options must be inside the square brackets and each
# one must be inside quotation marks and separated from the
# others by a comma and a space.
# You must provide as many 'enable password' options as the clients
# in CLIENTS_ARRAY and each option will be relative to the client
# with the same index value. Two options are already defined for
# example purposes and should be updated.
# Indicate 'yes' to enable the use of a password for the corresponding
# client or indicate 'no' otherwise.
ENABLE_CLIENTS_PASSWORDS_ARRAY = ["yes", "no"]

# The addresses that the client will use to connect to the
# server. They can be DNS names, IPv4 addresses or IPv6
# addresses.
# All the addresses must be inside the square brackets and each
# address must be inside quotation marks and separated from
# the others by a comma and a space.
# You can provide as many addresses you want. Two are already
# defined for example purposes and should be replaced.
SERVER_ADDRESSES_ARRAY = ["example.com", "127.0.0.1"]

# The ports that the client will use to connect to the
# server.
# All the ports must be inside the square brackets and each
# port must be inside quotation marks and separated from
# the others by a comma and a space.
# You must provide as many ports as the addresses in
# SERVER_ADDRESSES_ARRAY and each port will be relative
# to the address with the same index value. Two ports are
# already defined for example purposes and should be replaced.
SERVER_PORTS_FOR_CLIENT_ARRAY = ["1194", "1194"]

# The ability for OpenVPN clients to choose randomly the
# address to which they will connect.
# This is useful to distribute the load between several addresses.
# Indicate 'yes' to enable the option or indicate 'no' otherwise.
ENABLE_REMOTE_RANDOM = "no"
