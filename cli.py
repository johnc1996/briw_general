import json
import sys
import re
import model

# Global

persist_file_path = 'persist.json'

persist_dict = {}

mode_verbs = ['get', 'add', 'read', 'write']
modes_expected = ['get-people', 'get-drinks', 'get-favourites', 'add-drinks', 'add-people', 'add-favourites',
                  'read-json', 'write-json']
border = 20*"=" + '\n'

# user specified
max_arg_count = 2


def read_persist_file():
    with open(persist_file_path, 'r') as fh:
        return json.load(fh)


def write_persist_file():
    with open(persist_file_path, 'w') as fh:
        return json.dump(persist_dict, fh)


def print_header(header_str):
    print(f"{border}{header_str}\n{border}")


def print_row(row_data):
    print(f"|    {row_data}\n")


def print_footer():
    print(border)


def print_table(table_name):
    print_header(table_name)
    for key, data_item in persist_dict[table_name].items():
        row_data = key + "    " + data_item
        print_row(row_data)
    print_footer()


def print_favourites():
    table_name = "favourites"
    print_header(table_name)
    for key, data_item in persist_dict[table_name].items():
        row_data = get_people_name_by_id(key) + "    " + get_drink_name_by_id(data_item)
        print_row(row_data)
    print_footer()


def get_people_id_by_name(name):
    people_id = None
    for table_id, table_name in persist_dict['people'].items():
        if table_name == name:
            people_id = table_id
    return people_id


def get_people_name_by_id(id):
    return persist_dict['people'][id]


def get_people_id_by_name(name):
    people_id = None
    for table_id, table_name in persist_dict['people'].items():
        if table_name == name:
            people_id = table_id
    return people_id


def get_drink_name_by_id(id):
    return persist_dict['drinks'][id]


def get_drink_id_by_name(name):
    drink_id = None
    for table_id, table_name in persist_dict['drinks'].items():
        if table_name == name:
            drink_id = table_id
    return drink_id


def get_new_key(table):
    max_key = 1
    for key, value in persist_dict[table].items():
        num_key = int(key)
        if num_key > max_key:
            max_key = num_key
    max_key = max_key + 1
    return str(max_key)


def set_new_person(name):
    has_set = False
    if get_people_id_by_name(name) is None:
        new_key = get_new_key('people')
        pseudo_db['people'][new_key] = name
        has_set = True
    return has_set


def get_data_id_by_name(table_name, name):
    primary_id = None
    for table_id, table_name in persist_dict[table_name].items():
        if table_name == name:
            primary_id = table_id
    return primary_id


def set_new_generic(table_name, data_item):
    has_set = False
    if get_data_id_by_name(table_name, data_item) is None:
        new_key = get_new_key(table_name)
        persist_dict[table_name][new_key] = data_item
        has_set = True
    return has_set       


def set_new_drink(name):
    has_set = False
    if get_drink_id_by_name(name) is None:
        new_key = get_new_key('drinks')
        pseudo_db['drinks'][new_key] = name
        has_set = True
    return has_set


def set_favourite(person, drink):
    person_id = get_people_id_by_name(person)
    drink_id = get_drink_id_by_name(drink)
    persist_dict['favourites'][person_id] = drink_id


def print_interactive_msg():
    msg_interactive = """
    some_app - interactive mode

    Enter an integer to enter a particular mode:
    """
    print(msg_interactive)
    mode_str = ""
    mode_integer = 1
    for mode in modes_expected:
        print("[%s] - %s " % (int(mode_integer), mode))
        mode_integer += 1


def validate_interactive_input(mode_integers):
    # TODO
    valid = True
    return valid


def clean_input(in_str):
    in_str = in_str.strip()
    in_str = in_str.lower()
    in_str = re.sub("[^a-zA-Z0-9\-\ ]", int_str)
    return in_str
   

def method_handler(mode):
    current_verb = mode.split('-')[0]
    current_data = mode.split('-')[-1]

    if current_verb == 'read':
        persist_dict = read_persist_file()
    elif current_verb == 'write':
        write_persist_file()
    elif current_verb == 'get':
        print_table(current_data)
        if current_data == 'favourites':
            print_favourites()
    elif current_verb == 'add':
        if current_data in ['people', 'drinks']:
            new_value = input('Enter a single value for %s: ' % current_data)
            new_value = clean_input(new_value)
            set_new_generic(current_data, new_value)
        elif current_data in ['favourites']:
            new_value = input('Enter a favourite pair separted by a comma eg ' 
                              'jane,goats milk %s: ' % current_data)
            person_name = clean_input(new_value.split(',')[0])
            drink = clean_input(new_value.split(',')[1])
            set_favourite(person_name, drink)
    
    write_persist_file() # force write


def validate_cli_input():   
    is_interactive = False
    """
    expected formats

    [cli.py] - interactive mode
    [cli.py <command-verb>-<object/data>]

    """ 
    args = sys.argv
    arg_count = len(args)
    
    if arg_count > max_arg_count - 1:
        print('Input failed :Argument count greater than %s' % arg_count)
        exit()


def sanitise_cli_input():
    pass


def sanitise():
    # clean/sanitise
    pass


def is_valid_mode():
    is_valid = False


def get_args():
    mode = 'interactive'
    """
    expected formats

    [cli.py] - interactive mode
    [cli.py <command-verb>-<object/data>]

    """ 
    args = sys.argv
    arg_count = len(args)
    
    if arg_count > max_arg_count - 1:
        print('Input failed :Argument count greater than %s' % arg_count)
        exit()
    elif arg_count == 1:
        mode = 'interactive'
    else:
        mode = args[1]

    return mode


persist_dict = read_persist_file()
mode = get_args()
session = model.make_session()

if mode == 'interactive':
    while True:

        print_interactive_msg()
        mode_integer = int(input())
        if not validate_interactive_input(mode_integer):
            print('Input invalid, try again')
        mode = modes_expected[mode_integer-1]
        method_handler(mode)

        should_continue = 'k'
        while should_continue not in ['y', 'n']:
            should_continue = input('Do you wish to continue? y/n?')

        if should_continue == 'n':
            break
else:
    method_handler(mode)
