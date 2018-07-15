#!/bin/bash

# First argument: Client identifier

INSTALLATION_DIR="/openvpn_instalation"  # This variable is repeated on 'install_openvpn_server.sh'
KEY_DIR="$INSTALLATION_DIR/client-configs/keys"
OUTPUT_DIR="$INSTALLATION_DIR/client-configs/files"
BASE_CONFIG="$INSTALLATION_DIR/client-configs/base.conf"

cat ${BASE_CONFIG} \
    <(echo -e '<ca>') \
    ${KEY_DIR}/ca.crt \
    <(echo -e '</ca>\n<cert>') \
    ${KEY_DIR}/${1}.crt \
    <(echo -e '</cert>\n<key>') \
    ${KEY_DIR}/${1}.key \
    <(echo -e '</key>\n<tls-auth>') \
    ${KEY_DIR}/ta.key \
    <(echo -e '</tls-auth>') \
    > ${OUTPUT_DIR}/${1}.ovpn
