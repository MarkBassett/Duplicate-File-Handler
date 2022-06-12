import os
import sys
import hashlib

def confirmation_input(test_func):
    ask_for_input = True
    while ask_for_input:
        confirmation = input()
        if test_func(confirmation):
            ask_for_input = False
        else:
            print('Wrong option')
    return confirmation

def yes_no(confimation):
    if confimation == 'yes' or confimation == 'no':
        return True
    return False

def number_list(confirmation):
    if confirmation != '':
        if confirmation[0].isdigit():
            return True
    return False

args = sys.argv
file_list = {}
if len(args) < 2:
    print('Directory is not specified')
else:
    root_folder = args[1]
    print(root_folder)
    for root, dirs, files in os.walk(root_folder):
        for name in files:
            file_path = os.path.join(root, name)
            size = str(os.path.getsize(file_path)) + ' bytes'
            if size in file_list:
                file_list[size].append(file_path)
            else:
                file_list[size] = [file_path]
    print('Enter file format:')
    file_format = input()
    print('Size sorting options:')
    print('1. Descending')
    print('2. Ascending')
    wrong_input = True
    while wrong_input:
        sort_option = int(input())
        if sort_option < 0 or sort_option > 2:
            print('Wrong option')
        else:
            wrong_input = False

    if sort_option == 1:
        sizes = sorted(file_list, reverse=True)
    else:
        sizes = sorted(file_list)
    for size in sizes:
        print(size)
        for file in file_list[size]:
            file_hash = ''
            if file_format in file or not file_format:
                print(file)

    print('Check for duplicates?')
    check_for_duplicates = confirmation_input(yes_no)

    if check_for_duplicates == 'yes':
        possible_duplicates = {}
        duplicates = {}
        file_hash = ''
        for size in sizes:
            possible_duplicates[size] = {}
            for file in file_list[size]:
                if file_format in file or not file_format:
                    with open(file, 'rb') as data:
                        file_data = data.read()
                        file_hash = hashlib.md5(file_data).hexdigest()
                        if file_hash in possible_duplicates[size]:
                            possible_duplicates[size][file_hash].append(file)
                        else:
                            possible_duplicates[size][file_hash] = [file]
        for size in possible_duplicates:
            for file_hash in possible_duplicates[size]:
                if len(possible_duplicates[size][file_hash]) > 1:
                    if size in duplicates:
                        duplicates[size].update({file_hash: possible_duplicates[size][file_hash]})
                    else:
                        duplicates[size] = {file_hash: possible_duplicates[size][file_hash]}
        count = 0
        deletable_files = {}
        for size in duplicates:
            print(size)
            for file_hash in duplicates[size]:
                print(f'Hash: {file_hash}')
                for file in duplicates[size][file_hash]:
                    count += 1
                    deletable_files[str(count)] = [file, size]
                    print(f'{count}. {file}')
    print('Delete files?')
    delete_files = confirmation_input(yes_no)
    if delete_files == 'yes':
        files_to_delete = confirmation_input(number_list)
        files_to_delete = files_to_delete.strip().split()
        total_space = 0
        for file in files_to_delete:
            os.remove(deletable_files[file][0])
            space = int(deletable_files[file][1].split()[0])
            total_space += space
        print(f'Total freed up space: {total_space} bytes')
