import argparse
import csv
import hashlib
import os
import time

"""
Define arguments to be passed to script
Input: -i is the root file path (required)
Output: -o is the file path for the output .csv file, default is current working directory (optional)
"""
parser = argparse.ArgumentParser(description='List md5 hash values for all files in a given root path')
parser.add_argument('-i', '--input', help='Root directory to be traversed', action='store', dest='i', required=True)
parser.add_argument('-o', '--output', help='Directory where .csv file to be output with file path, file name, and hash value', action='store', dest='o', nargs='?', default=os.getcwd())

args = parser.parse_args()

root_dir = args.i
output_dir = args.o

"""
Takes a file path.
Returns a list with its sha256 hash value and file size (bytes).
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
containing file name, its absolute path, md5 hash value, and file size
"""
def get_files_hash_values(root_dir):
    all_hash_paths_list = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            hash_path_dict = {}

            abs_path = os.path.abspath(os.path.join(root, file))
            rel_path = os.path.relpath(os.path.join(root, file))
            hash_value = hash_file(abs_path)

            hash_path_dict['file'] = file
            hash_path_dict['relpath'] = rel_path
            hash_path_dict['path'] = abs_path
            hash_path_dict['hash'] = hash_value[0]
            hash_path_dict['file_size'] = hash_value[1]

            all_hash_paths_list.append(hash_path_dict)

    return all_hash_paths_list

def write_hashes_to_csv(all_hash_path_list):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_file_name = 'file_hash_values-' + timestamp + '.csv'
    csv_out = os.path.join(output_dir, output_file_name)

    with open(csv_out, 'a', newline='') as output_csv:
        writer = csv.writer(output_csv, quotechar='"', delimiter=',')

        for file_dict in all_hash_path_list:
            out_row = [file_dict['file'], file_dict['path'], file_dict['hash'], file_dict['file_size']]
            writer.writerow(out_row)

# Create list of dictionaries for all files in the root directory
all_files_hashes = get_files_hash_values(root_dir)

# Write all file names, absolute paths, and hashes to a csv
write_hashes_to_csv(all_files_hashes)