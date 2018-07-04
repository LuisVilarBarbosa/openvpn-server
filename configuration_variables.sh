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
SERVER_NAME="server"

# The address that the client will use to connect to the
# server. It can be a DNS name, an IPv4 address or an IPv6
# address.
SERVER_ADDRESS="example.com"

# The port used by the OpenVPN server. 1194 and 1195 are
# the default ports.
# Be sure that the port is not in use.
SERVER_PORT="1194"

# The protocol used by the OpenVPN server. It can be either
# UDP or TCP.
SERVER_PROTOCOL="udp"

# The firewall protection mode you want to use to open access
# to OpenSSH and OpenVPN servers. It can be 'limit' or 'allow'.
# 'limit' protects the machine, but 'allow' is better when
# there are multiple connections in a short amount of time.
FIREWALL_MODE="limit"

# The names of the different OpenVPN clients.
# All the names must be inside the parenthesis and each name
# must be inside quotation marks and separated from the others
# by a space.
# Do not use spaces or special characters.
# You can create as many clients you want. Two are already
# defined for example purposes.
CLIENTS_ARRAY=("client1" "client2")
