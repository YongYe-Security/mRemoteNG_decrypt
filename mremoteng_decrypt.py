#!/usr/bin/env python3
import argparse
import csv
import re
import base64
import sys
import hashlib
import datetime
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad


# DECRYPTION ###################################################################
def decrypt(mode, data, password):
    if (mode == 'CBC'):
        return cbc_decrypt(data, password)
    if (mode == 'GCM'):
        return gcm_decrypt(data, password)
    raise ValueError(f'unkown mode {mode}') ;

def gcm_decrypt(data, password):
    salt = data[:16]
    nonce = data[16:32]
    ciphertext = data[32:-16]
    tag = data[-16:]
    # TODO: get these values from the config file
    key = hashlib.pbkdf2_hmac('sha1', password, salt, 1000, dklen=32)   # default values
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    cipher.update(salt)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag).decode()
    except ValueError:
        print('MAC tag not valid, this means the master password is wrong or the crypto values aren\'t default')
        exit(1)
    return plaintext

def cbc_decrypt(data, password):
    iv = data[:16]
    ciphertext = data[16:]
    key = hashlib.md5(password).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()



def print_output(name, hostname, username, password, node_num, file):
    tabs = "" if node_num == 5 else "\t" * (node_num // 4)
    if node_num == 5:
        file.write('=' * 80 + '\n')
        print('=' * 80)
    output_str = f'{tabs}Name: {name}\n{tabs}Host: {hostname}\n{tabs}User: {username}\n{tabs}Pass: {password}\n'
    file.write(output_str + '\n')
    print(output_str)

# MAIN #########################################################################
parser = argparse.ArgumentParser(description = 'Decrypt mRemoteNG configuration files')
parser.add_argument('config_file', type=str, help='mRemoteNG XML configuration file')
parser.add_argument('-p', '--password', type=str, default='mR3m', help='Optional decryption password')
args = parser.parse_args()

with open(args.config_file, 'r', encoding='utf-8') as f:
    conf = f.read()

mode = re.findall('BlockCipherMode="([^"]*)"', conf)
if not mode:
    mode = 'CBC'            # <1.75 key is md5(password) and encryption is CBC
elif mode[0] == 'GCM':
    mode = 'GCM'            # >=1.75 key is PBKDF2(password) and encryption is GCM
else:
    print('Unknown mode {}, implement it yourself or open a ticket'.format(mode[0]))
    sys.exit(1)

# Extract and decrypt file data if FullFileEncryption is true
full_encryption = re.findall('FullFileEncryption="([^"]*)"', conf)

if full_encryption and (full_encryption[0] == 'true'):
    cypher=base64.b64decode(re.findall('<.*>(.+)</mrng:Connections>', conf)[0]) 
    conf=decrypt(mode, cypher, args.password.encode())

nodes = re.findall('<Node .+?>', conf)
tabnums = re.finditer(r'([\s\t]*)<Node Name=', conf)
nodetab_list = []
current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
output_filename = f'output_{current_time}.txt'
    
    
for tabnum in tabnums:
    leading_characters = tabnum.group(1)
    nodetab_numbers = len(leading_characters)
    nodetab_list.append(nodetab_numbers)


for i, node in enumerate(nodes):
    name = re.findall(' Name="([^"]*)"', node)[0]
    username = re.findall(' Username="([^"]*)"', node)[0]
    Portnumber = re.findall(' Port="([^"]*)"', node)[0]
    hostname = re.findall(' Hostname="([^"]*)"', node)[0]
    Protocolname = re.findall(' Protocol="([^"]*)"', node)[0]
    if hostname != '':
        hostname = f'{hostname}:{Portnumber}\t({Protocolname})'
    domainname = re.findall(' Domain="([^"]*)"', node)[0]
    if domainname != '':
        username = f'{domainname}\{username}'
    data = base64.b64decode(re.findall(' Password="([^ ]*)"', node)[0])
    password=""
    if data != b'':
        password=decrypt(mode, data, args.password.encode())
    

    with open(output_filename, 'a', encoding='utf-8') as file:
        print_output(name, hostname, username, password, nodetab_list[i], file)

