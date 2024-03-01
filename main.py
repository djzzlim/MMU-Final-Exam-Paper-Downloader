# Copyright notice
# Copyright (c) 2024 Lim Kar Joon. All rights reserved.
import time
import os
# Check and install required libraries
try:
    import requests
    import json
except ImportError:
    print("Installing required libraries...")
    os.system('pip install requests')
    os.system('pip install json')

import requests
import json
import urllib.request

# Banner
print("""
********************************************
* MMU Final Exam Paper Downloader          *
*                                          *
* Automatically download final exam papers *
* from Multimedia University's Vlib.       *
*                                          *
* by Lim Kar Joon (2024)                   *
********************************************
""")

try:
    requests.get("http://erep.mmu.edu.my")
    print("You are connected to MMU VPN")
except:
    print("You are not connected to MMU VPN")
    input("Press Any Key To Exit...")
    quit()

def find_most_duplicates(lst):
        max_count = 0
        most_common_element = None

        for element in lst:
            count = lst.count(element)

            if count > max_count:
                max_count = count
                most_common_element = element

        return most_common_element

def download_files(file_links, output_directory):
    for link in file_links:
        filename = link.split('/')[-1]  # Get the filename from the URL
        filename = filename.replace("%20", " ")
        filename_copy = filename.replace("%20", " ")

        # Extract the file extension
        file_name, file_extension = os.path.splitext(filename)

        # Generate a unique filename by appending a suffix
        unique_filename = filename
        suffix = 1

        while os.path.exists(os.path.join(output_directory, unique_filename)):
            # If the filename already exists, add a suffix to make it unique
            unique_filename = f"{file_name}-{suffix}{file_extension}"
            suffix += 1

        file_path = os.path.join(output_directory, unique_filename)
        print(f"Downloading {filename_copy}...")
        try:
            urllib.request.urlretrieve(link, file_path)
            print(f"Downloaded {filename_copy}")
        except Exception as e:
            print(f"Failed to download {filename_copy} from {link}. Trying alternative URLs.")
            for i in range(2, 10):
                try:
                    eprintid = link.split('/')[-(i+1)]  # Get the eprintid from the URL
                    new_link = f"http://erep.mmu.edu.my/id/eprint/{eprintid}/{i}/{filename}"
                    urllib.request.urlretrieve(new_link, file_path)
                    print(f"Successfully downloaded {filename_copy}")
                    break  # Exit the loop if download is successful
                    if i == 10:
                        print("Please manually download {filename_copy}.")
                except Exception as e:
                    continue
            else:
                print(f"Failed to download {filename_copy} from all alternative URLs.")
                continue

url = 'http://erep.mmu.edu.my/cgi/search/archive/simple/export_inhousedb_JSON.js'

while True:
    # Accept simplified subject code input
    print("Example: For 'TMA 1101 - Calculus', enter 'TMA 1101'")
    print("Type 'Exit' or '' to QUIT")
    subject_code = input("Please enter Subject Code: ")

    if (subject_code == "" or subject_code == 'Exit'):
        break

    params = {
        'screen': 'Search',
        'dataset': 'archive',
        '_action_export': '1',
        'output': 'JSON',
        'exp': f'0|1|-date/creators_name/title|archive|-|q:abstract/creators_name/date/documents/title:ALL:IN:{subject_code}|-|eprint_status:eprint_status:ANY:EQ:archive|metadata_visibility:metadata_visibility:ANY:EQ:show'
    }

    response = requests.get(url, params=params)

    data = response.text

    data = data.replace("'", '"')

    parsed_data = json.loads(data)

    file = []
    filename_list = []
    title = []

    for item in parsed_data:
        titleid = item.get("title", "")
        title.append(titleid)
        eprintid = item.get("eprintid", "")
        document = item.get("documents", [{}])[0]  # Get the first document, or an empty dictionary if not found
        filename = document.get("files", [{}])[0].get("filename", "")  # Get the filename from the first file, or an empty string if not found
        filename_list.append(filename)
        filename = filename.replace(' ', "%20")
        file_link = f"http://erep.mmu.edu.my/id/eprint/{eprintid}/1/{filename}"
        file.append(file_link)


    # Get the current working directory
    cwd = os.getcwd()

    # Check if the Final Exam folder exists
    final_exam_folder = os.path.join(cwd, "Final Exam")
    if not os.path.exists(final_exam_folder):
        os.makedirs(final_exam_folder)

    # Check if the Subject Code folder exists

    subject_code_folder = os.path.join(final_exam_folder, find_most_duplicates(title))
    if not os.path.exists(subject_code_folder):
        os.makedirs(subject_code_folder)

    current_dir_list = os.listdir(subject_code_folder)

    for filename in current_dir_list.copy():  # Use copy() to iterate over a copy of the list
        if filename in filename_list:
            index = filename.index(filename)
            del file[index]

    # Download files
    download_files(file, subject_code_folder)

    print("Files downloaded successfully.")
    time.sleep(1)
    try:
        os.system("cls")
    except:
        os.system("clear")
        
try:
    os.system("cls")
except:
    os.system("clear")

print("Goodbye!!!")
