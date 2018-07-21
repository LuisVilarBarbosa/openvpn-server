# OpenVPN server

This repository contains the Python code necessary to configure an OpenVPN server.

The entry point to install the OpenVPN server is "install_openvpn_server.py".

This configuration is useful to create an OpenVPN server on hardware like a Raspberry Pi, that does not support software like pfSense, in a simple and fast manner and has some extra features not indicated in the Digital Ocean's tutorial like the ability to block the usage of DNS servers external to those indicated by the OpenVPN server which was an issue on Windows 10.

Be free to change this configuration to suit your needs and give suggestions or indicate issues.

To verify if everything is working, access /var/log/syslog and look at the messages written by "ovpn-*name_given_to_server*".

This configuration has been tested with success on Ubuntu Server 18.04, Debian Stretch 9.4.0 and Raspbian Stretch 9.4.

This configuration is originally based on:
- https://www.digitalocean.com/community/tutorials/how-to-set-up-an-openvpn-server-on-ubuntu-18-04

A little bit of history:
- Originally, this repository contained Bash scripts used to configure the OpenVPN servers, but because some mistakes were not being detected due to the nature of the Bash shell and because it was being necessary some complex Bash code to perform all the operations needed, the Bash code has been moved to Python.
