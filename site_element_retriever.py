#-*- coding: utf-8 -*-

""" Manual """
# Place script to whatever destination with related folder, install absent Python modules
# Place some input urls to site_data\\0_1_input_urls.txt file in format: whatever;;;link
# One link per line
# 
# Execute the script

""" Describtion """
# All common paths are stored in Common_Paths class

# Site_Link_Manager():
# Manages higher level site main links and control their status in a process chain: 
# - duplicate check according to base url (DUPLICATE_BASE_URL)
# - id generation and assignment to site base links
# - succefull extraction confirmation output to 1_ready_for_veri.txt file

# HTML_File_Maker():
# Takes a link provided by Link_Module_Driver()  as inputs, strips link to base url (home page)
# collects all internal links present in homepage and saves htmls to "site_data\\html\\" folder

# Text_Extractor():
# extracts visible text from site, compares between pages and leaves unique only, saves to "site_data\\text\\" folder

# Translator():
# Takes text files as input and outputs copies in english (text_eng\\)
# Notice: Output text is one line with no paragraph separation

# Link_Module_Driver()
# Takes main input - 0_1_input_urls.txt cycles links and modules
# Acts as controlling application where separate modules can commented out (deactivated) if needed

# site_data\\page_list.txt
# Index of site page specific data and file_names

from bs4 import BeautifulSoup as BS # for data extraction
import urllib2 # open url for reading
import urlparse # Parsing url for base url extraction
import os # domain folder creation mkdir(); script file destination path collection
import time # for time delays when accesing traffic sensitive stuff
import io # for encoding handling when writing to files
import common_methods as c_m # custom common to modules and script input output, deduplication and other methods
from copy import copy # making copies of lists and dictionaries


# for Link_Manager module link ids
import datetime

# modules needed for translator operation:
import pyperclip # clipboard access with unicode character
from selenium import webdriver # for chrome intance
from selenium.webdriver.common.keys import Keys # for sending commands to instance elements
from selenium.webdriver.chrome.options import Options # for chrome extension presence in the instance




# page_link = "http://tingvallabyggtjanst.se/" # Test link. A list of links will be provided.	

# Methods needed for url handling: extracting base_url, deduplication of urls ect.

class Common_Paths(object):
    def __init__(self, input_url):
        self.input_url = input_url
        print "INIT INPUT URL:", self.input_url
        self.base_url = c_m.mk_url_base(self.input_url) # home_page
        print "INIT BASE URL:", self.base_url
        self.domain = c_m.strip_to_domain(self.base_url)
        print "INIT DOMAIN:", self.domain
        # base paths:
        self.static_part_path = "site_data\\"
        self.pc_specific_part_path = os.path.dirname(os.path.realpath(__file__)) + "\\"
        self.main_path = self.pc_specific_part_path + self.static_part_path
        print "INIT MAIN PATH:", self.main_path


        # dynamic part path:
        self.domain_folder_name = self.domain + u"\\"
        self.domain_folder_path = self.main_path + self.domain_folder_name

        self.page_list_f_name = u"page_list.txt" #site pages' data and data file names destination
        self.page_list_path = self.main_path + self.domain_folder_name + self.page_list_f_name

        # module specific paths
        self.html_folder_name = u"html\\" # retrieved html ouput files folder
        self.text_folder = u"text\\" # output unique text files folder  
        self.eng_text_folder = u"text_eng\\" # translated text output files folder

        self.text_folder_path = self.domain_folder_path + self.text_folder
        self.text_eng_folder_path = self.domain_folder_path + self.eng_text_folder


    def mk_filesystem(self, folder_name):
        """ Creates needed for module operation folders"""
        try:
            print "%s FOLDER" % folder_name
            c_m.mk_directory(self.main_path, self.domain_folder_name, folder_name)
        except WindowsError:
            print "'%s' FOLDER ALREADY IN PLACE" % folder_name

class Site_Link_Manager(Common_Paths):
    def __init__(self, input_url):
        super(Site_Link_Manager, self).__init__(input_url)
        # link filesystem file NAMES
        self.vr_file_name = "1_ready_for_veri.txt" # if empty an empty list is added with other lists, and this changes nothing
        self.dupli_file_name = "0_2_duplicates.txt" # dupli file will not be read appended only


        # link filesystem file PATHS
        self.vr_file_path = self.main_path + self.vr_file_name
        self.dupli_file_path = self.main_path + self.dupli_file_name

        self.old_id_list = [] # used for next id generation

    def check_if_duplicate(self):

        # loads lists from ready, verified as good and bad text files
        print "READing VERI READY LIST"
        veri_ready_list = c_m.l_of_l_read(self.vr_file_path)
        print "READ VERI GOOD"
        veri_good_list = c_m.l_of_l_read(self.vg_file_path)
        print "READ VERI BAD"
        veri_bad_list = c_m.l_of_l_read(self.vb_file_path)

        #/
        print "MERGING TO ALL ENTRIES LISTS......"
        old_entries_list = veri_ready_list + veri_good_list + veri_bad_list # adding all lists into one

        print "EXTRACTING BASE URL FOR DUPLI CHECKING END ID AS LINK"
        old_base_url_id_dict = {}
        for entry in old_entries_list:
            current_site_link_id = entry[0]
            
            print "CURRENT ENTRY", entry
            current_site_base_url = entry[3]
            old_base_url_id_dict[current_site_base_url] = current_site_link_id

            self.old_id_list.append(current_site_link_id) # for next id generation

        try:
            old_base_url_id_dict[self.base_url]
            print "DUPLICATE LINK FOUND"
            print "ADDING TO DUPLICATE link FILE\npath:%s" % self.dupli_file_path
            dupli_entry_pack = [old_base_url_id_dict[self.base_url], "DUPLICATE_BASE_URL", self.base_url]
            c_m.txt_file_append(dupli_entry_pack, self.dupli_file_path)
            return True
        except KeyError:
            print "INPUT SITE LINK IS UNIQUE"
            return False

        
    def make_next_id(self): # INTERNAL METHOD: add_to_veri_good

        # today date
        str_today = str(datetime.date.today())
        clean_str_today = str_today.replace('-','')

        # looking for today ids if not found assigns the fisrst id for the day
        today_link_number_component = []
        for old_id in self.old_id_list:
            split_id = old_id.split('_') # splitting id into "date"  "day entry count" components
            print "split_id:", split_id
            date_id_component = split_id[0]
            print "TEST TODAY DATE", clean_str_today
            print "DATE ID COMPONENT", date_id_component
            if clean_str_today == date_id_component:
                today_link_number_component.append(int(split_id[1]))

        if len(today_link_number_component) > 0:
            last_added_link_number = max(today_link_number_component)
            next_link_id_no = last_added_link_number + 1
            next_id_4digits_no = "%04d" % next_link_id_no
            next_id = clean_str_today + "_" + next_id_4digits_no
            return next_id

        else: # this is first link processed today
            next_id = clean_str_today + "_" + "0000"
            return next_id

    def add_to_veri_good(self):
        next_id = self.make_next_id()
        entry_data_pack = [next_id, "READY_FOR_VERI", self.input_url, self.base_url]
        c_m.txt_file_append(entry_data_pack, self.vr_file_path)

class HTML_File_Maker(Common_Paths):
    def __init__(self, input_url):
        super(HTML_File_Maker, self).__init__(input_url)
        self.domain_file_name = "page_0.html"
        self.mk_filesystem(self.html_folder_name) # creates folder for html output        
        # page list parameters:

        self.link_contains_separator = "link_contains_separator.txt"
        self.page_list = []
        #/
        self.links_contain_seprator = []
        self.bs_object_dict = {} # link as key, bs_object as item, returned after last module operation

    # components for domain links scraping
    def retrieve_html(self, input_url, domain_folder_name, data_type, file_name):
        """ Retrieves html from url and write to txt or from txt file if palready present"""
        print "RETRIEVING HTML CODE FOR PAGE:", input_url
        try:
            from_path = "%s%s%s%s" % (self.main_path, domain_folder_name, data_type, file_name)
            print "HTML CODE RETRIEVED LOCALY\npath:%s" % from_path
            with io.open(from_path, "r", encoding='utf-8') as f:
                content = f.read()
            bs_object = BS(content, 'html.parser')
            return bs_object
            
        except IOError:
            print "RETRIEVING HTML CODE ONLINE"

            # time_to_sleep = 2
            # print "SLEEPING FOR %d s................." % time_to_sleep
            # time.sleep(time_to_sleep)

            response = urllib2.urlopen(input_url)
            content = response.read()

            # for always proper utf-8 encoding
            bs_object = BS(content, 'html.parser')
            bs_content = bs_object.prettify('utf-8')
            u_content = unicode(bs_content, 'utf-8')
            #/

            to_path = "%s%s%s%s" % (self.main_path, domain_folder_name, data_type, file_name)
            print "WRITING RETRIEVED HTML_CODE TO FILE\npath:%s" % to_path
            with io.open(to_path, "w", encoding='utf-8') as f:
                f.write(u_content)

            # print "html WRITTEN to %s.txt" % file_name
            return bs_object

    def mk_link_list(self, BS_object, base_url):
        """ Find all links in html, constructs full links from part and makes a list"""
        link_list = []
        body = BS_object.find('body')
        for element in body.find_all('a'):
        # for link in BS_object.find_all('a'): # TEST if there are any links in html head
        
            raw_link = element.get('href')
            print "GETS RAW LINK: %r" % raw_link
            if "https:/" in raw_link or "http:/" in raw_link:
                print "FOUND FULL LINK", raw_link
                if raw_link.startswith(base_url): # Internal URL check
                    print "FULL LINK STARTS WITH BASE URL AND IS GOOD FOR LINK LIST"
                    link_list.append(raw_link)
                else:
                    print "THIS FULL LINK IS NOT INTERNAL LINK"
            else:
                # when part link found it will be always internal link
                print "FOUND PART LINK", raw_link
                try:
                    raw_link.strip()
                except:
                    pass
                print "MAKING FULL LINK FROM PART"
                full_link = urlparse.urljoin(base_url, raw_link)
                print "FULL LINK MADE FROM PART LINK", full_link
                if full_link.startswith(base_url): # Internal URL check
                    print "FULL LINK STARTS WITH BASE URL AND IS GOOD FOR LINK LIST"
                    link_list.append(full_link)
                else:
                    print "THIS FROM PART TO FULL LINK IS NOT INTERNAL LINK"



        dedupli_list = c_m.remove_duplicates(link_list) # 
        dedupli_list.sort()
        try:
            dedupli_list.remove(base_url) # we do not need retriving base url html again
            print "LINK LIST AFTER BASE URL REMOVAL", len(dedupli_list)
        except ValueError:
            print "mk_link_list: NO BASE URL FOUND"

        return dedupli_list

    #/
    # Main modules

    def scrape_domain_int_links(self):
        BS_object = self.retrieve_html(self.base_url, self.domain_folder_name, self.html_folder_name, self.domain_file_name)
        print "BS OBJECT CREATED"
        domain_link_list = self.mk_link_list(BS_object, self.base_url) # internal if full link has base url
        self.bs_object_dict[self.base_url] = BS_object
        print "LINKS RETRIEVED AND PROCESSED TO LEAVE ONLY INTERNAL AND UNIQUE LINKS\n%r" % len(domain_link_list)
        self.page_list.append([self.base_url, self.domain_file_name]) # first entry to page list
        return domain_link_list


    def mk_htmls(self):
        """ Makes unicode local html copies
        creates page_list file with file_name and respective link url as data entries"""

        domain_link_list = self.scrape_domain_int_links()
        # driving links, to collect htmls from web and create htmls with removed img elements
        for ind in range(len(domain_link_list)):
            page_file_name = "page_" + str(ind + 1) + ".html" # gen file names for html file of page on site
            active_page_link = domain_link_list[ind]
            if ";;;" in active_page_link: # separator problems hedging
                self.links_contain_seprator.append([active_page_link, page_file_name])
                print "LINK CONTAINS SEPARATOR, CAN NOT ADD TO PAGE LIST, WILL RUIN DATASYSTEM, WILL BE ADDED TO SEPARATE FILE"
            else:
                BS_object = self.retrieve_html(active_page_link, self.domain_folder_name, self.html_folder_name, page_file_name)
                self.page_list.append([active_page_link, page_file_name])
                self.bs_object_dict[active_page_link] = BS_object
        # if no ";;;" separator found in link, then write as usual
        if len(self.links_contain_seprator) > 0:
            c_m.l_of_l_write(self.links_contain_seprator, self.main_path, self.domain_folder_name, self.link_contains_separator)
        else:
            c_m.l_of_l_write(self.page_list, self.main_path, self.domain_folder_name, self.page_list_f_name)
        return self.bs_object_dict

class Text_Extractor(Common_Paths):
    def __init__(self, input_url):
        super(Text_Extractor, self).__init__(input_url)
        self.mk_filesystem(self.text_folder) # creates folder for txt output
        self.page_list = c_m.l_of_l_read(self.page_list_path) # retrive page_list from file as list of lists

    def extract_page_text(self, bs_object):
        """ Extracts html page text"""

        # kill all script and style elements
        for script in bs_object(["script", "style", "head"]):
            script.extract()    # rip it out

        # get text
        text = bs_object.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text_list_gen = (chunk for chunk in chunks if chunk)
        text_list = list(text_list_gen)
        # print "TEXT LIST >>>\n", text_list
        
        return text_list

    def mk_text_files(self, bs_object_dict):

        print "MAKING UNIQUE PAGE TEXT FILES"
        print "TOTAL PAGES TO BE PROCESSED", len(self.page_list)
        for ind in range(len(self.page_list)):

            copy_page_list = copy(self.page_list)
            poped_page_data_entry = self.page_list[ind]

            #forming page text file name
            split_page_html_f_name = poped_page_data_entry[1].split('.')
            page_text_f_name = split_page_html_f_name[0] + "_text.txt"

            #making a list of site text line, with active page excluded to be able to find unique text lines
            self.page_list[ind].append(page_text_f_name)

            copy_page_list.pop(ind)
            active_page_excluded_txt_l_list = []
            for data_line in copy_page_list:
                active_link = data_line[0]
                active_bs_object = bs_object_dict[active_link]
                page_text_list = self.extract_page_text(active_bs_object)
                active_page_excluded_txt_l_list = active_page_excluded_txt_l_list + page_text_list

            #removing duplicates from almost all text list
            clean_excluded_txt_l_list = c_m.remove_duplicates(active_page_excluded_txt_l_list)

            #checking if text lines from active page link are present in other pages
            poped_bs_object = bs_object_dict[poped_page_data_entry[0]]
            poped_page_text_list = self.extract_page_text(poped_bs_object)
            unique_text_line_list = []
            for text_line in poped_page_text_list:
                if text_line not in clean_excluded_txt_l_list:
                    unique_text_line_list.append(text_line)
                else:
                    pass

            #counting lengths of texts for sorting and writing text to file
            symbols_written_to_page = c_m.l_of_l_write(unique_text_line_list, self.text_folder_path, page_text_f_name) # write_to_file
            self.page_list[ind].append(str(symbols_written_to_page))

            print self.page_list[ind][2], "DONE"
        
        c_m.l_of_l_write(self.page_list, self.page_list_path) #write new page list

        

class Translator(Common_Paths):
    def __init__(self, input_url):
        super(Translator, self).__init__(input_url)

        # starts chrome with translate app
        self.options = Options()
        self.options.add_argument('load-extension=C:\\Users\\MuMu\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\aapbdbdomjkkjkaonfhkkikfgjllcleb\\2.0.6_0')
        self.driver = webdriver.Chrome(chrome_options=self.options)

        # creates folder for txt_eng output
        self.mk_filesystem(self.eng_text_folder)

    def mk_eng_txt_files(self):

        """ Takes a list of texts parts feeds to translate,
        gets the translated text,
        stacks it together"""

        self.page_list_path
        self.text_folder_path
        main_path = 'E:\\Python_work_files\\Projects\\site_data'
        main_list_f_name = "main_list.txt"
        new_page_list = []

        print "RETRIEVING MAIN_LIST.........."
        main_list = c_m.l_of_l_read(self.page_list_path)

        # iterating throug unique text per page txts
        for data_set in main_list:

            p_text_f_name = data_set[2]
            print "TRANSLATING TEXT FROM FILE %s" % p_text_f_name

            eng_p_text_f_name = "eng_" + p_text_f_name
            error_eng_p_text_f_name = "error_" + eng_p_text_f_name

            page_text = c_m.simply_read(self.text_folder_path, p_text_f_name)

            # if page has less than 10 symbols it is not translated
            if len(page_text) < 10:
                c_m.simply_write(page_text, self.text_eng_folder_path, eng_p_text_f_name)
                continue

            # initial text output value for while loop
            text_output = ""

            # loop safety paramters
            track_while_loops = 0
            max_while_loops = 5


            # sleep times for not to abuse translate and for every part to work:
            ext_get_sleep = 2
            text_translate_sleep = 1
            text_paste_sleep = 1
            text_copy_to_clip_sleep = 1

            # big while cycle to submit input as long as no output is generated
            while len(text_output) == 0:
                # eternal loop safeguard
                if track_while_loops > max_while_loops:
                    # raise error
                    print "MAXIMUM TRIES TO TO TRANSLATE THE SAMPLE EXEEDED \npath: %s\\%s\\eng_TXT\\%s" % (main_path, self.domain, error_eng_p_text_f_name)
                    error_massage = "error when translating page"
                    c_m.simply_write(error_massage, self.text_eng_folder_path, error_eng_p_text_f_name)

                # getting translate popup as html page:
                self.driver.get("chrome-extension://aapbdbdomjkkjkaonfhkkikfgjllcleb/popup.html")
                print "SLEEPING %d seconds, after EXTENSION GET" % ext_get_sleep
                time.sleep(ext_get_sleep)

                print "POPULATING CLIPBOARD with text from file...."
                pyperclip.copy(page_text)
                print "Sleeping after copying to clipboard for %d s" % text_copy_to_clip_sleep
                time.sleep(text_copy_to_clip_sleep)

                # Finding text input element
                text_input_el = self.driver.find_element_by_id('text-input')
                #sending command via selenium Keys
                text_input_el.send_keys(Keys.CONTROL, 'v')
                print "Sleeping after pasting for %d" % text_paste_sleep
                time.sleep(text_paste_sleep)
                #submit to translate
                print "Pressing return"
                text_input_el.send_keys(Keys.RETURN)
                
                text_output_tries = 0 # initial number of small while loop tries

                # skips find output element and take text when trying for the first time
                if track_while_loops == 0 and eng_p_text_f_name == "eng_page_0_text.txt":
                    track_while_loops += 1
                    continue

                # small while cycle waiting for input to be processed
                while text_output_tries < 5 and not text_output:
                    text_output_tries +=1
                    print "sleeping after submition for %d s. Waiting for text to be translated" % text_translate_sleep
                    time.sleep(text_translate_sleep)

                #find output element, take text
                    try:
                        text_output_el = self.driver.find_element_by_xpath('//*[@id="translation"]/div[6]')
                        text_output = text_output_el.text
                        print "TRANS_TEST_1: input sample\n%r" % page_text
                        print "TRANS_TEST_1: text_sample_ouput\n%r" % text_output
                    except:
                        print "Trying for %d time - THE TRANSLATED SAMPLE WAS NOT GENERATED" % text_output_tries

            print "WRITING TRANSLATED OUTPUT TO FILE: ", eng_p_text_f_name
            c_m.simply_write(text_output, self.text_eng_folder_path, eng_p_text_f_name)
            data_set.append(eng_p_text_f_name)
            new_page_list.append(data_set)
            track_while_loops += 1 # incrementing tries
        print "DONE TRANSLATING SITE %s " % self.domain
        print "UPDATING PAGE LIST WITH ENG TEXT FILE NAMES"
        c_m.l_of_l_write(new_page_list, self.page_list_path)
        self.driver.quit() # working chrome window closing





class Link_Module_Driver(object):

    def __init__(self):

        self.pc_specific_part_path = os.path.dirname(os.path.realpath(__file__)) + "\\"
        self.static_part_path = "site_data\\0_1_input_urls.txt"

        self.link_input_path =  self.pc_specific_part_path + self.static_part_path


    def drive_input_links(self):
        # driving links
        input_links_nested_list =[[],[]]
        
        while len(input_links_nested_list) > 0:
            # retieving input_link_list
            input_links_nested_list = c_m.l_of_l_read(self.link_input_path)

            url = input_links_nested_list[0][1] #input link in nested list type data table.
                                                # will raise out of range error if empty input link file is provided.
            print "drive_input_links: INPUT URL:", url

            # driving modules
            site_selector = Common_Paths(url) # System module

            # Comment out if you do not need site link management
            site_link_manager_sys = Site_Link_Manager(url)
            # checking if link is duplicate
            is_duplicate = site_link_manager_sys.check_if_duplicate()
            if is_duplicate:
                print "drive_input_links: GOING TO THE NEXT SITE LINK"
                input_links_nested_list.pop(0)
                c_m.l_of_l_write(input_links_nested_list, self.link_input_path)
                continue
            print "drive_input_links: DUBLI CHECK DONE"
            #/

            # Comment out if you do not need html retrieval
            html_maker = HTML_File_Maker(url)
            site_bs_object_dict = html_maker.mk_htmls() # output html bs_object dict for next module
            print "drive_input_links: HTML FILES DONE BS OBJECTS READY"
            #/

            # Comment out if you do not need text extraction
            txt_maker = Text_Extractor(url)
            txt_maker.mk_text_files(site_bs_object_dict)
            print "drive_input_links: TEXT FILE MAKER DONE"
            #/

            # Comment out if you do not need english translation
            translator = Translator(url)
            translator.mk_eng_txt_files()
            print "drive_input_links: TRANSLATOR DONE"
            print "drive_input_links: ADDING TO VERI GOOD FILE"
            #/

            # Comment out if you do not need site link management
            site_link_manager_sys.add_to_veri_good()
            print "drive_input_links: LINK DONE, POPING..."
            input_links_nested_list.pop(0)
            print "drive_input_links: UPDATING INPUT LINK DATA"
            c_m.l_of_l_write(input_links_nested_list, self.link_input_path)
            #/

link_driver = Link_Module_Driver()
link_driver.drive_input_links()



