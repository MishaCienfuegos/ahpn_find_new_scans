import hashlib
import os

"""
This is a rip-off of calculate_hash_values.
Modifications: Returns list of dictionaries, not csv.
Calculates sha-256 (not md5) to conform to existing manifests for AHPN.
"""

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

"""
Takes name of root directory as string
Returns a list of dictionaries for all files in the directory
containing file name, its absolute path, sha-256 hash value, and file size
"""
def get_files_hash_values(root_dir):
  all_hash_paths_list = []

  for root, dirs, files in os.walk(root_dir):
    for file in files:
      hash_path_dict = {}

      abs_path = os.path.abspath(os.path.join(root, file))
      hash_value = hash_file(abs_path)

      hash_path_dict['file'] = file
      hash_path_dict['path'] = abs_path
      hash_path_dict['hash'] = hash_value[0]
      hash_path_dict['file_size'] = hash_value[1]

      all_hash_paths_list.append(hash_path_dict)

  return all_hash_paths_list