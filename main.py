from processor import Processor

use_runtime_input = False  # Boolean to decide weather or not to use input at runtime

# Predefine
file_name = ''  # Namelist File name
group_num = 0  # Number of group
group_list = None  # Change to list "[]" if group name is applicable
final_prefix = '15 Jul 2024'  # Add the prefix of the result file name
if use_runtime_input or (file_name == '' and group_num == 0 and group_list is None):
    print('Please enter start configuration: ')
    file_name = input('Enter filename: ')
    group_num = input('Enter Number of Group: ')
    list_str = input("Enter List of Group Names(seperated by comma): ")
    if not list_str.isspace():
        group_list = list_str.split(',')
    final_prefix = input('Enter The prefix of result filename: ')

processor = Processor(file_name, group_num, group_list)

processor.make_a_group(final_prefix)

print("Processed")

