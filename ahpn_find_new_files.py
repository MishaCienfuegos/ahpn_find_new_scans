import argparse
from get_files_hash_values import get_files_hash_values
import csv
import hashlib
import os
import re

existing_manifest = 'test_files/2_2018.csv'
new_calculated_hashes = 'test_files/ahpn-misha_test-2-1-hash_values.csv'
new_root_dir = '../../../../../ahpn/misha_test/ahpn_2019/2/1'
# new_root_dir = '../../Downloads'

new_manifest_list = [{'file': '17427196.tif', 'path': '/mnt/ahpn/misha_test/ahpn_2019/2/1/17427196.tif', 'hash': 'ea756afc8bb793d9dda6b6ef8086c62f2065a295c59bc95680eed5d53d6b4c68', 'file_size': 50545}, {'file': '17427197.tif', 'path': '/mnt/ahpn/misha_test/ahpn_2019/2/1/17427197.tif', 'hash': 'b3f35eda4bbbf5ed40adbba4104e584969c16332df846a2f289dcad6f5380898', 'file_size': 131168}, {'file': '17427198.tif', 'path': '/mnt/ahpn/misha_test/ahpn_2019/2/1/17427198.tif', 'hash': '3e4f7e27c5742dbbc55bf019a827409f9bbb2cec556ddfc923e4d293d480e88c', 'file_size': 154177}, {'file': '17427199.tif', 'path': '/mnt/ahpn/misha_test/ahpn_2019/2/1/17427199.tif', 'hash': '24b30fc3fcdadf9e0bb36e6be3e2084ab35e7ec140110395d4c88b575bed3329', 'file_size': 68948}, {'file': '17427200.tif', 'path': '/mnt/ahpn/misha_test/ahpn_2019/2/1/17427200.tif', 'hash': '4bdf0fe0cc6a870d793768a6c5d624c927cb07e97bb9cf231f42085a67914e93', 'file_size': 156391}, {'file': '17427201.tif', 'path': '/mnt/ahpn/misha_test/ahpn_2019/2/1/17427201.tif', 'hash': '56e716a99e86444d88545a2ca3ee7fbff4d515727d5aba0f75a66fb89b592286', 'file_size': 99158}, {'file': '17427863.tif', 'path': '/mnt/ahpn/misha_test/ahpn_2019/2/1/17427863.tif', 'hash': 'ba918760d29b63a8cdb37fde90c9b6dae91393ea525a3ef06beb8522b73d10fc', 'file_size': 17172}, {'file': '17470374.tif', 'path': '/mnt/ahpn/misha_test/ahpn_2019/2/1/17470374.tif', 'hash': 'd791fb8a28f886dae9781b689b1c66ba064b7a81db225d896c0cd4a718a3ee15', 'file_size': 115478}, {'file': '17470375.tif', 'path': '/mnt/ahpn/misha_test/ahpn_2019/2/1/17470375.tif', 'hash': '79aa184189b9ac2b5401a32f9522e6bc6cf766d04e649467e0e8892f79087b31', 'file_size': 124963}, {'file': '17470376.tif', 'path': '/mnt/ahpn/misha_test/ahpn_2019/2/1/17470376.tif', 'hash': '991643e3c890962c2dd7b7ab52fb7e2ba24ae4158e431c13035998ad437400dd', 'file_size': 1246816}, {'file': '11193087.tif', 'path': '/mnt/ahpn/misha_test/ahpn_2019/2/1/11193087.tif', 'hash': 'ea411a0f9529b173d0ecd719782f7a93d323d8bc061c6cb84326c22ca5d7273a', 'file_size': 34120}, {'file': '11194577.tif', 'path': '/mnt/ahpn/misha_test/ahpn_2019/2/1/11194577.tif', 'hash': '5a26bcda9b9029b2e9080feeab708ddbf90b752fe61ec1079b92769cca2bef98', 'file_size': 32518}]

def unixify_existing_manifest(existing_manifest_path):
  with open(existing_manifest_path, 'r') as file:
    csv_reader = csv.reader(file, delimiter=',', quotechar='"')
    manifest_list = []

    for row in csv_reader:
      row_dict = {}

      unixified_file_name = re.sub(r'\\', r'/', row[1])
      row_dict['hash'] = row[0]
      row_dict['path'] = unixified_file_name

      manifest_list.append(row_dict)

    return manifest_list

# run calculate hash values on second input location (2019)
# returns list of dictionaries
def calculate_new_manifest(new_files_root_dir):
  new_manifest = get_files_hash_values(new_files_root_dir)

  return new_manifest

def compare_hashes(existing_manifest, new_manifest):
  for row in new_manifest:
    print(row['hash'], row['path'])

# Change existing manifest file paths to unix format
existing_manifest_list = unixify_existing_manifest(existing_manifest)

# Calculate hash values for new files
new_manifest_list = calculate_new_manifest(new_root_dir)
print('new manifest:', new_manifest_list)

# comparison = compare_hashes(existing_manifest_list, new_manifest_list)
# print('comparison:', comparison[0])