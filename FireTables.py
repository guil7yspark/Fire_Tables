#!/usr/bin/env python3
from tkinter import *
import iptc
import re
import os
import Save_Helpers
from sys import stdout

top_frame=None
bottom_frame=None

def main():
    #Main GUI Window
    root = Tk()
    root.title("Fire Tables")
    root.configure(bg="#212121")
    root.minsize(1160, 150)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(2, weight=1)

    global top_frame
    top_frame = LabelFrame(root)
    top_frame.grid(row=0, column=0, sticky="nsew")
    top_frame.configure(bg="#212121")
    top_frame.columnconfigure(0, weight=1)
    top_frame.columnconfigure(1, weight=1)
    top_frame.columnconfigure(2, weight=1)
    top_frame.columnconfigure(3, weight=1)
    top_frame.columnconfigure(4, weight=1)
    top_frame.columnconfigure(5, weight=1)
    top_frame.columnconfigure(6, weight=1)
    top_frame.columnconfigure(7, weight=1)
    top_frame.rowconfigure(2, weight=1)
    rule_header = Label(top_frame, text='  [Rule No.]  ', font="bold", bg="#353535", fg="#80FF00")
    rule_header.grid(row=0, column=0)
    input_output_forward = Label(top_frame, text='  [Input, Ouput, or Forward]  ', font="bold", bg="#353535", fg="#80FF00")
    input_output_forward.grid(row=0, column=1)
    #Source IP column header and entry box
    source_ip = Label(top_frame, text='  [Source IP]  ', font="bold", bg="#353535", fg="#80FF00")
    source_ip.grid(row=0, column=2)
    #Source port column header and entry box
    source_port = Label(top_frame, text='  [Source Port]  ', font="bold", bg="#353535", fg="#80FF00")
    source_port.grid(row=0, column=3)
    #Destination IP column header and entry box
    destination_ip = Label(top_frame, text='  [Destination IP]  ', font="bold", bg="#353535", fg="#80FF00")
    destination_ip.grid(row=0, column=4)
    #Destination port column header and entry box
    destination_port = Label(top_frame, text='  [Destination Port]  ', font="bold", bg="#353535", fg="#80FF00")
    destination_port.grid(row=0, column=5)
    #Protocol column header and drop down box
    protocol = Label(top_frame, text='  [Protocol]  ', font="bold", bg="#353535", fg="#80FF00")
    protocol.grid(row=0, column=6)
    #Accept or Drop column header and drop down box
    accept_or_drop_label = Label(top_frame, text='  [Accept or Drop]  ', font="bold", bg="#353535", fg="#80FF00")
    accept_or_drop_label.grid(row=0, column=7)
    #Bottom frame containing the "Add Rule", "Remove Rule", and "Save" buttons
    global bottom_frame
    bottom_frame = LabelFrame(root, bg="#353535")
    bottom_frame.grid(row=1, column=0, sticky='se', padx=20, pady=20)

    global bottom_center_frame
    bottom_center_frame = LabelFrame(root, bg="#353535")
    bottom_center_frame.grid(row=1, column=0, sticky='s', padx=20, pady=20)
    #Remove rule button
    remove_rule_button = Button(bottom_center_frame, text='Remove Rule', font="bold", bg="#353535", fg="#80FF00")
    remove_rule_button.grid(row=0, column=1)
    remove_rule_button.bind("<Button-1>", Remove_Rules)   
    # Remove Rule Entry Box
    global remove_rule_entry_box
    remove_rule_button.grid(row=0, column=1)
    remove_rule_entry_box = Entry(bottom_center_frame, width=12, bg="#353535", fg="#80FF00")
    remove_rule_entry_box.grid(row=0, column=2, ipady=5)    
    #Save button
    save_button = Button(bottom_frame, text='Save', font="bold", bg="#353535", fg="#80FF00")
    save_button.grid(row=0, column=2)
    save_button.bind("<Button-1>", Save_Rules)
    #Show Rules Button
    show_current_rules = Button(bottom_frame, text='View Current Rules', font="bold", bg="#353535", fg="#80FF00")
    show_current_rules.grid(row=0, column=0)
    show_current_rules.bind("<Button-1>", Show_Rules)    
    #Bottom left frame for "Delete All" button
    global bottom_left_frame
    bottom_left_frame = LabelFrame(root, bg="#353535") 
    bottom_left_frame.grid(row=1, column=0, sticky='sw', padx=20, pady=20)
    # Delete All Rules button
    delete_all_rules = Button(bottom_left_frame, text='Delete All', font="bold", bg="#353535", fg="#80FF00")
    delete_all_rules.grid(row=0, column=0)
    delete_all_rules.bind("<Button-1>", Remove_All_Rules)

    app = App()
    root.mainloop()

# Show status of IPTables Rules
def Show_Rules(event):
    #os.system('x-terminal-emulator')
    # Clear terminal
    os.system('clear')
    # Display iptables rules
    os.system('sudo iptables-legacy -L')

# Delete only the rules inputed
def Remove_Rules(event):
    #Create a dictionary and retreive input from remove rule entry box
    rules_to_remove = {}
    index_of_rule = ""
    index_of_rule = remove_rule_entry_box.get()
    #print(index)
    # Create an index from input
    if "-" in index_of_rule:
        first_num = int(index_of_rule[0]) - 1
        second_num = int(index_of_rule[2:])
        index_range = str(first_num) + ":" + str(second_num)
        #print(index_range[0:3])
    else:
        first_num = (int(index_of_rule) -1)
        second_num = first_num + 1
    # Get values of specified rule(s)
    for key in table_of_rules[first_num:second_num]: 
        rules_to_remove = Save_Helpers.get_current_values(key)
        #print(rules_to_remove)
        
        chain = ''
        rule = ''
        match = ''
        target = '' 
        #print(the_rule)
        regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$'''
        # Create rule(s) to be removed from rules_to_remove dictionary
        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), (rules_to_remove['input_options']))
        rule = iptc.Rule()
        #rule.in_interface = "eth+"   
        # Retrieve IPs and error check entries
        if(re.search(regex, str(rules_to_remove['source_ip']))):
            rule.src = rules_to_remove['source_ip']
        #else:
            #print("FireTables: Rule Source IP set to anywhere")
        if(re.search(regex,str(rules_to_remove['destination_ip']))):    
            rule.dst = rules_to_remove['destination_ip']
        #else:
            #print("FireTables: Rule Destination IP set to anywhere")
        # Retrieve Accept or Drop options
        target = iptc.Target(rule, rules_to_remove['accept_or_drop_options'])    
        rule.target = target
        # Retrieve Protocol
        rule.protocol = rules_to_remove['protocol_options']   
        match = iptc.Match(rule, rules_to_remove['protocol_options'])
        # Retrieve Ports and error check entries
        if rules_to_remove['protocol_options'] != 'icmp':
            if rules_to_remove['source_port'] != "":
                if int(rules_to_remove['source_port']) in range(65535):
                    match.sport = rules_to_remove['source_port']
            #else:
                #print("FireTables: Rule Source Port set to anywhere")
    
            if rules_to_remove['destination_port'] != "":
                if int(rules_to_remove['destination_port']) in range(65535):
                    match.dport = rules_to_remove['destination_port']
            #else:
                #print("FireTables: Rule Destination Port set to anywhere")
        rule.add_match(match)
        # Delete rule(s) from iptables
        chain.delete_rule(rule)
    # Clear terminal
    os.system('clear')
    # Display iptables rules
    os.system('sudo iptables-legacy -L')
    
# Delete All Button Function!
def Remove_All_Rules(event):
    # Flush iptables
    table = iptc.Table(iptc.Table.FILTER)
    table.flush()
    # Clear terminal
    os.system('clear')
    # Display iptables rules
    os.system('sudo iptables-legacy -L')    
    #print(table_of_rules)

rule_counter=0
table_of_rules = []
row_count = 0
class App(object):
    #Function to create a new rule row
    def new_row(self):
        global rule_counter
        global table_of_rules
        global row_count
        rule_counter += 1 
        new_rule = Label(top_frame, text=rule_counter, font="bold", bg="#212121", fg="#80FF00")
        new_rule.grid(column=0, ipady=10)
        
        global input_output_forward_options
        input_output_forward_options = StringVar()
        input_output_forward_options.set("INPUT")
        global input_output_forward_button
        input_output_forward_button = OptionMenu(top_frame, input_output_forward_options, "INPUT", "OUTPUT", "FORWARD")
        input_output_forward_button.config(bg="#353535", fg="#80FF00", width=9)
        input_output_forward_button.grid(column=1)

        global source_ip_entry_box 
        source_ip_entry_box = Entry(top_frame, width=14)
        source_ip_entry_box.config(bg="#353535", fg="#80FF00")
        source_ip_entry_box.grid(column=2)

        global source_port_entry_box 
        source_port_entry_box = Entry(top_frame, width=7)
        source_port_entry_box.config(bg="#353535", fg="#80FF00")
        source_port_entry_box.grid(column=3)

        global destination_ip_entry_box 
        destination_ip_entry_box = Entry(top_frame, width=14)
        destination_ip_entry_box.config(bg="#353535", fg="#80FF00")
        destination_ip_entry_box.grid(column=4)

        global destination_port_entry_box 
        destination_port_entry_box = Entry(top_frame, width=7)
        destination_port_entry_box.config(bg="#353535", fg="#80FF00")
        destination_port_entry_box.grid(column=5)

        global protocol_options 
        protocol_options = StringVar()
        protocol_options.set("tcp")
        global protocol_button 
        protocol_button = OptionMenu(top_frame, protocol_options, "tcp", "udp", "icmp")
        protocol_button.config(bg="#353535", fg="#80FF00", width=5)
        protocol_button.grid(column=6)

        global accept_or_drop_options
        accept_or_drop_options = StringVar()
        accept_or_drop_options.set("ACCEPT")
        global accept_or_drop_button 
        accept_or_drop_button = OptionMenu(top_frame, accept_or_drop_options, "ACCEPT", "DROP")
        accept_or_drop_button.config(bg="#353535", fg="#80FF00", width=7)
        accept_or_drop_button.grid(column=7)

        self.num_rows += 1
        new_rule.grid(column=0, row=self.num_rows, sticky='WE')
        input_output_forward_button.grid(column=1, row=self.num_rows)
        source_ip_entry_box.grid(column=2, row=self.num_rows)
        source_port_entry_box.grid(column=3, row=self.num_rows)
        destination_ip_entry_box.grid(column=4, row=self.num_rows)
        destination_port_entry_box.grid(column=5, row=self.num_rows)
        protocol_button.grid(column=6, row=self.num_rows)
        accept_or_drop_button.grid(column=7, row=self.num_rows)
        row_count += 1

        global row_of_boxes
        # Dictionary to save placements of input on interface for a single row
        row_of_boxes = {}
        row_of_boxes = {'input_output_forward_options' : input_output_forward_options, 
                    'source_ip_entry_box' : source_ip_entry_box,
                    'destination_ip_entry_box' :  destination_ip_entry_box,
                    'protocol_options' : protocol_options,
                    'source_port_entry_box' : source_port_entry_box, 
                    'destination_port_entry_box' : destination_port_entry_box,
                    'accept_or_drop_options' : accept_or_drop_options}
        # Add row to table_of_rules list
        table_of_rules.append(row_of_boxes)
        #print(table_of_rules)

    #Function for linking new rows to the "Add Rule" button
    def __init__(self):
        self.num_rows = 1
        #Auto run function at start
        self.new_row()
        add_rule_button = Button(bottom_center_frame, text='New Rule', font="bold", bg="#353535", fg="#80FF00", command=self.new_row)
        add_rule_button.grid(row=0, column=0)

# Function saves rule to IPTables
def Save_Rules(event):
    #print(table_of_rules)
    rule_to_save = {}
    #Retrieve inputed values from input locations
    for key in table_of_rules: 
        rule_to_save = Save_Helpers.get_current_values(key)
        #print(rule_to_save)
        #Format values into iptable rule and save
        Save_Helpers.iptc_to_ip_tables(rule_to_save)
    # Clear terminal 
    os.system('clear')
    # Display iptables rules
    os.system('sudo iptables-legacy -L')
    #print(table_of_rules)

if __name__ == '__main__':
    main()
