#!/bin/bash

# Originally based on https://www.digitalocean.com/community/tutorials/how-to-set-up-an-openvpn-server-on-ubuntu-18-04

SCRIPT_FILENAME=$0

# Verify which shell is running this script

## Based on https://unix.stackexchange.com/questions/71121/determine-shell-in-script-during-runtime
if test -n "$ZSH_VERSION"; then
  PROFILE_SHELL=zsh
elif test -n "$BASH_VERSION"; then
  PROFILE_SHELL=bash
elif test -n "$KSH_VERSION"; then
  PROFILE_SHELL=ksh
elif test -n "$FCEDIT"; then
  PROFILE_SHELL=ksh
elif test -n "$PS3"; then
  PROFILE_SHELL=unknown
else
  PROFILE_SHELL=sh
fi

if [ $PROFILE_SHELL != "bash" ]; then
  echo "Changing to Bash shell."
  sudo su -c "bash $SCRIPT_FILENAME"
  exit
fi

# Verify if this script is running as root

if [ "$(id -u)" != "0" ]; then
  echo "Running this script as root."
  sudo su -c "bash $SCRIPT_FILENAME"
  exit
fi

# Print initialization messages

echo "This script will create an OpenVPN tunnel."
echo "Pay attention to the output for errors or warnings."
echo "Trying to replace an already existing server with the same name will not work correctly. The client configuration files of the original server would work and the ones for the new server would not work."
echo "Press enter to continue..."
read -r DUMMY_VAR

# Load functions

is_valid_dns_name_fun () {
  dns_name=$1
  if [[ ! $dns_name =~ ^([0-9a-zA-Z-]+(\.[0-9a-zA-Z-]+)*)$ ]]; then
    return 0
  fi
  if [[ ! $dns_name =~ ^(.{1,63})$ ]]; then
    return 0
  fi
  OIFS=$IFS  # Internal_field_separator
  IFS="."
  for part in $dns_name; do
    if [[ $part =~ ^([0-9]+)$ || $part =~ ^(-) || $part =~ (-)$ ]]; then
      IFS=OIFS
      return 0
    fi
  done
  IFS=OIFS
  return 1
}

is_valid_ipv4_address_fun () {
  ipv4_address=$1
  if [[ ! $ipv4_address =~ ^([0-9]{1,3}(\.[0-9]{1,3}){3})$ ]]; then
    return 0
  fi
  OIFS=$IFS  # Internal_field_separator
  IFS="."
  for part in $ipv4_address; do
    if [[ $part < 0 || $part > 255 ]]; then
      IFS=OIFS
      return 0
    fi
  done
  IFS=OIFS
  return 1
}

is_valid_ipv6_address_fun () {
  ipv6_address=$1
  if [[ $ipv6_address =~ ^([0-9a-fA-F]{4}(:[0-9a-fA-F]{4}){4})$ ]]; then
    return 1
  fi
  return 0
}

# Preparing the instalation
INITIAL_PWD=$(pwd)
INSTALLATION_DIR="/openvpn_instalation"  # This variable is repeated on 'make_config.sh'
mkdir -p $INSTALLATION_DIR

cp $INITIAL_PWD/configuration_variables.sh $INSTALLATION_DIR
echo "Please update the variables inside 'configuration_variables.sh'."
echo "Press enter to perform the manual update."
read -r DUMMY_VAR
nano $INSTALLATION_DIR/configuration_variables.sh
source $INSTALLATION_DIR/configuration_variables.sh

if [[ ! $SERVER_NAME =~ ^([a-zA-Z0-9_-]+)$ ]]; then
  echo "Invalid name: $SERVER_NAME"
  echo "Please, do not use spaces or special characters."
  exit
fi

is_valid_dns_name_fun $SERVER_ADDRESS
is_valid_dns_name=$?
is_valid_ipv4_address_fun $SERVER_ADDRESS
is_valid_ipv4_address=$?
is_valid_ipv6_address_fun $SERVER_ADDRESS
is_valid_ipv6_address=$?
if [[ is_valid_dns_name == 0 && is_valid_ipv4_address == 0 && is_valid_ipv6_address == 0 ]]; then
  echo "Invalid address: $SERVER_ADDRESS"
  echo "It should be a DNS name, an IPv4 address or an IPv6 address."
  exit
fi

MIN_PORT=0
MAX_PORT=65535
if [[ ! $SERVER_PORT =~ ^([0-9]{1,5})$ || ! $SERVER_PORT -ge $MIN_PORT || ! $SERVER_PORT -le $MAX_PORT ]]; then
  echo "Invalid port: $SERVER_PORT"
  echo "It should be between $MIN_PORT and $MAX_PORT."
  exit
fi

SERVER_PROTOCOL=${SERVER_PROTOCOL,,} # Changes all characters to lowercase
if [[ ! $SERVER_PROTOCOL =~ ^(udp|tcp)$ ]]; then
  echo "Invalid protocol: $SERVER_PROTOCOL"
  exit
fi

is_valid_ipv4_address_fun $OPENVPN_SUBNET
is_valid_ipv4_address=$?
if [[ is_valid_ipv4_address == 0 ]]; then
  echo "Invalid subnet: $OPENVPN_SUBNET"
  exit
fi

is_valid_ipv4_address_fun $OPENVPN_SUBNET_MASK
is_valid_ipv4_address=$?
if [[ is_valid_ipv4_address == 0 ]]; then
  echo "Invalid subnet mask: $OPENVPN_SUBNET_MASK"
  exit
fi

if [[ ! $BYPASS_DNS =~ ^(yes|no)$ ]]; then
  echo "Invalid 'bypass-dns' option: $BYPASS_DNS"
  exit
fi

is_valid_ipv4_address_fun $dns_server
is_valid_ipv4_address=$?
is_valid_ipv6_address_fun $dns_server
is_valid_ipv6_address=$?
for dns_server in ${DNS_SERVERS_ARRAY[*]}; do
  if [[ is_valid_ipv4_address == 0  && is_valid_ipv6_address == 0 ]]; then
    echo "Invalid DNS server: $dns_server"
    exit
  fi
done

ALLOW_CLIENT_TO_CLIENT=${ALLOW_CLIENT_TO_CLIENT,,} # Changes all characters to lowercase
if [[ ! $ALLOW_CLIENT_TO_CLIENT =~ ^(yes|no)$ ]]; then
  echo "Invalid 'client-to-client' option: $ALLOW_CLIENT_TO_CLIENT"
  exit
fi

ALLOW_DUPLICATE_CN=${ALLOW_DUPLICATE_CN,,} # Changes all characters to lowercase
if [[ ! $ALLOW_DUPLICATE_CN =~ ^(yes|no)$ ]]; then
  echo "Invalid 'duplicate-cn' option: $ALLOW_DUPLICATE_CN"
  exit
fi

FIREWALL_MODE=${FIREWALL_MODE,,} # Changes all characters to lowercase
if [[ ! $FIREWALL_MODE =~ ^(limit|allow)$ ]]; then
  echo "Invalid mode: $FIREWALL_MODE"
  exit
fi

for client in ${CLIENTS_ARRAY[*]}; do
  if [[ ! $client =~ ^([a-zA-Z0-9_-]+)$ ]]; then
    echo "Invalid name: $client"
    echo "Please, do not use spaces or special characters."
    exit
  fi
done

apt-get update
apt-get install -y ufw

# Step 1 — Installing OpenVPN and EasyRSA
apt-get install -y openvpn
wget -P $INSTALLATION_DIR/ https://github.com/OpenVPN/easy-rsa/releases/download/v3.0.4/EasyRSA-3.0.4.tgz
cd $INSTALLATION_DIR
tar xf EasyRSA-3.0.4.tgz

# Step 2 — Configuring the EasyRSA Variables and Building the CA
cd $INSTALLATION_DIR/EasyRSA-3.0.4/
cp vars.example vars
perl -i -p -e "s|#set_var EASYRSA_REQ_COUNTRY|set_var EASYRSA_REQ_COUNTRY|" $INSTALLATION_DIR/EasyRSA-3.0.4/vars
perl -i -p -e "s|#set_var EASYRSA_REQ_PROVINCE|set_var EASYRSA_REQ_PROVINCE|" $INSTALLATION_DIR/EasyRSA-3.0.4/vars
perl -i -p -e "s|#set_var EASYRSA_REQ_CITY|set_var EASYRSA_REQ_CITY|" $INSTALLATION_DIR/EasyRSA-3.0.4/vars
perl -i -p -e "s|#set_var EASYRSA_REQ_ORG|set_var EASYRSA_REQ_ORG|" $INSTALLATION_DIR/EasyRSA-3.0.4/vars
perl -i -p -e "s|#set_var EASYRSA_REQ_EMAIL|set_var EASYRSA_REQ_EMAIL|" $INSTALLATION_DIR/EasyRSA-3.0.4/vars
perl -i -p -e "s|#set_var EASYRSA_REQ_OU|set_var EASYRSA_REQ_OU|" $INSTALLATION_DIR/EasyRSA-3.0.4/vars
echo "Please update the following variables inside 'vars':"
echo " - EASYRSA_REQ_COUNTRY"
echo " - EASYRSA_REQ_PROVINCE"
echo " - EASYRSA_REQ_CITY"
echo " - EASYRSA_REQ_ORG"
echo " - EASYRSA_REQ_EMAIL"
echo " - EASYRSA_REQ_OU"
echo "Press enter to perform the manual update."
read -r DUMMY_VAR
nano vars
echo "yes" | ./easyrsa init-pki
echo "" | ./easyrsa build-ca nopass

# Step 3 — Creating the Server Certificate, Key, and Encryption Files
cd $INSTALLATION_DIR/EasyRSA-3.0.4/
echo "" | ./easyrsa gen-req $SERVER_NAME nopass
cp $INSTALLATION_DIR/EasyRSA-3.0.4/pki/private/$SERVER_NAME.key /etc/openvpn/
echo "yes" | ./easyrsa sign-req server $SERVER_NAME
cp pki/issued/$SERVER_NAME.crt /tmp
cp pki/ca.crt /tmp
cp /tmp/{$SERVER_NAME.crt,ca.crt} /etc/openvpn/
./easyrsa gen-dh
openvpn --genkey --secret ta.key
cp $INSTALLATION_DIR/EasyRSA-3.0.4/ta.key /etc/openvpn/
cp $INSTALLATION_DIR/EasyRSA-3.0.4/pki/dh.pem /etc/openvpn/

# Step 4 — Generating a Client Certificate and Key Pair
mkdir -p $INSTALLATION_DIR/client-configs/keys
chmod -R 700 $INSTALLATION_DIR/client-configs
cd $INSTALLATION_DIR/EasyRSA-3.0.4/
for client in ${CLIENTS_ARRAY[*]}; do
  echo "" | ./easyrsa gen-req $client nopass
  cp pki/private/$client.key $INSTALLATION_DIR/client-configs/keys/
  echo "yes" | ./easyrsa sign-req client $client
  cp pki/issued/$client.crt $INSTALLATION_DIR/client-configs/keys/
done
cp $INSTALLATION_DIR/EasyRSA-3.0.4/ta.key $INSTALLATION_DIR/client-configs/keys/
cp /etc/openvpn/ca.crt $INSTALLATION_DIR/client-configs/keys/

# Step 5 — Configuring the OpenVPN Service
cp /usr/share/doc/openvpn/examples/sample-config-files/server.conf.gz /etc/openvpn/$SERVER_NAME.conf.gz
gzip -d /etc/openvpn/$SERVER_NAME.conf.gz
perl -i -p -e "s|tls-auth ta.key 0 # This file is secret|tls-auth ta.key 0 # This file is secret\nkey-direction 0|" /etc/openvpn/$SERVER_NAME.conf
perl -i -p -e "s|cipher AES-256-CBC|cipher AES-256-CBC\nauth SHA256|" /etc/openvpn/$SERVER_NAME.conf
perl -i -p -e "s|dh dh2048.pem|dh dh.pem|" /etc/openvpn/$SERVER_NAME.conf
perl -i -p -e "s|;user nobody|user nobody|" /etc/openvpn/$SERVER_NAME.conf
perl -i -p -e "s|;group nogroup|group nogroup|" /etc/openvpn/$SERVER_NAME.conf

## (Optional) Push DNS Changes to Redirect All Traffic Through the VPN
if [[ $BYPASS_DNS == "yes" ]]; then
  perl -i -p -e "s|;push \"redirect-gateway def1 bypass-dhcp\"|push \"redirect-gateway def1 bypass-dhcp bypass-dns\"|" /etc/openvpn/$SERVER_NAME.conf
elif [[ $BYPASS_DNS == "no" ]]; then
  perl -i -p -e "s|;push \"redirect-gateway def1 bypass-dhcp\"|push \"redirect-gateway def1 bypass-dhcp\"|" /etc/openvpn/$SERVER_NAME.conf
fi
DHCP_OPTION_DNS_FULL=""
for dns_server in ${DNS_SERVERS_ARRAY[*]}; do
  DHCP_OPTION_DNS_PART="push \"dhcp-option DNS $dns_server\"\n"
  DHCP_OPTION_DNS_FULL="$DHCP_OPTION_DNS_FULL$DHCP_OPTION_DNS_PART"
done
perl -i -p -e "s|;push \"dhcp-option DNS 208.67.222.222\"\n||" /etc/openvpn/$SERVER_NAME.conf
perl -i -p -e "s|;push \"dhcp-option DNS 208.67.220.220\"\n|$DHCP_OPTION_DNS_FULL|" /etc/openvpn/$SERVER_NAME.conf

## (Optional) Adjust the Port and Protocol
perl -i -p -e "s|port 1194|port $SERVER_PORT|" /etc/openvpn/$SERVER_NAME.conf
perl -i -p -e "s|;proto tcp\n||" /etc/openvpn/$SERVER_NAME.conf
perl -i -p -e "s|proto udp|proto $SERVER_PROTOCOL|" /etc/openvpn/$SERVER_NAME.conf
if [[ $SERVER_PROTOCOL == "tcp" ]]; then
    perl -i -p -e "s|explicit-exit-notify 1|explicit-exit-notify 0|" /etc/openvpn/$SERVER_NAME.conf
fi

## (Optional) Point to Non-Default Credentials
perl -i -p -e "s|cert server.crt|cert $SERVER_NAME.crt|" /etc/openvpn/$SERVER_NAME.conf
perl -i -p -e "s|key server.key|key $SERVER_NAME.key|" /etc/openvpn/$SERVER_NAME.conf

## Some of the extra adjustments not indicated in the Digital Ocean tutorial
perl -i -p -e "s|server 10.8.0.0 255.255.255.0|server $OPENVPN_SUBNET $OPENVPN_SUBNET_MASK|" /etc/openvpn/$SERVER_NAME.conf
if [[ $ALLOW_CLIENT_TO_CLIENT == "yes" ]]; then
  perl -i -p -e "s|;client-to-client|client-to-client|" /etc/openvpn/$SERVER_NAME.conf
fi
if [[ $ALLOW_DUPLICATE_CN == "yes" ]]; then
  perl -i -p -e "s|;duplicate-cn|duplicate-cn|" /etc/openvpn/$SERVER_NAME.conf
fi

# Step 6 — Adjusting the Server Networking Configuration
perl -i -p -e "s|#net.ipv4.ip_forward=1|net.ipv4.ip_forward=1|" /etc/sysctl.conf
sysctl -p
cp $INITIAL_PWD/before.rules $INSTALLATION_DIR/
INTERFACE=$(ip route | grep default | grep -P 'dev \w+' -o) # -P means Perl-style and -o means match only (Based on https://stackoverflow.com/questions/3320416/how-to-extract-a-value-from-a-string-using-regex-and-a-shell)
INTERFACE_ARRAY=($INTERFACE)
perl -i -p -e "s|eth0|${INTERFACE_ARRAY[1]}|" $INSTALLATION_DIR/before.rules
if ! grep -qF "$(cat $INSTALLATION_DIR/before.rules)" /etc/ufw/before.rules; then  # if the data inside $INSTALLATION_DIR/before.rules is not inside /etc/ufw/before.rules
  perl -i -p -e "s|# Don't delete these required lines, otherwise there will be errors|$(cat $INSTALLATION_DIR/before.rules)\n\n# Don't delete these required lines, otherwise there will be errors|" /etc/ufw/before.rules
fi
rm $INSTALLATION_DIR/before.rules
perl -i -p -e "s|DEFAULT_FORWARD_POLICY=\"DROP\"|DEFAULT_FORWARD_POLICY=\"ACCEPT\"|" /etc/default/ufw
ufw $FIREWALL_MODE $SERVER_PORT/$SERVER_PROTOCOL
ufw $FIREWALL_MODE OpenSSH
ufw disable
echo "yes" | ufw enable

# Step 7 — Starting and Enabling the OpenVPN Service
systemctl start openvpn@$SERVER_NAME
systemctl enable openvpn@$SERVER_NAME

# Step 8 — Creating the Client Configuration Infrastructure
mkdir -p $INSTALLATION_DIR/client-configs/files
cp /usr/share/doc/openvpn/examples/sample-config-files/client.conf $INSTALLATION_DIR/client-configs/base.conf
perl -i -p -e "s|remote my-server-1 1194|remote $SERVER_ADDRESS $SERVER_PORT|" $INSTALLATION_DIR/client-configs/base.conf
perl -i -p -e "s|proto udp|proto $SERVER_PROTOCOL|" $INSTALLATION_DIR/client-configs/base.conf
perl -i -p -e "s|;user nobody|user nobody|" $INSTALLATION_DIR/client-configs/base.conf
perl -i -p -e "s|;group nogroup|group nogroup|" $INSTALLATION_DIR/client-configs/base.conf
perl -i -p -e "s|ca ca.crt|#ca ca.crt|" $INSTALLATION_DIR/client-configs/base.conf
perl -i -p -e "s|cert client.crt|#cert client.crt|" $INSTALLATION_DIR/client-configs/base.conf
perl -i -p -e "s|key client.key|#key client.key|" $INSTALLATION_DIR/client-configs/base.conf
perl -i -p -e "s|cipher AES-256-CBC|cipher AES-256-CBC\nauth SHA256\nkey-direction 1|" $INSTALLATION_DIR/client-configs/base.conf
perl -i -p -e "s|key-direction 1|key-direction 1\n# script-security 2\n# up /etc/openvpn/update-resolv-conf\n# down /etc/openvpn/update-resolv-conf|" $INSTALLATION_DIR/client-configs/base.conf
cp $INITIAL_PWD/make_config.sh $INSTALLATION_DIR/client-configs/make_config.sh
chmod 700 $INSTALLATION_DIR/client-configs/make_config.sh

# Step 9 — Generating Client Configurations
cd $INSTALLATION_DIR/client-configs
for client in ${CLIENTS_ARRAY[*]}; do
  ./make_config.sh $client
  if [[ $BYPASS_DNS == "yes" ]]; then
    perl -i -p -e "s|client\n|client\nsetenv opt block-outside-dns\n|" $INSTALLATION_DIR/client-configs/files/$client.ovpn
  fi
done

# Undoing changes to the terminal status
cd $INITIAL_PWD

# Print informational messages
echo ""
echo ""
echo "The client configuration files are placed on '$INSTALLATION_DIR/client-configs/files/'."
echo "You may want to uncomment the following lines on some of your client configuration files if you are using some Linux client:"
echo "# script-security 2                    --> script-security 2"
echo "# up /etc/openvpn/update-resolv-conf   --> up /etc/openvpn/update-resolv-conf"
echo "# down /etc/openvpn/update-resolv-conf --> down /etc/openvpn/update-resolv-conf"
echo ""
echo ""
systemctl status openvpn@$SERVER_NAME
