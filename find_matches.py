import argparse
import csv
import os
import time

# Reads two lists of dictionaries.
# Compares hash values between them and writes any matches to a .csv.
# Returns a list of lists.
def find_matches(list_1, list_2):
  matches = []

  # Loop through rows in *second* list to begin comparison.
  # For each item in *new* (second) manifest, check for match in existing manifest
  for item in list_2:
    path_2 = item['path']
    hash_value_2 = item['hash']

  # Compare to each row in the *first* list
  for item in list_1:
    path_1 = item['path']
    hash_value_1 = item['hash']

    # If match found, create match list and append match to matches list
    if hash_value_2 == hash_value_1:
      match = [hash_value_2, path_2, path_1]
    
    matches.append(match)

  return matches

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