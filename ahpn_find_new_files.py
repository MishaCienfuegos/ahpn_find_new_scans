import argparse
import csv
import hashlib
import os
import re
from sysconfig import get_path
import time

# TODO add args, not hardcoded file paths

# File path to manifest (.csv) for materials already written to tape
existing_manifest_csv_path = 'test_files/2_1_2018.csv'

# File path to directory containing most recent submission from AHPN
new_files_dir = '../../../../../ahpn/misha_test/ahpn_2019/2/1'

# TODO DUMMY DATA FOR TESTING PURPOSES, DELETE
# new_manifest_list = [
#   {'file': '17427196.tif', 'rel_path': 'dummy_path', 'path': '2/1/17427196.tif', 'hash': 'ea756afc8bb793d9dda6b6ef8086c62f2065a295c59bc95680eed5d53d6b4c68', 'file_size': 50545},
#   {'file': '17427197.tif', 'rel_path': 'dummy_path', 'path': '2/1/17427197.tif', 'hash': 'b3f35eda4bbbf5ed40adbba4104e584969c16332df846a2f289dcad6f5380898', 'file_size': 131168},
#   {'file': '17427198.tif', 'rel_path': 'dummy_path', 'path': '2/1/17427198.tif', 'hash': '3e4f7e27c5742dbbc55bf019a827409f9bbb2cec556ddfc923e4d293d480e88c', 'file_size': 154177},
#   {'file': '17427199.tif', 'rel_path': 'dummy_path', 'path': '2/1/17427199.tif', 'hash': '24b30fc3fcdadf9e0bb36e6be3e2084ab35e7ec140110395d4c88b575bed3329', 'file_size': 68948},
#   {'file': '17427200.tif', 'rel_path': 'dummy_path', 'path': '2/1/17427200.tif', 'hash': '4bdf0fe0cc6a870d793768a6c5d624c927cb07e97bb9cf231f42085a67914e93', 'file_size': 156391},
#   {'file': '10014110.tif', 'rel_path': 'dummy_path', 'path': '2/1/10014110.tif', 'hash': '80fb9ac2daf2cf5c7ee59b6fd5d423641eab110da771a9c3c39722a316d62abe', 'file_size': 183623},
#   {'file': '17427201.tif', 'rel_path': 'dummy_path', 'path': '2/1/17427201.tif', 'hash': '56e716a99e86444d88545a2ca3ee7fbff4d515727d5aba0f75a66fb89b592286', 'file_size': 99158},
#   {'file': 'bogus.tif', 'rel_path': 'dummy_path', 'path': '2/1/bogus.tif', 'hash': 'fakefakefakefakefakefakefakefakefakefake9b592286', 'file_size': 99158},
#   {'file': 'bogus.tif', 'rel_path': 'dummy_path', 'path': '2/1/extra-bogus.tif', 'hash': '56e716a99e86444d88545a2ca3ee7fbff4d515727d5aba0f75a66fb89b592286', 'file_size': 99158},
#   {'file': '17427863.tif', 'rel_path': 'dummy_path', 'path': '2/1/17427863.tif', 'hash': 'ba918760d29b63a8cdb37fde90c9b6dae91393ea525a3ef06beb8522b73d10fc', 'file_size': 17172},
#   {'file': '17470374.tif', 'rel_path': 'dummy_path', 'path': '2/1/17470374.tif', 'hash': 'd791fb8a28f886dae9781b689b1c66ba064b7a81db225d896c0cd4a718a3ee15', 'file_size': 115478},
#   {'file': '17470375.tif', 'rel_path': 'dummy_path', 'path': '2/1/17470375.tif', 'hash': '79aa184189b9ac2b5401a32f9522e6bc6cf766d04e649467e0e8892f79087b31', 'file_size': 124963},
#   {'file': '17470376.tif', 'rel_path': 'dummy_path', 'path': '2/1/17470376.tif', 'hash': '991643e3c890962c2dd7b7ab52fb7e2ba24ae4158e431c13035998ad437400dd', 'file_size': 1246816},
#   {'file': '11193087.tif', 'rel_path': 'dummy_path', 'path': '/mnt/ahpn/misha_test/ahpn_2019/2/1/11193087.tif', 'hash': 'ea411a0f9529b173d0ecd719782f7a93d323d8bc061c6cb84326c22ca5d7273a', 'file_size': 34120},
#   {'file': '11194577.tif', 'rel_path': 'dummy_path', 'path': '/mnt/ahpn/misha_test/ahpn_2019/2/1/11194577.tif', 'hash': '5a26bcda9b9029b2e9080feeab708ddbf90b752fe61ec1079b92769cca2bef98', 'file_size': 32518}
# ]

# =====================================
# FUNCTIONS
# =====================================

# Takes file path to existing manifest csv
# Converts Windows file paths to Unix style
# Returns list of dictionaries with a hash and file path for each item
def unixify_existing_manifest(existing_manifest_path):
  print('Preparing existing manifest for comparison...')
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

# Gets the top-level directory from provided path (string)
def get_path_root(path):
  # after ',' through the first '/'
  regex = '\w*/'
  path_start = re.search(regex, path)

  return path_start.group()

# Takes a file path.
# Returns a list of lists with its sha-256 hash value and file size (bytes).
def hash_file(file_path):
    hash = hashlib.sha256()
    buffer_size = 65536
    hash_value = ''

    # Print dialog for each file while calculating hash
    print('Calculating hash for:', file_path)

    with open(file_path, 'rb') as file:
        while True:
            data = file.read(buffer_size)
            if not data:
                break
            hash.update(data)

    file_size = os.path.getsize(file_path)
    hash_value = [hash.hexdigest(), file_size]

    return hash_value

# Takes file path to new files directory (2019 disk)
# Uses existing manifest path to determine root of new manifest path (so they're comparable)
# Returns list of dictionaries with file name, its absolute path, sha-256 hash value, and file size
def calculate_new_manifest(new_files_root_dir, existing_manifest_list):
  print('Calculating new manifest for', new_files_root_dir)

  new_manifest_list = []
  existing_path_example = existing_manifest_list[3]['path']
  existing_path_root = get_path_root(existing_path_example)

  for root, dirs, files in os.walk(new_files_root_dir):
    for file in files:
      hash_path_dict = {}

      full_path = os.path.relpath(os.path.join(root, file))
      abs_path = os.path.abspath(os.path.join(root, file))

      # Split new manifest relative path on the root of the existing manifest path
      # Concatenate path root to back half of full path
      split_path = re.split(existing_path_root, full_path)
      path = existing_path_root + split_path[1]

      hash_value = hash_file(abs_path)

      hash_path_dict['file'] = file
      hash_path_dict['full_path'] = full_path
      hash_path_dict['path'] = path
      hash_path_dict['hash'] = hash_value[0]
      hash_path_dict['file_size'] = hash_value[1]

      new_manifest_list.append(hash_path_dict)

  return new_manifest_list

# Find matches, then subtract list of matches from new files list
def find_matches(existing_manifest_list, new_manifest_list):
  matches = []

  # Loop through rows in first file to begin comparison
  for row in existing_manifest_list:
    hash_1 = row['hash']
    path_1 = row['path']

    # Compare to each row in new_manifest_list
    # NOTE: A match has the same hash value AND same file path
    for row in new_manifest_list:
      hash_2 = row['hash']
      path_2 = row['path']
      file_name_2 = row['file']

      # If match found, create match list and append match to matches list
      if hash_1 == hash_2 and path_1 == path_2:
          match = {
            'hash': hash_1, 
            'existing_path': path_1,
            'path': path_2, 
            'file': file_name_2
          }
          
          matches.append(match)

  return matches

def subtract_lists(new_manifest_list, match_list):
  copy_list = new_manifest_list
  match_hashes = [item['hash'] for item in match_list]
  match_paths = [item['path'] for item in match_list]
  print('match paths:', len(match_paths))

  # If hash is same and file path is different, keep in copy list
  copy_list[:] = [item for item in copy_list if item.get('hash') not in match_hashes or item.get('path') not in match_paths]
  return copy_list

# Takes a list and a string to use in a descriptive name for the output csv
# Writes path and hash to csv, as well as file name and size, if available
def write_list_to_csv(list, name):
  timestamp = time.strftime("%Y%m%d-%H%M%S")
  output_file_name = 'aphn_' + name + '-' + timestamp + '.csv'

  # If no matches found, do not write csv, return message
  if len(list) <= 0:
    print('No unmatched files to copy.')

  # Else, write each match to a csv row
  else:
    with open(output_file_name, 'a', newline='', encoding='utf-8') as output_csv:
      writer = csv.writer(output_csv, quotechar='"', delimiter=',')
        
      for row in list:
        out_row = [row['hash'], row['path']]
        if 'full_path' in row:
          out_row.append(row['full_path'])
        if 'file' in row:
          out_row.append(row['file'])
        if 'file_size' in row:
          out_row.append(row['file_size'])
        writer.writerow(out_row)

# =====================================
# EXECUTE
# =====================================

# Step 1:
# Change existing manifest file's paths to unix format
# and make convert csv to list
existing_manifest_list = unixify_existing_manifest(existing_manifest_csv_path)

# Step 2:
# Calculate hash values for new files and create a list
# Write new_manifest_list to csv for future reference
# NOTE: This step is long on my local machine; use DUMMY DATA above for simple testing
new_manifest_list = calculate_new_manifest(new_files_dir, existing_manifest_list)
write_list_to_csv(new_manifest_list, 'new_manifest_list')
print('new manifest list', new_manifest_list[0])

# Step 3:
# Find matches between new_manifest_list and existing_manifest_list
match_list = find_matches(existing_manifest_list, new_manifest_list)
if match_list:
  print('match list:', match_list[0])
  write_list_to_csv(match_list, 'match_list')

# TODO this is for testing; copy list should equal length difference for "real" data
new_manifest_length = len(new_manifest_list)
match_list_length = len(match_list)
list_difference = new_manifest_length - match_list_length

print('new manifest list length:', new_manifest_length)
print('match list length:', match_list_length)
print('difference:', list_difference)

# Step 4:
# Subtract match_list from new_manifest_list
copy_list = subtract_lists(new_manifest_list, existing_manifest_list)

if copy_list:
  print('copy list length:', len(copy_list))
  write_list_to_csv(copy_list, 'copy_list')
