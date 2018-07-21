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

if [ "$PROFILE_SHELL" != "bash" ]; then
  echo "Changing to Bash shell."
  sudo su -c "bash \"$SCRIPT_FILENAME\""
  exit
fi

# Verify if this script is running as root

if [ "$(id -u)" != "0" ]; then
  echo "Running this script as root."
  sudo su -c "bash \"$SCRIPT_FILENAME\""
  exit
fi

# Print initialization messages

echo "This script will create an OpenVPN tunnel."
echo "Pay attention to the output for errors or warnings."
echo "Replace an already existing OpenVPN server with the same name will work correctly but old configurations on UFW will remain."
echo "Press enter to continue..."
read -r DUMMY_VAR

# Load functions

is_valid_dns_name_fun () {
  dns_name=$1
  if [[ ! "$dns_name" =~ ^([0-9a-zA-Z-]+(\.[0-9a-zA-Z-]+)*)$ ]]; then
    return 0
  fi
  if [[ ! "$dns_name" =~ ^(.{1,63})$ ]]; then
    return 0
  fi
  OIFS=$IFS  # Internal_field_separator
  IFS="."
  for part in "$dns_name"; do
    if [[ "$part" =~ ^([0-9]+)$ || "$part" =~ ^(-) || "$part" =~ (-)$ ]]; then
      IFS=$OIFS
      return 0
    fi
  done
  IFS=$OIFS
  return 1
}

is_valid_ipv4_address_fun () {
  ipv4_address=$1
  if [[ ! "$ipv4_address" =~ ^([0-9]{1,3}(\.[0-9]{1,3}){3})$ ]]; then
    return 0
  fi
  OIFS=$IFS  # Internal_field_separator
  IFS="."
  for part in "$ipv4_address"; do
    if [[ $part < 0 || $part > 255 ]]; then
      IFS=$OIFS
      return 0
    fi
  done
  IFS=$OIFS
  return 1
}

is_valid_ipv6_address_fun () {
  ipv6_address=$1
  if [[ "$ipv6_address" =~ ^([0-9a-fA-F]{4}(:[0-9a-fA-F]{4}){4})$ ]]; then
    return 1
  fi
  return 0
}

is_valid_port_fun () {
  port=$1
  MIN_PORT=0
  MAX_PORT=65535
  if [[ "$port" =~ ^([0-9]{1,5})$ && $port -ge $MIN_PORT && $port -le $MAX_PORT ]]; then
    return 1
  fi
  echo "Invalid port: $port"
  echo "It should be between $MIN_PORT and $MAX_PORT."
  return 0
}

# Preparing the instalation
INITIAL_PWD=$(pwd)
AUXILIARY_FILES_PATH=$(echo "$INITIAL_PWD/$0" | grep -P ".*/" -o)
AUXILIARY_FILES_PATH=${AUXILIARY_FILES_PATH%/}  # Remove the last "/" from the string
INSTALLATION_DIR="/openvpn_instalation"  # This variable is repeated on 'make_config.sh'
CLIENTS_FILES_DIR="/openvpn_clients_files"
mkdir -p "$INSTALLATION_DIR"

cp "$AUXILIARY_FILES_PATH/configuration_variables.py" "$INSTALLATION_DIR"
echo "Please update the variables inside 'configuration_variables.py'."
echo "Press enter to perform the manual update."
read -r DUMMY_VAR
nano "$INSTALLATION_DIR/configuration_variables.py"
source "$INSTALLATION_DIR/configuration_variables.py"

if [[ ! "$SERVER_NAME" =~ ^([a-zA-Z0-9_-]+)$ ]]; then
  echo "Invalid name: $SERVER_NAME"
  echo "Please, do not use spaces or special characters."
  exit
fi

is_valid_port_fun "$SERVER_PORT"
is_valid_port=$?
if [[ is_valid_port == 0 ]]; then
  exit
fi

SERVER_PROTOCOL=${SERVER_PROTOCOL,,} # Changes all characters to lowercase
if [[ ! "$SERVER_PROTOCOL" =~ ^(udp|tcp)$ ]]; then
  echo "Invalid protocol: $SERVER_PROTOCOL"
  exit
fi

is_valid_ipv4_address_fun "$OPENVPN_SUBNET"
is_valid_ipv4_address=$?
if [[ is_valid_ipv4_address == 0 ]]; then
  echo "Invalid subnet: $OPENVPN_SUBNET"
  exit
fi

is_valid_ipv4_address_fun "$OPENVPN_SUBNET_MASK"
is_valid_ipv4_address=$?
if [[ is_valid_ipv4_address == 0 ]]; then
  echo "Invalid subnet mask: $OPENVPN_SUBNET_MASK"
  exit
fi

if [[ ! "$BYPASS_DNS" =~ ^(yes|no)$ ]]; then
  echo "Invalid 'bypass-dns' option: $BYPASS_DNS"
  exit
fi

is_valid_ipv4_address_fun "$dns_server"
is_valid_ipv4_address=$?
is_valid_ipv6_address_fun "$dns_server"
is_valid_ipv6_address=$?
for dns_server in ${DNS_SERVERS_ARRAY[*]}; do
  if [[ is_valid_ipv4_address == 0  && is_valid_ipv6_address == 0 ]]; then
    echo "Invalid DNS server: $dns_server"
    exit
  fi
done

ALLOW_CLIENT_TO_CLIENT=${ALLOW_CLIENT_TO_CLIENT,,} # Changes all characters to lowercase
if [[ ! "$ALLOW_CLIENT_TO_CLIENT" =~ ^(yes|no)$ ]]; then
  echo "Invalid 'client-to-client' option: $ALLOW_CLIENT_TO_CLIENT"
  exit
fi

ALLOW_DUPLICATE_CN=${ALLOW_DUPLICATE_CN,,} # Changes all characters to lowercase
if [[ ! "$ALLOW_DUPLICATE_CN" =~ ^(yes|no)$ ]]; then
  echo "Invalid 'duplicate-cn' option: $ALLOW_DUPLICATE_CN"
  exit
fi

FIREWALL_MODE=${FIREWALL_MODE,,} # Changes all characters to lowercase
if [[ ! "$FIREWALL_MODE" =~ ^(limit|allow)$ ]]; then
  echo "Invalid mode: $FIREWALL_MODE"
  exit
fi

for client in ${CLIENTS_ARRAY[*]}; do
  if [[ ! "$client" =~ ^([a-zA-Z0-9_-]+)$ ]]; then
    echo "Invalid name: $client"
    echo "Please, do not use spaces or special characters."
    exit
  fi
done

CLIENTS_ARRAY_LENGTH=${#CLIENTS_ARRAY[@]}
CLIENTS_PASSWORDS_ARRAY_LENGTH=${#CLIENTS_PASSWORDS_ARRAY[@]}
if [[ $CLIENTS_ARRAY_LENGTH != $CLIENTS_PASSWORDS_ARRAY_LENGTH ]]; then
  echo "The number of clients should be equal to the number of passwords."
  exit
fi

for server_address in ${SERVER_ADDRESSES_ARRAY[*]}; do
  is_valid_dns_name_fun "$server_address"
  is_valid_dns_name=$?
  is_valid_ipv4_address_fun "$server_address"
  is_valid_ipv4_address=$?
  is_valid_ipv6_address_fun "$server_address"
  is_valid_ipv6_address=$?
  if [[ is_valid_dns_name == 0 && is_valid_ipv4_address == 0 && is_valid_ipv6_address == 0 ]]; then
    echo "Invalid address: $server_address"
    echo "It should be a DNS name, an IPv4 address or an IPv6 address."
    exit
  fi
done

SERVER_ADDRESSES_ARRAY_LENGTH=${#SERVER_ADDRESSES_ARRAY[@]}
SERVER_PORTS_FOR_CLIENT_ARRAY_LENGTH=${#SERVER_PORTS_FOR_CLIENT_ARRAY[@]}
if [[ $SERVER_ADDRESSES_ARRAY_LENGTH != $SERVER_PORTS_FOR_CLIENT_ARRAY_LENGTH ]]; then
  echo "The number of server addresses should be equal to the number of server ports."
  exit
fi
for server_port in ${SERVER_PORTS_FOR_CLIENT_ARRAY[*]}; do
  is_valid_port_fun "$server_port"
  is_valid_port=$?
  if [[ is_valid_port == 0 ]]; then
    exit
  fi
done

ENABLE_REMOTE_RANDOM=${ENABLE_REMOTE_RANDOM,,} # Changes all characters to lowercase
if [[ ! "$ENABLE_REMOTE_RANDOM" =~ ^(yes|no)$ ]]; then
  echo "Invalid 'remote-random' option: $ENABLE_REMOTE_RANDOM"
  exit
fi

apt-get update
apt-get install -y ufw

# Step 1 — Installing OpenVPN and EasyRSA
apt-get install -y openvpn
wget --no-clobber -P "$INSTALLATION_DIR/" https://github.com/OpenVPN/easy-rsa/releases/download/v3.0.4/EasyRSA-3.0.4.tgz
cd "$INSTALLATION_DIR"
tar xf EasyRSA-3.0.4.tgz

# Step 2 — Configuring the EasyRSA Variables and Building the CA
EASYRSA_DIR="$INSTALLATION_DIR/EasyRSA-3.0.4"
cd "$EASYRSA_DIR"
cp vars.example vars
VARS_DIR="$EASYRSA_DIR/vars"
perl -i -p -e "s|#set_var EASYRSA_REQ_COUNTRY|set_var EASYRSA_REQ_COUNTRY|" "$VARS_DIR"
perl -i -p -e "s|#set_var EASYRSA_REQ_PROVINCE|set_var EASYRSA_REQ_PROVINCE|" "$VARS_DIR"
perl -i -p -e "s|#set_var EASYRSA_REQ_CITY|set_var EASYRSA_REQ_CITY|" "$VARS_DIR"
perl -i -p -e "s|#set_var EASYRSA_REQ_ORG|set_var EASYRSA_REQ_ORG|" "$VARS_DIR"
perl -i -p -e "s|#set_var EASYRSA_REQ_EMAIL|set_var EASYRSA_REQ_EMAIL|" "$VARS_DIR"
perl -i -p -e "s|#set_var EASYRSA_REQ_OU|set_var EASYRSA_REQ_OU|" "$VARS_DIR"
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
cd "$EASYRSA_DIR"
echo "" | ./easyrsa gen-req "$SERVER_NAME" nopass
cp "$EASYRSA_DIR/pki/private/$SERVER_NAME.key" /etc/openvpn/
echo "yes" | ./easyrsa sign-req server "$SERVER_NAME"
cp "pki/issued/$SERVER_NAME.crt" /tmp
cp pki/ca.crt /tmp
cp "/tmp/$SERVER_NAME.crt" /etc/openvpn/
cp /tmp/ca.crt "/etc/openvpn/ca_$SERVER_NAME.crt"
./easyrsa gen-dh
openvpn --genkey --secret ta.key
cp "$EASYRSA_DIR/ta.key" "/etc/openvpn/ta_$SERVER_NAME.key"
cp "$EASYRSA_DIR/pki/dh.pem" "/etc/openvpn/dh_$SERVER_NAME.pem"

# Step 4 — Generating a Client Certificate and Key Pair
CLIENT_CONFIGS_DIR="$INSTALLATION_DIR/client-configs"
CLIENT_KEYS_DIR="$CLIENT_CONFIGS_DIR/keys"
mkdir -p "$CLIENT_KEYS_DIR"
chmod -R 700 "$CLIENT_CONFIGS_DIR"
cd "$EASYRSA_DIR"
for ((i=0; i < $CLIENTS_ARRAY_LENGTH; i++)); do
  client=${CLIENTS_ARRAY[$i]}
  password=${CLIENTS_PASSWORDS_ARRAY[$i]}
  if [[ "$password" == "" ]]; then
    printf "\n" | ./easyrsa gen-req "$client" nopass
  else
    printf "$password\n$password\n\n" | ./easyrsa gen-req "$client"
  fi
  cp "pki/private/$client.key" "$CLIENT_KEYS_DIR/"
  echo "yes" | ./easyrsa sign-req client "$client"
  cp "pki/issued/$client.crt" "$CLIENT_KEYS_DIR/"
done
cp "$EASYRSA_DIR/ta.key" "$CLIENT_KEYS_DIR/"
cp "/etc/openvpn/ca_$SERVER_NAME.crt" "$CLIENT_KEYS_DIR/ca.crt"

# Step 5 — Configuring the OpenVPN Service
SERVER_CONF_PATH="/etc/openvpn/$SERVER_NAME.conf"
cp /usr/share/doc/openvpn/examples/sample-config-files/server.conf.gz "$SERVER_CONF_PATH.gz"
gzip -d -f "$SERVER_CONF_PATH.gz"
perl -i -p -e "s|tls-auth ta.key 0 # This file is secret|tls-auth ta_$SERVER_NAME.key 0 # This file is secret\nkey-direction 0|" "$SERVER_CONF_PATH"
perl -i -p -e "s|cipher AES-256-CBC|cipher AES-256-CBC\nauth SHA256|" "$SERVER_CONF_PATH"
perl -i -p -e "s|ca ca.crt|ca ca_$SERVER_NAME.crt|" "$SERVER_CONF_PATH"
perl -i -p -e "s|dh dh2048.pem|dh dh_$SERVER_NAME.pem|" "$SERVER_CONF_PATH"
perl -i -p -e "s|;user nobody|user nobody|" "$SERVER_CONF_PATH"
perl -i -p -e "s|;group nogroup|group nogroup|" "$SERVER_CONF_PATH"

## (Optional) Push DNS Changes to Redirect All Traffic Through the VPN
if [[ "$BYPASS_DNS" == "yes" ]]; then
  perl -i -p -e "s|;push \"redirect-gateway def1 bypass-dhcp\"|push \"redirect-gateway def1 bypass-dhcp bypass-dns\"|" "$SERVER_CONF_PATH"
elif [[ "$BYPASS_DNS" == "no" ]]; then
  perl -i -p -e "s|;push \"redirect-gateway def1 bypass-dhcp\"|push \"redirect-gateway def1 bypass-dhcp\"|" "$SERVER_CONF_PATH"
fi
DHCP_OPTION_DNS_FULL=""
for dns_server in ${DNS_SERVERS_ARRAY[*]}; do
  DHCP_OPTION_DNS_PART="push \"dhcp-option DNS $dns_server\"\n"
  DHCP_OPTION_DNS_FULL="$DHCP_OPTION_DNS_FULL$DHCP_OPTION_DNS_PART"
done
perl -i -p -e "s|;push \"dhcp-option DNS 208.67.222.222\"\n||" "$SERVER_CONF_PATH"
perl -i -p -e "s|;push \"dhcp-option DNS 208.67.220.220\"\n|$DHCP_OPTION_DNS_FULL|" "$SERVER_CONF_PATH"

## (Optional) Adjust the Port and Protocol
perl -i -p -e "s|port 1194|port $SERVER_PORT|" "$SERVER_CONF_PATH"
perl -i -p -e "s|;proto tcp\n||" "$SERVER_CONF_PATH"
perl -i -p -e "s|proto udp|proto $SERVER_PROTOCOL|" "$SERVER_CONF_PATH"
if [[ "$SERVER_PROTOCOL" == "tcp" ]]; then
    perl -i -p -e "s|explicit-exit-notify 1|explicit-exit-notify 0|" "$SERVER_CONF_PATH"
fi

## (Optional) Point to Non-Default Credentials
perl -i -p -e "s|cert server.crt|cert $SERVER_NAME.crt|" "$SERVER_CONF_PATH"
perl -i -p -e "s|key server.key|key $SERVER_NAME.key|" "$SERVER_CONF_PATH"

## Some of the extra adjustments not indicated in the Digital Ocean tutorial
perl -i -p -e "s|server 10.8.0.0 255.255.255.0|server $OPENVPN_SUBNET $OPENVPN_SUBNET_MASK|" "$SERVER_CONF_PATH"
if [[ "$ALLOW_CLIENT_TO_CLIENT" == "yes" ]]; then
  perl -i -p -e "s|;client-to-client|client-to-client|" "$SERVER_CONF_PATH"
fi
if [[ "$ALLOW_DUPLICATE_CN" == "yes" ]]; then
  perl -i -p -e "s|;duplicate-cn|duplicate-cn|" "$SERVER_CONF_PATH"
fi

# Step 6 — Adjusting the Server Networking Configuration
perl -i -p -e "s|#net.ipv4.ip_forward=1|net.ipv4.ip_forward=1|" /etc/sysctl.conf
sysctl -p
cp "$AUXILIARY_FILES_PATH/before.rules" "$INSTALLATION_DIR/"
perl -i -p -e "s|10.8.0.0/8|$OPENVPN_SUBNET/$OPENVPN_SUBNET_MASK_IN_BITS|" "$INSTALLATION_DIR/before.rules"
INTERFACE=$(ip route | grep default | grep -P 'dev \w+' -o) # -P means Perl-style and -o means match only (Based on https://stackoverflow.com/questions/3320416/how-to-extract-a-value-from-a-string-using-regex-and-a-shell)
INTERFACE=${INTERFACE:4} # remove 'dev '
perl -i -p -e "s|eth0|$INTERFACE|" "$INSTALLATION_DIR/before.rules"
if [[ ! $(cat /etc/ufw/before.rules) =~ "$(cat "$INSTALLATION_DIR/before.rules")" ]]; then  # if the data inside "$INSTALLATION_DIR/before.rules" is not inside /etc/ufw/before.rules
  perl -i -p -e "s|# Don't delete these required lines, otherwise there will be errors|$(cat "$INSTALLATION_DIR/before.rules")\n\n# Don't delete these required lines, otherwise there will be errors|" /etc/ufw/before.rules
fi
perl -i -p -e "s|DEFAULT_FORWARD_POLICY=\"DROP\"|DEFAULT_FORWARD_POLICY=\"ACCEPT\"|" /etc/default/ufw
ufw "$FIREWALL_MODE" "$SERVER_PORT"/"$SERVER_PROTOCOL"
ufw "$FIREWALL_MODE" OpenSSH
ufw disable
echo "y" | ufw enable

# Step 7 — Starting and Enabling the OpenVPN Service
systemctl start "openvpn@$SERVER_NAME"
systemctl enable "openvpn@$SERVER_NAME"

# Step 8 — Creating the Client Configuration Infrastructure
mkdir -p "$CLIENT_CONFIGS_DIR/files"
BASE_CONF_PATH="$CLIENT_CONFIGS_DIR/base.conf"
cp /usr/share/doc/openvpn/examples/sample-config-files/client.conf "$BASE_CONF_PATH"
REMOTES_FULL=""
for ((i=0; i < $SERVER_ADDRESSES_ARRAY_LENGTH; i++)); do
  REMOTES_PART="remote ${SERVER_ADDRESSES_ARRAY[$i]} ${SERVER_PORTS_FOR_CLIENT_ARRAY[$i]}\n"
  REMOTES_FULL="$REMOTES_FULL$REMOTES_PART"
done
perl -i -p -e "s|remote my-server-1 1194\n||" "$BASE_CONF_PATH"
perl -i -p -e "s|;remote my-server-2 1194\n|$REMOTES_FULL|" "$BASE_CONF_PATH"
if [[ "$ENABLE_REMOTE_RANDOM" == "yes" ]]; then
  perl -i -p -e "s|;remote-random|remote-random|" "$BASE_CONF_PATH"
fi
perl -i -p -e "s|proto udp|proto $SERVER_PROTOCOL|" "$BASE_CONF_PATH"
perl -i -p -e "s|;user nobody|user nobody|" "$BASE_CONF_PATH"
perl -i -p -e "s|;group nogroup|group nogroup|" "$BASE_CONF_PATH"
perl -i -p -e "s|ca ca.crt|#ca ca.crt|" "$BASE_CONF_PATH"
perl -i -p -e "s|cert client.crt|#cert client.crt|" "$BASE_CONF_PATH"
perl -i -p -e "s|key client.key|#key client.key|" "$BASE_CONF_PATH"
perl -i -p -e "s|cipher AES-256-CBC|cipher AES-256-CBC\nauth SHA256\nkey-direction 1|" "$BASE_CONF_PATH"
perl -i -p -e "s|key-direction 1|key-direction 1\n# script-security 2\n# up /etc/openvpn/update-resolv-conf\n# down /etc/openvpn/update-resolv-conf|" "$BASE_CONF_PATH"
cp "$AUXILIARY_FILES_PATH/make_config.sh" "$CLIENT_CONFIGS_DIR/make_config.sh"
chmod 700 "$CLIENT_CONFIGS_DIR/make_config.sh"

# Step 9 — Generating Client Configurations
SERVER_CLIENTS_FILES_DIR="$CLIENTS_FILES_DIR/$SERVER_NAME"
mkdir -p "$SERVER_CLIENTS_FILES_DIR"
cd "$CLIENT_CONFIGS_DIR"
for client in ${CLIENTS_ARRAY[*]}; do
  ./make_config.sh "$client"
  if [[ "$BYPASS_DNS" == "yes" ]]; then
    perl -i -p -e "s|client\n|client\nsetenv opt block-outside-dns\n|" "$CLIENT_CONFIGS_DIR/files/$client.ovpn"
  fi
done
mv "$CLIENT_CONFIGS_DIR/files/"* "$SERVER_CLIENTS_FILES_DIR/"

# Restart OpenVPN service (useful when replacing an already existing OpenVPN server)
systemctl restart "openvpn@$SERVER_NAME"

# Undoing changes no longer needed
cd "$INITIAL_PWD"
rm -r "$INSTALLATION_DIR"

# Print informational messages
echo ""
echo ""
echo "The client configuration files are placed on '$SERVER_CLIENTS_FILES_DIR/'."
echo "You may want to uncomment the following lines on some of your client configuration files if you are using some Linux client:"
echo "# script-security 2                    --> script-security 2"
echo "# up /etc/openvpn/update-resolv-conf   --> up /etc/openvpn/update-resolv-conf"
echo "# down /etc/openvpn/update-resolv-conf --> down /etc/openvpn/update-resolv-conf"
echo ""
echo ""
systemctl status "openvpn@$SERVER_NAME"
