# OpenVPN server

This repository contains the necessary instructions to configure an OpenVPN server.

The entry point to install the OpenVPN server is "install_openvpn_server.py".

This configuration is useful to create an OpenVPN server on hardware like a Raspberry Pi, that does not support software like pfSense, in a simple and fast manner and has some extra features not indicated in the Digital Ocean's tutorial like the ability to block the usage of DNS servers external to those indicated by the OpenVPN server which was an issue on Windows 10.

Be free to change this configuration to suit your needs and give suggestions or indicate issues.

To verify if everything is working, access /var/log/syslog and look at the messages written by "ovpn-*name_given_to_server*".

This configuration has been tested with success on Ubuntu Server 18.04, Debian Stretch 9.4.0 and Raspbian Stretch 9.4.

This configuration is originally based on:
- https://www.digitalocean.com/community/tutorials/how-to-set-up-an-openvpn-server-on-ubuntu-18-04
