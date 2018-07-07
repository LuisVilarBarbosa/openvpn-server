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

# The VPN subnet for OpenVPN to draw client addresses from.
# The server will take the first IPv4 address for itself,
# the rest will be made available to clients. Each client
# will be able to reach the server using the first IPv4
# address of the subnet.
OPENVPN_SUBNET="10.8.0.0"
OPENVPN_SUBNET_MASK="255.255.255.0"

# The ability to block outside DNS servers on the client and
# only allow those provided by the OpenVPN server.
# Indicate 'yes' to block outside DNS servers or indicate 'no'
# otherwise.
BYPASS_DNS="yes"

# The DNS servers provided to OpenVPN clients.
# All the IP addresses must be inside the parenthesis and each
# IP address must be inside quotation marks and separated from
# the others by a space.
# You can provide as many DNS servers you want. Two are already
# defined for example purposes and refer to the public DNS
# servers provided by opendns.com.
DNS_SERVERS_ARRAY=("208.67.222.222" "208.67.220.220")

# The ability for OpenVPN clients to "see" each other.
# By default, clients will only see the server.
# To force clients to only see the server, you will also need
# to appropriately firewall the server's TUN/TAP interface.
# Indicate 'yes' to allow clients to "see" each other or
# indicate 'no' otherwise.
ALLOW_CLIENT_TO_CLIENT="no"

# The ability to have multiple clients connected with the same
# certificate/key files or common names. This is recommended
# only for testing purposes. For production use, each client
# should have its own certificate/key pair.
# Indicate 'yes' to allow multiple clients connected with the same
# certificate/key files or common names or indicate 'no' otherwise.
#
# IF YOU HAVE NOT GENERATED INDIVIDUAL
# CERTIFICATE/KEY PAIRS FOR EACH CLIENT,
# EACH HAVING ITS OWN UNIQUE "COMMON NAME",
# ENABLE THIS OPTION.
ALLOW_DUPLICATE_CN="no"

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
