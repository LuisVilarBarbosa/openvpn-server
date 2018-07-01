#!/bin/sh

# Based on https://www.digitalocean.com/community/tutorials/how-to-set-up-an-openvpn-server-on-ubuntu-18-04

echo "This script will create an OpenVPN tunnel called 'server'. Press enter to continue..."
read -r DUMMY_VAR

# Preparing the instalation
INITIAL_PWD=$(pwd)
sudo apt-get update
sudo apt-get install -y ufw

# Step 1 — Installing OpenVPN and EasyRSA
sudo apt-get install -y openvpn
wget -P ~/ https://github.com/OpenVPN/easy-rsa/releases/download/v3.0.4/EasyRSA-3.0.4.tgz
cd ~
tar xvf EasyRSA-3.0.4.tgz

# Step 2 — Configuring the EasyRSA Variables and Building the CA
cd ~/EasyRSA-3.0.4/
cp vars.example vars
echo "Please update 'vars'. Press enter to perform the manual update."
read -r DUMMY_VAR
nano vars
./easyrsa init-pki
./easyrsa build-ca nopass

# Step 3 — Creating the Server Certificate, Key, and Encryption Files
cd EasyRSA-3.0.4/
./easyrsa init-pki
./easyrsa gen-req server nopass
sudo cp ~/EasyRSA-3.0.4/pki/private/server.key /etc/openvpn/
cd EasyRSA-3.0.4/
./easyrsa import-req ~/EasyRSA-3.0.4/pki/reqs/server.req server
./easyrsa sign-req server server
cp pki/issued/server.crt /tmp
cp pki/ca.crt /tmp
sudo cp /tmp/{server.crt,ca.crt} /etc/openvpn/
./easyrsa gen-dh
openvpn --genkey --secret ta.key
sudo cp ~/EasyRSA-3.0.4/ta.key /etc/openvpn/
sudo cp ~/EasyRSA-3.0.4/pki/dh.pem /etc/openvpn/

# Step 4 — Generating a Client Certificate and Key Pair
mkdir -p ~/client-configs/keys
chmod -R 700 ~/client-configs
cd ~/EasyRSA-3.0.4/
./easyrsa gen-req client1 nopass
cp pki/private/client1.key ~/client-configs/keys/
cp pki/reqs/client1.req /tmp
./easyrsa import-req /tmp/client1.req client1
./easyrsa sign-req client client1
cp pki/issued/client.crt /tmp
cp /tmp/client1.crt ~/client-configs/keys/
cp EasyRSA-3.0.4/ta.key ~/client-configs/keys/
sudo cp /etc/openvpn/ca.crt ~/client-configs/keys/

# Step 5 — Configuring the OpenVPN Service
sudo cp /usr/share/doc/openvpn/examples/sample-config-files/server.conf.gz /etc/openvpn/
sudo gzip -d /etc/openvpn/server.conf.gz
sudo perl -i -p -e "s|tls-auth ta.key 0 # This file is secret|tls-auth ta.key 0 # This file is secret\nkey-direction 0|" /etc/openvpn/server.conf
sudo perl -i -p -e "s|cipher AES-256-CBC|cipher AES-256-CBC\nauth SHA256|" /etc/openvpn/server.conf
sudo perl -i -p -e "s|dh*\n|dh dh.pem\n|" /etc/openvpn/server.conf
sudo perl -i -p -e "s|;user nobody|user nobody|" /etc/openvpn/server.conf
sudo perl -i -p -e "s|;group nogroup|group nogroup|" /etc/openvpn/server.conf

## (Optional) Push DNS Changes to Redirect All Traffic Through the VPN
sudo perl -i -p -e "s|\n*redirect gateway*\n|\npush \"redirect-gateway def1 bypass-dhcp bypass-dns\"\n|" /etc/openvpn/server.conf
sudo perl -i -p -e "s|;push \"dhcp-option DNS 208.67.222.222\"|push \"dhcp-option DNS 208.67.222.222\"|" /etc/openvpn/server.conf
sudo perl -i -p -e "s|;push \"dhcp-option DNS 208.67.220.220\"|push \"dhcp-option DNS 208.67.220.220\"|" /etc/openvpn/server.conf

## (Optional) Adjust the Port and Protocol
sudo perl -i -p -e "s|port 1194|port 1194|" /etc/openvpn/server.conf
sudo perl -i -p -e "s|proto udp|proto udp|" /etc/openvpn/server.conf
if [sudo cat /etc/openvpn/server.conf | grep proto == "proto tcp"]; then
    sudo perl -i -p -e "s|explicit-exit-notify 1|explicit-exit-notify 0|" /etc/openvpn/server.conf;
fi

# Step 6 — Adjusting the Server Networking Configuration
sudo perl -i -p -e "s|#net.ipv4.ip_forward=1|net.ipv4.ip_forward=1|" /etc/sysctl.conf
sudo sysctl -p
$BEFORE_RULES=$(sudo cat $INITIAL_PWD/before.rules)
sudo perl -i -p -e "s|# Don't delete these required lines, otherwise there will be errors|$BEFORE_RULES\n# Don't delete these required lines, otherwise there will be errors|" /etc/ufw/before.rules
sudo perl -i -p -e "s|DEFAULT_FORWARD_POLICY=\"DROP\"|DEFAULT_FORWARD_POLICY=\"ACCEPT\"|" /etc/default/ufw
sudo ufw limit 1194/udp  # MAYBE YOU WANT TO CHANGE "LIMIT" TO "ALLOW", IF YOU HAVE SEVERAL CONNECTIONS
sudo ufw limit OpenSSH   # MAYBE YOU WANT TO CHANGE "LIMIT" TO "ALLOW", IF YOU HAVE SEVERAL CONNECTIONS
sudo ufw disable
sudo ufw enable

# Step 7 — Starting and Enabling the OpenVPN Service
sudo systemctl start openvpn@server
sudo systemctl status openvpn@server
sudo systemctl enable openvpn@server

# Step 8 — Creating the Client Configuration Infrastructure
mkdir -p ~/client-configs/files
cp /usr/share/doc/openvpn/examples/sample-config-files/client.conf ~/client-configs/base.conf
sudo perl -i -p -e "s|\n*remote*\n|\nremote your_server_ip 1194\n|" ~/client-configs/base.conf  # UPDATE THIS LINE WITH THE NAME OR IP OF YOUR SERVER
sudo perl -i -p -e "s|proto udp|proto udp|" ~/client-configs/base.conf
sudo perl -i -p -e "s|;user nobody|user nobody|" ~/client-configs/base.conf
sudo perl -i -p -e "s|;group nogroup|group nogroup|" ~/client-configs/base.conf
sudo perl -i -p -e "s|ca ca.crt|#ca ca.crt|" ~/client-configs/base.conf
sudo perl -i -p -e "s|cert client.crt|#cert client.crt|" ~/client-configs/base.conf
sudo perl -i -p -e "s|key client.key|#key client.key|" ~/client-configs/base.conf
sudo perl -i -p -e "s|cipher AES-256-CBC|cipher AES-256-CBC\nauth SHA256\nkey-direction 1|" ~/client-configs/base.conf
sudo perl -i -p -e "s|key-direction 1|key-direction 1\n# script-security 2\n# up /etc/openvpn/update-resolv-conf\n# down /etc/openvpn/update-resolv-conf|" ~/client-configs/base.conf  # THIS COMMENTED LINES SHOULD BE UNCOMMENTED FOR LINUX CLIENTS
cp $INITIAL_PWD/make_config.sh ~/client-configs/make_config.sh
chmod 700 ~/client-configs/make_config.sh

# Step 9 — Generating Client Configurations
cd ~/client-configs
sudo ./make_config.sh client1
echo "The client confiuration file is placed on ~/client-configs/files/client1.ovpn"

# Undoing changes to the terminal status
cd $INITIAL_PWD
