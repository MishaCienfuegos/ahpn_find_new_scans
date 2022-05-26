import argparse
import csv
import os
import time

# Reads two lists of dictionaries.
# Compares hash values between them and writes any matches to a .csv.
# Returns a list of lists.
def find_new_assets(list_1, list_2):
  copy_list = list_2

  # Loop through rows in *second* list to begin comparison.
  # For each item in *new* (second) manifest, check for match in existing manifest
  for idx, new_asset in enumerate(copy_list):
    path_2 = new_asset['path']
    hash_value_2 = new_asset['hash']

    # Compare to each row in the *first* list
    for existing_asset in list_1:
      path_1 = existing_asset['path']
      hash_value_1 = existing_asset['hash']

      # If match found, cease looping through first list;
      # Remove this item from copy_list
      if hash_value_2 == hash_value_1 and hash_value_2 == copy_list[idx].get('hash'):
        print('copy list hash:', copy_list[idx].get('hash'))
        print('hash value 2:', hash_value_2)
        copy_list.remove(copy_list[idx])

  # print('copy list:', copy_list, len(copy_list))
  return copy_list

# def write_lists_to_csv(matches):
#   timestamp = time.strftime("%Y%m%d-%H%M%S")
#   output_file_name = 'matched_hashes-' + timestamp + '.csv'

#   # If no matches found, do not write csv, return message
#   if len(matches) <= 0:
#     print('No matches found.')

#   # Else, write each match to a csv row
#   else:
#     with open(output_file_name, 'a', newline='', encoding='utf-8') as output_csv:
#       writer = csv.writer(output_csv, quotechar='"', delimiter=',')
        
#       for match in matches:
#         writer.writerow(match)

# Create list of lists for all hash value matches found between csv 1 & csv 2
# matches = find_matches(csv_path_1, csv_path_2)

# Write hash value, first file name & path, and second file name & path to csv
# write_lists_to_csv(matches)