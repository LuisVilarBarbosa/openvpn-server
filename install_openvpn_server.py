#!/usr/bin/python
# coding=utf-8

import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import ui

def main():
    try:
        ui.verify_python_version()
        my_file_path = os.path.abspath(sys.argv[0])

        # Verify if this script is running as root

        if os.geteuid() != 0:
            print("Running this script as root.")
            ui.execute_command(["sudo", "python3", my_file_path])
            quit()

        # Print initialization messages

        print("This script will create an OpenVPN tunnel.")
        print("Replace an already existing OpenVPN server with the same name will work correctly but old configurations on UFW will remain.")
        input("Press enter to continue...")

        # Preparing the installation
        initial_cwd = os.getcwd()
        auxiliary_files_path = my_file_path[:my_file_path.rfind("/")]
        installation_dir = tempfile.mkdtemp()
        clients_files_dir = initial_cwd + "/openvpn_clients_files"
        ui.makedirs(installation_dir)

        input("Please update the variables inside 'configuration_variables.py', save the file and press enter.")
        import configuration_variables
        import configuration_variables_validator
        configuration_variables_validator.validate_configuration_variables()

        ui.execute_command(["apt-get", "update"])
        ui.execute_command(["apt-get", "install", "-y", "ufw"])

        # Step 1 — Installing OpenVPN and EasyRSA
        ui.execute_command(["apt-get", "install", "-y", "openvpn"])
        ui.execute_command(["wget", "--no-clobber", "-P", installation_dir + "/", "https://github.com/OpenVPN/easy-rsa/releases/download/v3.0.4/EasyRSA-3.0.4.tgz"])
        os.chdir(installation_dir)
        tar = tarfile.open("EasyRSA-3.0.4.tgz")
        tar.extractall()
        tar.close()

        # Step 2 — Configuring the EasyRSA Variables and Building the CA
        easyrsa_dir = installation_dir + "/EasyRSA-3.0.4"
        os.chdir(easyrsa_dir)
        shutil.copy2("vars.example", "vars")
        vars_path = easyrsa_dir + "/vars"
        ui.replace_text_in_file("#set_var EASYRSA_REQ_COUNTRY", "set_var EASYRSA_REQ_COUNTRY", vars_path)
        ui.replace_text_in_file("#set_var EASYRSA_REQ_PROVINCE", "set_var EASYRSA_REQ_PROVINCE", vars_path)
        ui.replace_text_in_file("#set_var EASYRSA_REQ_CITY", "set_var EASYRSA_REQ_CITY", vars_path)
        ui.replace_text_in_file("#set_var EASYRSA_REQ_ORG", "set_var EASYRSA_REQ_ORG", vars_path)
        ui.replace_text_in_file("#set_var EASYRSA_REQ_EMAIL", "set_var EASYRSA_REQ_EMAIL", vars_path)
        ui.replace_text_in_file("#set_var EASYRSA_REQ_OU", "set_var EASYRSA_REQ_OU", vars_path)
        print("Please update the following variables inside 'vars':")
        print(" - EASYRSA_REQ_COUNTRY")
        print(" - EASYRSA_REQ_PROVINCE")
        print(" - EASYRSA_REQ_CITY")
        print(" - EASYRSA_REQ_ORG")
        print(" - EASYRSA_REQ_EMAIL")
        print(" - EASYRSA_REQ_OU")
        input("Press enter to perform the manual update.")
        ui.execute_command(["nano", vars_path])
        ui.execute_command(["./easyrsa", "init-pki"], "yes\n")
        ui.execute_command(["./easyrsa", "build-ca", "nopass"], "\n")

        # Step 3 — Creating the Server Certificate, Key, and Encryption Files
        os.chdir(easyrsa_dir)
        ui.execute_command(["./easyrsa", "gen-req",  configuration_variables.SERVER_NAME, "nopass"], "\n")
        shutil.copy2(easyrsa_dir + "/pki/private/" + configuration_variables.SERVER_NAME + ".key", "/etc/openvpn/")
        ui.execute_command(["./easyrsa", "sign-req", "server", configuration_variables.SERVER_NAME], "yes\n")
        shutil.copy2("pki/issued/" + configuration_variables.SERVER_NAME + ".crt", "/tmp")
        shutil.copy2("pki/ca.crt", "/tmp")
        shutil.copy2("/tmp/" + configuration_variables.SERVER_NAME + ".crt", "/etc/openvpn/")
        shutil.copy2("/tmp/ca.crt", "/etc/openvpn/ca_" + configuration_variables.SERVER_NAME + ".crt")
        ui.execute_command(["./easyrsa", "gen-dh"])
        ui.execute_command(["openvpn", "--genkey", "--secret", "ta.key"])
        shutil.copy2(easyrsa_dir + "/ta.key", "/etc/openvpn/ta_" + configuration_variables.SERVER_NAME + ".key")
        shutil.copy2(easyrsa_dir + "/pki/dh.pem", "/etc/openvpn/dh_" + configuration_variables.SERVER_NAME + ".pem")

        # Step 4 — Generating a Client Certificate and Key Pair
        client_configs_dir = installation_dir + "/client-configs"
        client_keys_dir = client_configs_dir + "/keys"
        ui.makedirs(client_keys_dir)
        ui.chmod_recursive(client_configs_dir, 0o700)
        os.chdir(easyrsa_dir)
        for i in range(len(configuration_variables.CLIENTS_ARRAY)):
            client = configuration_variables.CLIENTS_ARRAY[i]
            enable_password = configuration_variables.ENABLE_CLIENTS_PASSWORDS_ARRAY[i]
            if enable_password == "no":
                  ui.execute_command(["./easyrsa", "gen-req", client, "nopass"], "\n")
            elif enable_password == "yes":
                  ui.execute_command(["./easyrsa", "gen-req", client], "\n")
            shutil.copy2("pki/private/" + client + ".key", client_keys_dir + "/")
            ui.execute_command(["./easyrsa", "sign-req", "client", client], "yes\n")
            shutil.copy2("pki/issued/" + client + ".crt", client_keys_dir + "/")
        shutil.copy2(easyrsa_dir + "/ta.key", client_keys_dir + "/")
        shutil.copy2("/etc/openvpn/ca_" + configuration_variables.SERVER_NAME + ".crt", client_keys_dir + "/ca.crt")

        # Step 5 — Configuring the OpenVPN Service
        server_conf_path = "/etc/openvpn/" + configuration_variables.SERVER_NAME + ".conf"
        shutil.copy2("/usr/share/doc/openvpn/examples/sample-config-files/server.conf.gz", server_conf_path + ".gz")
        ui.decompress_gzip_file(server_conf_path + ".gz")
        if ui.replace_text_in_file(";tls-auth ta.key 0 # This file is secret", "tls-auth ta_" + configuration_variables.SERVER_NAME + ".key 0 # This file is secret\nkey-direction 0", server_conf_path) == 0:
            ui.replace_text_in_file("tls-auth ta.key 0 # This file is secret", "tls-auth ta_" + configuration_variables.SERVER_NAME + ".key 0 # This file is secret\nkey-direction 0", server_conf_path)
        if ui.replace_text_in_file(";cipher AES-128-CBC   # AES", "cipher AES-256-CBC   # AES\nauth SHA256", server_conf_path) == 0:
            ui.replace_text_in_file("cipher AES-256-CBC", "cipher AES-256-CBC\nauth SHA256", server_conf_path)
        ui.replace_text_in_file("ca ca.crt", "ca ca_" + configuration_variables.SERVER_NAME + ".crt", server_conf_path)
        ui.replace_text_in_file("dh dh2048.pem", "dh dh_" + configuration_variables.SERVER_NAME + ".pem", server_conf_path)
        ui.replace_text_in_file(";user nobody", "user nobody", server_conf_path)
        ui.replace_text_in_file(";group nogroup", "group nogroup", server_conf_path)

        ## (Optional) Push DNS Changes to Redirect All Traffic Through the VPN
        if configuration_variables.BYPASS_DNS == "yes":
            ui.replace_text_in_file(";push \"redirect-gateway def1 bypass-dhcp\"", "push \"redirect-gateway def1 bypass-dhcp bypass-dns\"", server_conf_path)
        elif configuration_variables.BYPASS_DNS == "no":
            ui.replace_text_in_file(";push \"redirect-gateway def1 bypass-dhcp\"", "push \"redirect-gateway def1 bypass-dhcp\"", server_conf_path)
        dhcp_option_dns_full = ""
        for dns_server in configuration_variables.DNS_SERVERS_ARRAY:
            dhcp_option_dns_part = "push \"dhcp-option DNS " + dns_server + "\"\n"
            dhcp_option_dns_full = dhcp_option_dns_full + dhcp_option_dns_part
        ui.replace_text_in_file(";push \"dhcp-option DNS 208.67.222.222\"\n", "", server_conf_path)
        ui.replace_text_in_file(";push \"dhcp-option DNS 208.67.220.220\"\n", dhcp_option_dns_full, server_conf_path)

        ## (Optional) Adjust the Port and Protocol
        ui.replace_text_in_file("port 1194", "port " + configuration_variables.SERVER_PORT, server_conf_path)
        ui.replace_text_in_file(";proto tcp\n", "", server_conf_path)
        ui.replace_text_in_file("proto udp", "proto " + configuration_variables.SERVER_PROTOCOL, server_conf_path)
        if configuration_variables.SERVER_PROTOCOL == "tcp":
            ui.replace_text_in_file("explicit-exit-notify 1", "explicit-exit-notify 0", server_conf_path)

        ## (Optional) Point to Non-Default Credentials
        ui.replace_text_in_file("cert server.crt", "cert " + configuration_variables.SERVER_NAME + ".crt", server_conf_path)
        ui.replace_text_in_file("key server.key", "key " + configuration_variables.SERVER_NAME + ".key", server_conf_path)

        ## Some of the extra adjustments not indicated in the Digital Ocean tutorial
        ui.replace_text_in_file("server 10.8.0.0 255.255.255.0", "server " + configuration_variables.OPENVPN_SUBNET + " " + configuration_variables.OPENVPN_SUBNET_MASK, server_conf_path)
        if configuration_variables.ALLOW_CLIENT_TO_CLIENT == "yes":
            ui.replace_text_in_file(";client-to-client", "client-to-client", server_conf_path)
        if configuration_variables.ALLOW_DUPLICATE_CN == "yes":
            ui.replace_text_in_file(";duplicate-cn", "duplicate-cn", server_conf_path)

        # Step 6 — Adjusting the Server Networking Configuration
        ui.replace_text_in_file("#net.ipv4.ip_forward=1", "net.ipv4.ip_forward=1", "/etc/sysctl.conf")
        ui.execute_command(["sysctl", "-p"])
        shutil.copy2(auxiliary_files_path + "/before.rules", installation_dir + "/")
        ui.replace_text_in_file("10.8.0.0/8", configuration_variables.OPENVPN_SUBNET + "/" + configuration_variables.OPENVPN_SUBNET_MASK_IN_BITS, installation_dir + "/before.rules")
        interface = ui.get_default_network_device()
        ui.replace_text_in_file("eth0", interface, installation_dir + "/before.rules")
        before_rules_to_add = ui.read_file(installation_dir + "/before.rules")
        if not before_rules_to_add in ui.read_file("/etc/ufw/before.rules"):
            ui.replace_text_in_file("# Don't delete these required lines, otherwise there will be errors", before_rules_to_add + "\n\n# Don't delete these required lines, otherwise there will be errors", "/etc/ufw/before.rules")
        ui.replace_text_in_file("DEFAULT_FORWARD_POLICY=\"DROP\"", "DEFAULT_FORWARD_POLICY=\"ACCEPT\"", "/etc/default/ufw")
        ui.execute_command(["ufw", configuration_variables.FIREWALL_MODE, configuration_variables.SERVER_PORT + "/" + configuration_variables.SERVER_PROTOCOL])
        ui.execute_command(["ufw", configuration_variables.FIREWALL_MODE, "OpenSSH"])
        ui.execute_command(["ufw", "disable"])
        ui.execute_command(["ufw", "enable"], "y\n")

        # Step 7 — Starting and Enabling the OpenVPN Service
        ui.execute_command(["systemctl", "start", "openvpn@" + configuration_variables.SERVER_NAME])
        ui.execute_command(["systemctl", "enable", "openvpn@" + configuration_variables.SERVER_NAME])

        # Step 8 — Creating the Client Configuration Infrastructure
        ui.makedirs(client_configs_dir + "/files")
        base_conf_path = client_configs_dir + "/base.conf"
        shutil.copy2("/usr/share/doc/openvpn/examples/sample-config-files/client.conf", base_conf_path)
        remotes_full = ""
        for i in range(len(configuration_variables.SERVER_ADDRESSES_ARRAY)):
            remotes_part = "remote " + configuration_variables.SERVER_ADDRESSES_ARRAY[i] + " " + configuration_variables.SERVER_PORTS_FOR_CLIENT_ARRAY[i] + "\n"
            remotes_full = remotes_full + remotes_part
        ui.replace_text_in_file("remote my-server-1 1194\n", "", base_conf_path)
        ui.replace_text_in_file(";remote my-server-2 1194\n", remotes_full, base_conf_path)
        if configuration_variables.ENABLE_REMOTE_RANDOM == "yes":
            ui.replace_text_in_file(";remote-random", "remote-random", base_conf_path)
        ui.replace_text_in_file("proto udp", "proto " + configuration_variables.SERVER_PROTOCOL, base_conf_path)
        ui.replace_text_in_file(";user nobody", "user nobody", base_conf_path)
        ui.replace_text_in_file(";group nogroup", "group nogroup", base_conf_path)
        ui.replace_text_in_file("ca ca.crt", "#ca ca.crt", base_conf_path)
        ui.replace_text_in_file("cert client.crt", "#cert client.crt", base_conf_path)
        ui.replace_text_in_file("key client.key", "#key client.key", base_conf_path)
        if ui.replace_text_in_file(";cipher x", "cipher AES-256-CBC\nauth SHA256\nkey-direction 1", base_conf_path) == 0:
            ui.replace_text_in_file("cipher AES-256-CBC", "cipher AES-256-CBC\nauth SHA256\nkey-direction 1", base_conf_path)
        ui.replace_text_in_file("key-direction 1", "key-direction 1\n# script-security 2\n# up /etc/openvpn/update-resolv-conf\n# down /etc/openvpn/update-resolv-conf", base_conf_path)
        shutil.copy2(auxiliary_files_path + "/make_config.sh", client_configs_dir + "/make_config.sh")
        os.chmod(client_configs_dir + "/make_config.sh", 0o700)

        # Step 9 — Generating Client Configurations
        server_clients_files_dir = clients_files_dir + "/" + configuration_variables.SERVER_NAME
        ui.makedirs(server_clients_files_dir)
        os.chdir(client_configs_dir)
        for client in configuration_variables.CLIENTS_ARRAY:
            ui.execute_command(["./make_config.sh", client, installation_dir])
            if configuration_variables.BYPASS_DNS == "yes":
                ui.replace_text_in_file("client\n", "client\nsetenv opt block-outside-dns\n", client_configs_dir + "/files/" + client + ".ovpn")
        ui.move_content(client_configs_dir + "/files/", server_clients_files_dir)

        # Restart OpenVPN service (useful when replacing an already existing OpenVPN server)
        ui.execute_command(["systemctl", "restart", "openvpn@" + configuration_variables.SERVER_NAME])

        # Print informational messages
        print("")
        print("")
        print("The client configuration files are placed on '" + server_clients_files_dir + "/'.")
        print("You may want to uncomment the following lines on some of your client configuration files if you are using some Linux client:")
        print("# script-security 2                    --> script-security 2")
        print("# up /etc/openvpn/update-resolv-conf   --> up /etc/openvpn/update-resolv-conf")
        print("# down /etc/openvpn/update-resolv-conf --> down /etc/openvpn/update-resolv-conf")
        print("")
        print("")
        ui.execute_command(["systemctl", "status", "openvpn@" + configuration_variables.SERVER_NAME])
    finally:
        # Undoing changes no longer needed
        os.chdir(initial_cwd)
        shutil.rmtree(installation_dir)

if __name__ == '__main__':
    main()
