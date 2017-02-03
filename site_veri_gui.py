#-*- coding: utf-8 -*-

""" ABOUT """
#   This script is still in prototyping stage new functionality is being added on the fly.
#   "site_veri_gui" is meant to represent prepocessed site page text data in as simplsistic way to achive much better speeds compared to site page loading directly from source.
#    Main purpose of the "site_veri_gui" is text based site verification with a help highlighting functionality.


# FILESYSTEM AND RELATIONS:
#   "site_veri_gui" usually works together with "site_retriever" and uses the same main path directory "site_data"
#    "site_retriever" retrives site html and extracts unique visible text in per page and makes equivalent english translation txt files


#FUNCTIONALITY:
#   Takes text files as inputs and represents them in Notebook tab fasion, up to 20 tabs.
#   "VERI_GOOD" and "VERI_BAD" buttons (top left gui corner) load next site and places site entry data to veri_bad or veri_good txt file,
# eqvuivalent source file "ready_for_veri" entry is deleted from file
#   Original and english text representation is supported. Accesed through "original" or "english" buttons(top right gui corner).
#   Hyperlink to original site page is available at the top of text representation folder

# Highlighting:
#   GUI supports highlighting of EXACT keywords (case insensitivity and alternate separator functionality in near future)
# of text in text reprenetation field central part of gui.
#   Keywords are highlighted when typed to keyword input field marked yellow (gui right side) and "enter" pressed
#   Entered keywords list is saved in local text file in site_data directory.
#   Sum keyword hit count per page is represented in each tab header.

# SCRIPT ARCHITECTURE OVERVIEW
#   Script is implemented in one main class
#   GUI interface, initial site loading with all functionality is initiated in __init__
#   The methods are sorted according to script processing order, sub methods are placed above main methods.
#   Procesing order is represented with "print" statements identifing source method.
#   The processing sequence is alternating from processing different functional methods in the same cycle
# to moving to different functional method only after cycle is finished thourghout the script.



""" NECESSARY IMPORTS """
from Tkinter import *
import ttk
import io
import webbrowser
import common_methods as c_m
from copy import copy


""" PRE GUI DATA PREPARATION """






""" GUI CLASS """

class Veri_GUI(object):
    def __init__(self, root):
        print "__init__: BUILDING GUI"
        self.root = root
        root.title("VERI")
        self.cont = ttk.Frame(root, relief='sunken')

        # __init__: unusual tab positioning is achieved through ttk Style functionality
        self.change_noteb = ttk.Style()
        self.change_tab = ttk.Style()
        self.change_noteb.configure('TNotebook', tabposition='wn')
        self.change_tab.configure('TNotebook.Tab', borderwidth=5)
        #/
        # __init__: ttk widget instantiation
        self.noteb = ttk.Notebook(self.cont)
        self.button_frame = ttk.Frame(self.cont, relief='sunken')
        self.good_button = Button(self.button_frame, text='VERI_GOOD', width=20, height=5, bg='green', command=self.veri_good_b)
        self.bad_button = Button(self.button_frame, text='VERI_BAD', width=20, height=5, bg='red', command=self.veri_bad_b)
        self.h_light_frame = Frame(self.cont, relief='raised', background='yellow', borderwidth='3')
        self.lang_b_frame = Frame(self.cont, relief='raised')
        self.eng_b = Button(self.lang_b_frame, text='english', relief='raised', command=self.load_eng_text)
        self.original_lang_b = Button(self.lang_b_frame, text='original', relief='raised', command=self.load_original_text)
        
        # __init__: text box for highlight input
        self.input_header = ttk.Label(self.h_light_frame, text='TEST_key', background='yellow')
        self.input_as_text = Text(self.h_light_frame, width=20, height=39, borderwidth=3, relief='sunken')
        #/

        # __init__: gridding STATIC gui components
        self.cont.grid(column=0, row=0, sticky=(N,W,S,E))
        self.button_frame.grid(column=0, row=0, sticky=(N,W,S,E))
        self.noteb.grid(column=0, row=1, sticky=(N,W,S,E))
        self.good_button.grid(column=0, row=0, sticky=(N,W))
        self.bad_button.grid(column=1, row=0, sticky=(N,W))
        self.lang_b_frame.grid(column=1, row=0, sticky=E)
        self.h_light_frame.grid(column=1, row=1, padx=3)
        self.eng_b.grid(column=0, row=0, sticky=(E), padx=5, pady=3)
        self.original_lang_b.grid(column=0, row=1, sticky=(E), padx=5, pady=3)
        self.input_header.grid(column=0, row=0, sticky=(N,S))
        self.input_as_text.grid(column=0, row=1, sticky=(N,S))
        #/
        # __init__: instances of DYNAMIC notebook tabs
        # max no. == 20 of tabs instances
        self.t_tab0 = Text(self.noteb, width=100, height=40, font=("Arial", "10"))                                                                                                                    
        self.t_tab1 = Text(self.noteb)
        self.t_tab2 = Text(self.noteb)
        self.t_tab3 = Text(self.noteb)
        self.t_tab4 = Text(self.noteb)
        self.t_tab5 = Text(self.noteb)
        self.t_tab6 = Text(self.noteb)
        self.t_tab7 = Text(self.noteb)
        self.t_tab8 = Text(self.noteb)
        self.t_tab9 = Text(self.noteb)
        self.t_tab10 = Text(self.noteb)
        self.t_tab11 = Text(self.noteb)
        self.t_tab12 = Text(self.noteb)
        self.t_tab13 = Text(self.noteb)
        self.t_tab14 = Text(self.noteb)
        self.t_tab15 = Text(self.noteb)
        self.t_tab16 = Text(self.noteb)
        self.t_tab17 = Text(self.noteb)
        self.t_tab18 = Text(self.noteb)
        self.t_tab19 = Text(self.noteb)

        # __init__: purpose: adding to list for ease of acces
        self.t_tab_list = [self.t_tab0, self.t_tab1, self.t_tab2, self.t_tab3, self.t_tab4, self.t_tab5,
                            self.t_tab6, self.t_tab7, self.t_tab8, self.t_tab9, self.t_tab10, self.t_tab11,
                            self.t_tab12, self.t_tab13, self.t_tab14, self.t_tab15, self.t_tab16, self.t_tab17,
                            self.t_tab18, self.t_tab19]
        #/
        print "__init__: GUI INSTANCE READY"

        print "__init__: INITIALIZING PATHS AND FILE NAMES"
        self.static_part_path = "site_selector\\site_data\\" 
        self.pc_specific_part_path = os.path.dirname(os.path.realpath(__file__)) + "\\"
        self.main_path = self.pc_specific_part_path + self.static_part_path
    
        self.very_ready_f_name = '1_ready_for_veri.txt'
        self.very_ready_f_path = self.main_path + self.very_ready_f_name
        self.very_good_f_name = '2_1_good_veri.txt'
        self.very_good_f_path = self.main_path + self.very_good_f_name
        self.very_bad_f_name = '2_2_bad_veri.txt'
        self.very_bad_f_path = self.main_path + self.very_bad_f_name
        self.all_hlights_f_name = '3_1_all_highlights.txt'
        self.all_hlights_f_path = self.main_path + self.all_hlights_f_name

        print "__init__: ASSIGNING INITIAL VALUES FOR GLOBALY USED DYNAMIC VARIABLES"
        self.eng_text = False # initial loaded original text
        self.eng_b_second_try = False # button second click controler
        self.original_b_second_try = True # button second click controler, True - initial language original
        self.active_link_url_no_domain_list = [] # for page link without domain later use after adding sum key hit per page in tab header

        print "__init__: INITIAL TABS LOADING AND HIGHLIGHTING"
        #__init__: READING SITE LINK (very_ready) FILE"
        self.veri_ready_list = c_m.l_of_l_read(self.very_ready_f_path)

        #__init__: LOADING INITIAL TAB DATA SET ACCORDING TO FIRST SITE ENTRY IN veri_ready"
        self.init_site_data = self.veri_ready_list[0]
        self.init_tabs_data_set_list = self.mk_tabs_data_set(self.init_site_data)

        print "__init__: NUMBER OF PAGES TO BE LOADED %d" % len(self.init_tabs_data_set_list)
        self.laod_tabs(self.init_tabs_data_set_list, self.eng_text)

        print "__init__: INITIATING HIGHLIGHTS FUCTIONALITY"

        #__init__: READING HIGHLIGHT KEYWORDS FILE"
        self.init_h_key_list = c_m.l_of_l_read(self.all_hlights_f_path) # returns a list of lists

        self.key_position_lib = {} # initial key position lib for faster highlighting removal

        # handling empty h key list
        if len(self.init_h_key_list) > 0:
            #__init__: KEYWORDS PRESENT IN FILE INITIALIZING HIGHLIGHTING FUNCTIONALITY
            self.test_hi_key_list = self.init_h_key_list[0] # index zero currenlty is test highlights, can be added other, always_positive, always_negative
            #__init__: SHOWING KEYS FROM FILE IN KEYS INPUT FIELD
            self.test_hi_key_list = self.write_key_input_field(self.test_hi_key_list) # adjusting for empty items in the text file
            #__init__: HIGHLIGHTING KEYS FROM FILE IN TAB\PAGE TEXT
            self.highlight_keys_in_site(self.test_hi_key_list)

        else:            
            #__init__: THE INITIAL HIGHLIGHT KEY LIST IS EMPTY
            self.init_h_key_list = [[],[],[]] # assigning initial apropriate format empty list value
            self.test_hi_key_list = self.init_h_key_list[0] # test key list initial empty list value

        # "Key input field Return key binding to highlighting controler method"
        self.input_as_text.bind('<Return>', self.react_to_highlighting_request)

    """ METHODS """
    """ TABS AND DATA HANDLING METHODS """

    # CALLED FROM METHOD: mk_tabs_data_set
    def mk_adjusted_page_list(self, page_list):
        
        """ page_list_20:
            - homepage first others sorted according to page length in symbols,
            - number of list items limited to 20 as is with tabs
            """
        print "IN: mk_adjusted_page_list"
        adjusted_page_list = [] # for making new from old page_list
        page_list_copy = copy(page_list)

        for ind in range(len(page_list_copy)):
            #mk_adjusted_page_list: placing original text length metric to position 0 in data list for list od list sorting sorting
            page_list_copy[ind].insert(0, int(page_list_copy[ind][3]))
            page_list_copy[ind].pop(4)

            if page_list_copy[ind][1] > 10: #remove pages with text length up to 10 symbols
                print "mk_adjusted_page_list: PAGE TEXT LENGTH IS MORE THAN 10 SYMBOLS, ADJUSTING PAGE DATA ENTRY %d" % ind
                adjusted_page_list.append(page_list_copy[ind])
        base_url_entry = copy(adjusted_page_list[0])
        adjusted_page_list.pop(0)
        sorted_adjusted = sorted(adjusted_page_list, reverse=True)    
        #mk_adjusted_page_list: base url to first tab position
        sorted_adjusted.insert(0, base_url_entry)

        #mk_adjusted_page_list: handling cases when site has less than 20 pages
        if len(sorted_adjusted) > 20:
            print "mk_adjusted_page_list: SITE HAS MORE THAN 20 PAGES"
            page_list_up_to_20 = sorted_adjusted[0:20]
        else:
            print "mk_adjusted_page_list: SITE HAS LESS THA 20 PAGES"
            page_list_up_to_20 = sorted_adjusted

        return page_list_up_to_20

    # CALLED FROM METHOD: __init__
    def mk_tabs_data_set(self, site_data_entry):

        """According to site data from 1_ready_for_veri file
        retrieves page data from page_list file,
        places homepage as first tab,
        sorts other according to page text symbol count from biggest down"""

        print "mk_tabs_data_set: RETRIEVING AND REARANGING PAGE LIST ENTRY DATA"
        base_url = site_data_entry[3]

        page_list_f_name = 'page_list.txt'
        url_domain = c_m.strip_to_domain(base_url) # domain acts as key in filesystem composed of folders named as domains
        print "FOR DOMAIN: ", url_domain
        domain_folder = url_domain + "\\"
        page_list_path = self.main_path + domain_folder + page_list_f_name
        page_list = c_m.l_of_l_read(page_list_path)

        print "mk_tabs_data_set: ADJUSTING PAGE LIST"
        adjusted_page_list = self.mk_adjusted_page_list(page_list) # sorting list according to unique page text length
        return adjusted_page_list

    # CALLED FROM CLASS METHOD:
    # - __init__
    # - veri_good_b
    # - veri_bad_b
    # - load_eng_text
    # - load_original_text
    
    def laod_tabs(self, adjusted_page_list, eng_text):

        """ From or according to adjusted page list data
            sets needed variable values,
            retrieves original or english page texts,
            loads tabs with apropriate data in place"""

        print "IN: laod_tabs"
        for ind in range(len(adjusted_page_list)):

            #laod_tabs: setting variables
            base_url = adjusted_page_list[0][1]
            url_domain = c_m.strip_to_domain(base_url)
            domain_folder = url_domain + "\\"
            page_link_url = adjusted_page_list[ind][1]
            active_link_url_no_domain = page_link_url.replace(base_url,'...')
            self.active_link_url_no_domain_list.append(active_link_url_no_domain)
            active_tab = self.t_tab_list[ind]

            #laod_tabs: method supports original and english page text loading set as input for method
            if eng_text:
                folder_type = "text_eng\\"
                page_text_f_name = adjusted_page_list[ind][4]
            else:
                folder_type = "text\\"
                page_text_f_name = adjusted_page_list[ind][3]
            page_text_f_path = self.main_path + domain_folder + folder_type + page_text_f_name
            #laod_tabs: LOADING TEXT FROM FILE
           
            self.noteb.add(active_tab, text='%s' % (active_link_url_no_domain)) #laod_tabs: tab header text

            #laod_tabs: INSERTING HYPERLINK TO TAB TEXT WIDGET
            hyper_page_link = page_link_url + '\n\n' #laod_tabs: empty line between hyperlink and text
            active_tab.insert(END, hyper_page_link)

            #laod_tabs: RETRIEVING PAGE TEXT FROM FILE
            page_text = c_m.simply_read(page_text_f_path)
            #laod_tabs: INSERTING PAGE TEXT TO TAB TEXT WIDGET
            active_tab.insert(END, page_text) #laod_tabs: Adding retrieved text to notebook text window

            #laod_tabs: CONFIGURING INSERTED LINK TO SHOW UP AS PROPER HYPERLINK
            active_tab.tag_add('hyper', '1.0', '1.%d' % len(page_link_url))
            active_tab.tag_config('hyper', foreground='blue')
            active_tab.tag_bind('hyper', "<Enter>", lambda event, arg=ind: self.mouse_on(event, arg))
            active_tab.tag_bind('hyper', "<Leave>", lambda event, arg=ind: self.mouse_of(event, arg))
            active_tab.tag_bind('hyper', "<Button-1>", lambda event, arg=page_link_url: self.hyper(event, arg))

            #TEST FUNCTIONALITY: if keyword present make the tab visible in GUI
            page_key_word = ["Om-oss", "om-oss", "om oss", "OM-OSS"]
            if (page_key_word[0] or page_key_word[1] or page_key_word[2] or page_key_word[3]) in page_link_url:
                self.noteb.select(active_tab)

    def delete_tabs(self, old_tabs_data_set):
        """ Deletes tabs according to tabs  for repopulation """
        print "IN: delete_tabs. NO. OF TABS TO BE DELETED - ",  len(old_tabs_data_set)
        for ind in range(len(old_tabs_data_set)):
            self.t_tab_list[ind].delete('1.0', END)
            self.noteb.forget(self.t_tab_list[ind])


    """ TEXT FIELD HYPERLINK HANDLING METHODS """

    # CALLED FROM METHOD: laod_tabs 
    def mouse_on(self, event, ind):
        """ Changes cursor pointer to hand2 binded action"""
        self.t_tab_list[ind].config(cursor="hand2")

    # CALLED FROM METHOD: laod_tabs
    def mouse_of(self, event, ind):
        """ Changes cursor pointer back to original"""
        self.t_tab_list[ind].config(cursor="")

    # CALLED FROM METHOD: laod_tabs
    def hyper(self, event, link_url):
        """ Opens link in a deafault browser on mouse click """
        print "IN: hyper. OPENING TEXT FIELD HYPERLINK IN A BROWSER"
        webbrowser.open_new(link_url)



    """ VERIFICATION FUNCTIONALITY METHODS """

    # CALLED FROM METHOD: __init__: self.good_button         
    def veri_good_b(self):
        """ Resets second try states,
        repopulates tabs with next site data,
        removes current site link from veri_ready and
        adds to veri_good file
        highlights newly added text"""

        veri_good_site_status = "VERI_GOOD"

        print "IN: veri_good_b. VERI GOOD BUTTON CLICKED"
        print "veri_good_b: REPOPULATING TABS WITH NEXT SITE DATA"
        
        #veri_good_b: RESETTING SECOND TRY MARKERS"
        self.eng_b_second_try = False # clearing english button tries
        self.original_b_second_try = False # clearing original button tries


        old_tab_data_set = self.init_tabs_data_set_list
        #veri_good_b: DELETING OLD TABS
        self.delete_tabs(old_tab_data_set)
        self.veri_ready_list[0][1] = veri_good_site_status
        current_site_data_entry = self.veri_ready_list[0]

        #veri_good_b: ADDING CLICKED AS GOOD SITE DATA ENTRY TO VERI GOOD FILE
        c_m.txt_file_append(current_site_data_entry, self.very_good_f_path)

        #veri_good_b: GOING TO THE NEXT SITE DATA ENTRY IN VERY READI LIST
        self.veri_ready_list.pop(0)
        next_site_data_entry = self.veri_ready_list[0]

        #veri_good_b: LOADING NEXT SITE TABS
        #veri_good_b: using global init_tabs_data_set_list parameter to delete tabs after button click
        self.init_tabs_data_set_list = self.mk_tabs_data_set(next_site_data_entry)
        self.laod_tabs(self.init_tabs_data_set_list, self.eng_text)

        print "veri_good_b: HIGHLIGHTING NEW SITE KEYWORDS"
        self.highlight_keys_in_site(self.test_hi_key_list)

        #veri_good_b: UPDATING VERI READY FILE WITH FIRST DELETED ENTRY VERI READY LIST
        c_m.l_of_l_write(self.veri_ready_list, self.very_ready_f_path)

    # CALLED FROM METHOD: __init__: self.bad_button
    def veri_bad_b(self):
        """ Resets second try states,
        repopulates tabs with next site data,
        removes current site link from veri_ready and
        adds to veri_bad file
        highlights newly added text"""

        print "IN: veri_bad_b. VERI GOOD BUTTON CLICKED"
        print "veri_bad_b: REPOPULATING TABS WITH NEXT SITE DATA"
        
        veri_bad_site_status = "VERI_BAD"

        #veri_bad_b: RESETTING SECOND TRY MARKERS
        self.eng_b_second_try = False # clearing english button tries
        self.original_b_second_try = False # clearing original button tries

        #veri_bad_b: DELETING OLD TABS
        old_tab_data_set = self.init_tabs_data_set_list
        self.delete_tabs(old_tab_data_set)

        #veri_bad_b: TRANSFERING MARKED AS BAD SITE DATA ENTRY TO VERI GOOD FILE
        self.veri_ready_list[0][1] = veri_bad_site_status
        current_site_data_entry = self.veri_ready_list[0]
        c_m.txt_file_append(current_site_data_entry, self.very_bad_f_path)

        #veri_bad_b: GOING TO THE NEXT SITE DATA ENTRY IN VERY READI LIST
        self.veri_ready_list.pop(0) 
        next_site_data_entry = self.veri_ready_list[0]

        #veri_bad_b: LOADING NEXT SITE TABS
        self.init_tabs_data_set_list = self.mk_tabs_data_set(next_site_data_entry)
        self.laod_tabs(self.init_tabs_data_set_list, self.eng_text)

        print "veri_bad_b: HIGHLIGHTING NEW SITE KEYWORDS"
        self.highlight_keys_in_site(self.test_hi_key_list)

        #veri_bad_b: UPDATING VERI READY FILE
        c_m.l_of_l_write(self.veri_ready_list, self.very_ready_f_path)


    """ HIGHLIGHTING METHODS """

    # CALLED FROM METHOD: highlight_keys_in_site
    def mk_tab20_text_list(self):
        """ Reads text from tab text fields,
        returns as a nested list"""

        print "mk_tab20_text_list: POPULATING tabs20_text_list..."
        tabs20_text_list = []
        for active_tab in self.t_tab_list:
            tab_text = active_tab.get('1.0', END)
            tab_text_list = tab_text.split('\n')
            tabs20_text_list.append(tab_text_list)
        return tabs20_text_list


    # CALLED FROM METHOD: highlight_keys_in_site
    def find_highlight_position(self, hi_keyword, page_text_as_list):
        """ Page text list index means line, find method return starting symbol of the keyword in line"""

        print "IN: find_highlight_position: LOOKING FOR KEY POSITION IN PAGE TEXT"
        page_h_position_list = []

        for ind in range(len(page_text_as_list)):
            track_s_line = ind
            track_s_symbol = page_text_as_list[ind].find(hi_keyword)
            if track_s_symbol > (-1):     
                h_position_entry = [track_s_line, track_s_symbol]
                page_h_position_list.append(h_position_entry)

        return page_h_position_list

    def count_keys_hit_per_page(self):
        """ From key_position_lib counts sum key hit count per page """

        print "IN: count_keys_hit_per_page: COUNTING KEY HITS AND MAKING VISIBLE IN TAB HEADER"

        for tab_ind in range(len(self.init_tabs_data_set_list)):
            active_link_url_no_domain = self.active_link_url_no_domain_list[tab_ind]
            sum_keys_hit_count_per_page = 0

            for key in self.key_position_lib:
                sum_keys_hit_count_per_page += len(self.key_position_lib[key][tab_ind])

            active_tab = self.t_tab_list[tab_ind]
            current_tab_id = self.noteb.index(active_tab)
            self.noteb.tab(current_tab_id, text="(%d)%s" % (sum_keys_hit_count_per_page, active_link_url_no_domain))


    # CALLED FROM METHODs:
    # - __init__
    # - veri_good_b
    # - react_to_highlighting_request
    # - load_eng_text
    # - load_original_text
    # - veri_bad_b

    def highlight_keys_in_site(self, key_list):
        """ Adds tag with cnaged background color
        according to found keyword position in text field"""

        print "IN: highlight_keys_in_site. HIGHLIGHTING KEYS IN TEXT FIELD"

        #filter empty items
        real_keys = []
        for key in key_list:
            if len(key) > 0:
                real_keys.append(key)
        #/

        #empty nested list with 20 lists for key highlighting positions recording
        fixed_tab_grid = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        
        print "highlight_keys_in_site: GETTING TEXT FROM TABS, SPLITTING TO LIST, NESTING TABS TO ALL TABS TEXT LIST"
        tabs20_text_list = self.mk_tab20_text_list()

        print "highlight_keys_in_site: GOING THROUGH KEYS LOOKING FOR POSITIONS IN PAGE, IF PRESENT, ADDING HIGHLIGHTS"
        for key in real_keys:
            fixed_tab_grid_copy = copy(fixed_tab_grid)
            self.key_position_lib[key] = fixed_tab_grid_copy # assigning empty position tracking grid for h_key

            sum_key_hit_count = 0
            for tab_ind in range(len(self.init_tabs_data_set_list)):
                tab_text_list = tabs20_text_list[tab_ind]
                key_p_in_page = self.find_highlight_position(key, tab_text_list) 

                if len(key_p_in_page) > 0:
                    active_tab = self.t_tab_list[tab_ind]

                    #highlight_keys_in_site: highlighting key in tab text
                    for s_line_s_symbol in key_p_in_page:

                        #highlight_keys_in_site: unpacking key position values
                        s_line = s_line_s_symbol[0] + 1 # text widget counts line from the first line
                        s_symbol = s_line_s_symbol[1]
                        e_line = s_line
                        e_symbols = s_symbol + len(key)
                        str_s_line = str(s_line)
                        str_s_symbol = str(s_symbol)
                        str_e_line = str(e_line)
                        str_e_symbols = str(e_symbols)
                        #/
                        #highlight_keys_in_site: highlighting
                        active_tab.tag_add('highlight%s.%s' % (str_s_line, str_s_symbol), '%s.%s' % (str_s_line, str_s_symbol), '%s.%s' % (str_e_line, str_e_symbols))
                        active_tab.tag_config('highlight%s.%s' % (str_s_line, str_s_symbol), background='yellow')
                        #/

                    print "highlight_keys_in_site: SAVING POSITIONS OF HIGHLIGHTED KEYWORDS:", key_p_in_page
                    self.key_position_lib[key][tab_ind] = key_p_in_page # function: assigning key position to specific page

                    print "highlight_keys_in_site: ADDING KEYS HIT COUNT PER PAGE TO THE TAB HEADER"                    
                    self.count_keys_hit_per_page()

    # CALLED FROM METHOD: react_to_highlighting_request    
    def remove_highlight(self, deleted_key):
        """ Removes highlights for deleted key"""

        print "IN: remove_highlight. DELETED KEY - %r" % deleted_key

        for tab_ind in range(len(self.init_tabs_data_set_list)):
            tab_key_p_list = self.key_position_lib[deleted_key][tab_ind]    # format: nested list with pages 
                                                                            # and keyword positions in the page
            if len(tab_key_p_list) > 0: #remove_highlight: meaning: if keys are present in the page
                active_tab = self.t_tab_list[tab_ind] #remove_highlight: activating tab

                for s_line_s_symbol in tab_key_p_list:
                    #remove_highlight: unpacking position values
                    s_line = s_line_s_symbol[0] + 1
                    s_symbol = s_line_s_symbol[1]
                    e_line = s_line
                    e_symbol = s_symbol + len(deleted_key)

                    str_s_line = str(s_line)
                    str_s_symbol = str(s_symbol)
                    str_e_line = str(e_line)
                    str_e_symbol = str(e_symbol)
                    #/

                    #remove_highlight: removing key related tags
                    active_tab.tag_remove('highlight%s.%s' % (str_s_line, str_s_symbol), 
                                            "%s.%s" % (str_s_line, str_s_symbol), "%s.%s" % (str_e_line, str_e_symbol))

        del self.key_position_lib[deleted_key] # deleting keyword position list
        print "remove_highlight: ADJUSTING KEY HIT COUNT ACCORDING TO NEW key_position_lib"                  
        self.count_keys_hit_per_page()

    # CALLED FROM METHOD: react_to_highlighting_request
    def read_key_input_field(self):
        """ Reads the field end makes a const sample figure out action made."""
        #read_key_input_field: format: keywords list separated by new lines, one new line character at the end
        print "IN: read_key_input_field: READING KEYWORDS FROM KEYWORD INPUT FIELD"
        test_input = self.input_as_text.get('1.0', END)
        print "test_input %r" % test_input
        u_test_input = unicode(test_input)
        if u_test_input.endswith("\n"):
            u_test_input = u_test_input[0:-1]
        #read_key_input_field: convert text to list
        test_key_input_list = u_test_input.split('\n')

        #read_key_input_field: failsafing input list
        no_empty = []
        is_empty = False
        for item in test_key_input_list:
            no_white_space = item.strip() #read_key_input_field: stripping white spaces characters
            if len(no_white_space) > 1:
                no_empty.append(no_white_space)
            else:
                is_empty = True # if found at least one empty item setting to rewriting mode
                print "read_key_input_field: EMPTY, WHITE SPACE, OR ONE SYMBOL KEY PRESENT IN THE KEYLIST"

        if is_empty: # rewriting mode
            self.write_key_input_field(no_empty, is_empty)

        return no_empty



    # CALLED FROM METHOD:
    # - __init__
    # - react_to_highlighting_request
    # - read_key_input_field
    def write_key_input_field(self, list_to_write, *arg):
        #write_key_input_field: failsafing input list
        no_empty = []
        for item in list_to_write:
            no_white_space = item.strip() # stripping white spaces characters
            if len(no_white_space) > 1:
                no_empty.append(no_white_space)
            else:
                arg = True # if found at least one empty item setting to rewriting mode
                print "write_key_input_field: EMPTY, WHITE SPACE, OR ONE SYMBOL KEY PRESENT IN THE KEYLIST"

        if arg: #write_key_input_field rewriting mode
            self.input_as_text.delete('1.0', END)
            as_text = unicode("\n".join(no_empty))
            #write_key_input_field updating global keylist and file keylist with corected version
            self.init_h_key_list[0] = no_empty
            c_m.l_of_l_write(self.init_h_key_list, self.all_hlights_f_path)
        else:
            as_text = unicode("\n".join(no_empty) + "\n")

        self.input_as_text.insert(END, as_text)
        return no_empty

    # CALLED FROM METHOD:  __init__ : self.input_as_text.bind
    def react_to_highlighting_request(self, event):

        test_input_key_list = self.read_key_input_field()

        print "IN: react_to_highlighting_request"
        print "react_to_highlighting_request: COMPARING INIT KEYWORD LIST WITH A LIST AFTER \"RETURN\" BINDED ACTION"

        if len(test_input_key_list) > len(self.test_hi_key_list):
            print "react_to_highlighting_request: NEW HIGHLIGHT KEYs ADDED TO HIGHLIGHT LIST"
            #react_to_highlighting_request: find added keywords and add to key list
            added_key_list = []
            for key in test_input_key_list:
                 #react_to_highlighting_request: filtering out empty keys and leaving which are not in previous list
                if key not in self.test_hi_key_list and len(key) > 0:
                    added_key = key

                    added_key_list.append(added_key) # highlight_keys_in_site tekes in keys as list

            print "react_to_highlighting_request: HIGHLIGHTING KEYS %r" % added_key_list
            self.highlight_keys_in_site(added_key_list)

            #react_to_highlighting_request: updating key list in local file
            self.init_h_key_list[0] = test_input_key_list
            c_m.l_of_l_write(self.init_h_key_list, self.all_hlights_f_path)
            self.test_hi_key_list = test_input_key_list

        elif len(test_input_key_list) == len(self.test_hi_key_list): # enter presed without adding anything
            print "react_to_highlighting_request: ENTER PRESSED WITHOUT ADDING ANY HIGHLIGHTS"            
            self.write_key_input_field(test_input_key_list, True) # rewrite True


        else: #react_to_highlighting_request: details: less keys are present in key input field than previous image of the field - self.test_hi_key_list
            print "react_to_highlighting_request: HIGHLIGHT KEYWORDs DELETED: ",

            #react_to_highlighting_request: need to know which highlight is removed.
            for h_key in self.test_hi_key_list:
                if h_key in test_input_key_list:
                    pass
                else:
                    deleted_key = h_key
                    print deleted_key
                    self.remove_highlight(deleted_key)
            #react_to_highlighting_request: rewriting keys to have corect format
            self.write_key_input_field(test_input_key_list, True)
            #react_to_highlighting_request: write new key list to txt file
            self.init_h_key_list[0] = test_input_key_list
            c_m.l_of_l_write(self.init_h_key_list, self.all_hlights_f_path)
            self.test_hi_key_list = test_input_key_list

    """ LANGUAGE HANDLING METHODS """

    def load_eng_text(self):
        """Repopulates tabs with english text"""

        print "load_eng_text: ENG TEXT BUTTON PUSHED"   
        self.original_b_second_try = False # clearing tries count for original text loading button
        self.eng_text = True
        if self.eng_b_second_try:
            print "load_eng_text: COMMAND IS ALREADY EXECUTED, NO NEED TO DO IT AGAIN"
        else:
            print "load_eng_text: BUTTON CLICKED FOR THE FIRST TIME"

            print "load_eng_text: REPOPULATING WITH ENGLISH TABS"
            self.delete_tabs(self.init_tabs_data_set_list)
            self.laod_tabs(self.init_tabs_data_set_list, self.eng_text)
            self.highlight_keys_in_site(self.test_hi_key_list)

            self.eng_b_second_try = True # next time button pushed command will not be executed


    def load_original_text(self):
        """Repopulates tabs with original text"""
        print "eng_text BUTTON PUSHED"
        self.eng_b_second_try = False # clearing tries count for english text loading button
        self.eng_text = False
        if self.original_b_second_try:
            print "load_original_text: COMMAND IS ALREADY EXECUTED, NO NEED TO DO IT AGAIN"

        else:
            print "load_original_text: BUTTON CLICKED FOR THE FIRST TIME"

            print "load_original_text: REPOPULATING WITH ORIGINAL TABS"
            self.delete_tabs(self.init_tabs_data_set_list)
            self.laod_tabs(self.init_tabs_data_set_list, self.eng_text)
            self.highlight_keys_in_site(self.test_hi_key_list)

            self.original_b_second_try = True #load_original_text: next time button pushed command will not be executed
    

root = Tk()
gui_object = Veri_GUI(root)

root.mainloop()


