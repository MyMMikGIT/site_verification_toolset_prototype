#-*- coding: utf-8 -*-

import io # file reading, writing with encoding
import urlparse # Parsing html for BS
import os # directory creation

# URL HANDLING
def mk_url_base(input_url):
    """ Strips an input url to base """
    base_url = urlparse.urljoin(input_url, '/')
    return base_url

def strip_to_domain(base_url):
    """ Strips url to domain """
    # Handling http and https domains
    if "https:/" in base_url:
        domain = base_url.strip("https://www.")
    else:
        domain = base_url.strip("http://www.")
    domain = domain.strip("/")
    return domain

# FILESYSTEM HANDLING
def mk_directory(*args):
    """ Makes folder for data from domain """
    path = "".join(args)
    os.makedirs(path)



#. INPUT OUTPUT MODULES
def l_of_l_write(list_data, *args):    
    """ Adds list or list with nested lists type data to file.
        Separate lines(items or joined list) are added to separate txt lines"""
    print "WRITING TO FILE...................."
    to_path = "".join(args)
    print "path: ", to_path
    # print "INPUT DATA TYPE:", type(list_data)
    total_symbol_counter = 0
    with io.open(to_path, "w", encoding='utf-8') as f:
        for sub_list in list_data:
            # can handle writing for list and non list input cases
            if type(sub_list) is list: 
                print "SUBLIST TYPE:", type(sub_list)
                line = unicode(";;;".join(sub_list) + '\n') # column separator ";;;"
                # print "line:", line
                f.write(line)
                total_symbol_counter = total_symbol_counter + len(line)
            else:
                f.write((sub_list + '\n'))
                total_symbol_counter = total_symbol_counter + len(sub_list)
    return total_symbol_counter

def l_of_l_read(*args):
    print "READING FILE and converting to A LIST OF LISTS.................."
    from_path = "".join(args)
    print "path: ", from_path
    l_of_l = []
    with io.open(from_path, 'r', encoding='utf-8') as file:
        empty_line_counter = 0
        for line in file:

            if len(line) < 3: # empty line since length is less then separator ";;;" length = 3
                empty_line_counter += 1
                    
            else:
                sub_list = line.split(';;;')
                last_item_ind = len(sub_list) - 1
                sub_list[last_item_ind] = sub_list[last_item_ind].strip('\n')
                l_of_l.append(sub_list)
        # if there was empty lines when reading the file is rewritten with corected data
        if empty_line_counter > 0:
            l_of_l_write(l_of_l, from_path) 
        else:
            pass
    return l_of_l

def simply_write(content, *args):
    """ Writes text content to txt file in """
    to_path = "".join(args)
    print "WRITING TO FILE\npath: %s" % to_path
    with io.open(to_path, "w", encoding='utf-8') as f:
        f.write(content)


def simply_read(*args):
    """ Writes text content to txt file in """
    from_path = "".join(args)
    print "READING FROM FILE\npath: %s" % from_path
    with io.open(from_path, "r", encoding='utf-8') as f:
        content = f.read()
    return content

def txt_file_append(input_list, *args):
    """ Expects list as input, converts to string with comma as separator and adds appends to file """
    string_input = ";;;".join(input_list)
    string_input = string_input + "\n"
    append_path = "".join(args)
    with io.open(append_path, "a", encoding='utf-8') as f:
        f.write(string_input)
#./
#/



# DATA PROCESSING
def remove_duplicates(a_list):
    """ Constructs a list without duplicates from input_list of items """
    print "REMOVING DUPLICATE VALUES. INPUT LIST LENGTH:", len(a_list)
    dedupli_list = []
    for item in a_list:
        if item not in dedupli_list:
            dedupli_list.append(item)
    print "DUPLICATES REMOVED. OUTPUT LIST LENGTH:", len(dedupli_list)
    return dedupli_list

