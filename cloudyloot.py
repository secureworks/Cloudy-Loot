#!/usr/bin/python3

# Copyright 2022 Secureworks
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
import requests
import os
import fnmatch
import argparse
import logging

key_file = ["*.pem", "*.key", "*.priv"]
ssh_file = ["*id_dsa*", "*id_ecdsa*", "*id_ed25519*", "*id_rsa*"]
cloud_tools = ["gcloud", "gsutil", "aws", "az", "kubectl"]
credential_files = ["gcloud", "access_tokens.db", "credentials. db", "credentials", "accessTokens.json", "azureProfile.json", "legacy_credentials", "token"]

gcp_metdata_endpoints = ["http://metadata.google.internal/computeMetadata/v1/?recursive=true&alt=text"]
aws_metadata_endpoints = ["http://169.254.169.254/latest/meta-data/", "http://169.254.169.254/latest/identity-credentials/ec2/info", "http://169.254.169.254/latest/user-data"]
azure_metada_endpoints = ["http://169.254.169.254/metadata/instance?api-version=2021-02-01"]

def find_exact(name, path):
    result = []
    for i in name:
        for root, dirs, files in os.walk(path):
            if i in files:
                result.append(os.path.join(root, i))
    return result

def find_pattern(pattern, path):
    result = []
    for i in pattern:
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, i):
                    result.append(os.path.join(root, name))
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=f"Cloudy Loot - Host enumeration tool, specifically looking for cloud loot", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-A', '--all',   action='store_true', help='Run all Enumeration')
    parser.add_argument('-e', '--env', action='store_true', help='Print ENV')
    parser.add_argument('-i', '--iptables', action='store_true', help='List IPTables rules')
    parser.add_argument('-k', '--keyfiles', action='store_true', help='Identify Key files')
    parser.add_argument('-t', '--tools', action='store_true', help='Identify Cloud Tools')
    parser.add_argument('-C', '--credfiles', action='store_true', help='Identify Credential Files')
    parser.add_argument('-c', '--containers', action='store_true', help='Enum Containers and orchestration')
    parser.add_argument('-m', '--metadata', action='store_true', help='Query Metadata Endpoints')
    parser.add_argument('-o', '--outfile', type=str, help='File Name to Log to')
    args = parser.parse_args()

    logging_format = '[%(levelname)s] %(message)s'
    logging_level  = logging.INFO
    if args.outfile is not None:
        logging.basicConfig(format=logging_format, level=logging_level, filename=args.outfile, filemode='w')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        logging.getLogger().addHandler(console)
    else:
        logging.basicConfig(format=logging_format, level=logging_level)

    print("[+] ----- OS ----- ")
    logging.info(f'OS_Info: {os.uname()}')

    if args.all or args.env:
        print("[+] ----- ENV ----- ")
        logging.info(f'ENV_Info: {os.environ}')
    
    if args.all or args.iptables:
        print("[+] ----- IPTABLES ----- ")
        logging.info(f'Iptables_info: {subprocess.Popen("iptables -L", shell=True).wait()}')

    if args.all or args.keyfiles:
        print("[+] ----- Key Files ----- ")
        for r in find_pattern(ssh_file, '/'):
            logging.info(f'Sshfile: {r}')
        for r in find_pattern(key_file, '/home/'):
            logging.info(f'Keyfile: {r}')
        for r in find_pattern(key_file, '/var/lib/docker/'):
            logging.info(f'Keyfile: {r}')
    
    if args.all or args.tools:
        print("[+] ----- Cloud Tools ----- ")
        for r in find_exact(cloud_tools, '/'):
            logging.info(f'Cloudtool: {r}')

    if args.all or args.credfiles:
        print("[+] ----- Credential Files ----- ")
        for r in find_exact(credential_files, '/'):
            logging.info(f'Cred_file: {r}')

    if args.all or args.metadata:
        print ("[+] ----- Metadata Endpoints ----- ")
        for i in gcp_metdata_endpoints:
            url = i
            headers = {'Metadata-Flavor': 'Google'}
            try:
                response = requests.get(url,headers=headers, timeout=2)
                if response.status_code == 200:
                    logging.info(response.content.decode())
                else:
                    logging.info(f'{str(response.status_code)} for {str(i)}')
            except:
                logging.info("No google metadata found")
        for i in aws_metadata_endpoints:
            url = i
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    logging.info(response.content)
                else:
                    logging.info(f'{str(response.status_code)} for {str(i)}')
            except:
                logging.info("No AWS metadata found")
        for i in azure_metada_endpoints:
            url = i
            headers = {'Metadata': 'True'}
            try:
                response = requests.get(url,headers=headers, timeout=2)
                if response.status_code == 200:
                    logging.info(response.content)
                else:
                    logging.info(f'{str(response.status_code)} for {str(i)}')
            except:
                logging.info("No Azure metadata found")
    
    if args.all or args.containers:
        print ("[+] ----- Checking for Container Software ----- ")
        print ("[+] ----- Running Docker Containers ----- ")
        try:
            logging.info(subprocess.Popen('docker ps', shell=True).wait())
        except:
            logging.info("Docker does not appear to be on the system")
        print ("[+] ----- Running Podman Containers ----- ")
        try: 
            logging.info(subprocess.Popen('podman pod list', shell=True).wait())
        except:
            logging.info("Podman does not appear to be on the system")
        print ("[+] ----- Running OpenVZ Containers ----- ")
        try: 
            logging.info(subprocess.Popen('vzlist', shell=True).wait())
        except:
            logging.info("OpenVZ does not appear to be on the system")
        print ("[+] ----- Running Containerd Containers ----- ")
        try:
            logging.info(subprocess.Popen('ctr image ls', shell=True).wait())
        except:
            logging.info("Containerd does not appear to be on the system")
        print ("[+] ----- Checking for Kubernetes config ----- ")
        try:
            logging.info(subprocess.Popen('kubectl config view', shell=True).wait())
        except:
            logging.info("Kubernetes does not appear to be on the system")
