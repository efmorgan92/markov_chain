'''This file loops through a directory of Slack log files and pulls out individual texts from both Emile and end users, then concatenates them into a Markov chain of conversation. 
The output is a single list of all conversations, in which each item is a list of a single individuals conversation with Emile. Individual conversation lists are formatted 
such that user inputs always fall on an odd index while Emile's responses fall on an even input.

This allows the program in run.py to only search for user inputs that match previous end user entries, and to only respond with texts previously sent by Emile. '''

import os

# Method to combine each individual conversation chain into one giant "list of lists"
def combine_end_users():
    folders = sorted(os.listdir("slack_raw_data/Emile Slack Logs"))
    final_chain = []
    for folder in folders:
        path = "slack_raw_data/Emile Slack Logs/" + folder + "/"
        final_chain.append(combine_data(path))
    return final_chain

# Opens all files in a folder and combines them into a single conversational chain. One folder contains all messages and responses from a single end user.
def combine_data(path):
    final_chain = ["", "Emile"]
    files = sorted(os.listdir(path))
    for file in files:
        chain = fetch_data(path + file) # Calls fetch_data method to create a chain of texts from a single file
        
        ''' In order to keep proper indexing, the following code segment checks to see whether two or more continuous texts have come in from the same user 
        (Emile or end user) and combines those into a single text. The texts are delimited by a unique "new_message" delimiter, so they can be separated in run.py code'''
        if final_chain[len(final_chain)-1] == "Emile":
            last_user = "Emile"
        elif final_chain[len(final_chain)-1] == "end_user":
            last_user = "end_user"
            
        if last_user == "end_user":
            if chain[0] == "": # starts and ends with end user -> remove last value in final_chain
                final_chain[len(final_chain)-2] += chain[1]
                
                if len(chain) > 2:
                    final_chain[len(final_chain)-1] = chain[2]
                else: final_chain = final_chain[:len(final_chain)-2]
                
                for item in chain[3:]:
                    final_chain.append(item)
            else: # ends with end user and starts with Emile -> replace last value with first
                final_chain[len(final_chain)-1] = chain[0]
                for item in chain[1:]:
                    final_chain.append(item)
        elif last_user == "Emile": # ends with Emile
            if chain[0] == "": #ends with Emile and starts with end_user
                final_chain[len(final_chain)-1] = chain[1]
                for item in chain[2:]: 
                    final_chain.append(item)
            else: # ends with Emile and starts with Emile
                final_chain[len(final_chain)-2] += chain[0]
                final_chain[len(final_chain)-1] = chain[1]
                for item in chain[2:]:
                    final_chain.append(item)
                    
    # Clean up the output. Emile's responses are stored with some funky characters. The code below will make him more legible at the command line. 
    for item in final_chain:
            new_item = item.replace("\u2019","'")
            new_item = new_item.replace("\u00a0"," ")
            new_item = new_item.replace("\/","/")
            final_chain[final_chain.index(item)] = new_item
    
    # Returns the final chain of conversation to be appended to the list of all conversations.
    final_chain = final_chain[:len(final_chain)-1]
    return final_chain
            
            
    
# This method is called by combine_data() and converts an input of one .json file into an output of a string of partial conversation.
def fetch_data(raw_data):
    # read in the data
    markov_data = open(raw_data,"r")
    raw_input = markov_data.read()
    markov_data.close()
    
    # Parse out data into initial messages
    data = [""]
    counter = 0
    for ch in raw_input: 
        if ch == "[" or ch == "]" or ch == '"':
            pass
        elif ch == "{":
            counter += 1
            data.append("")
        elif ch == ",":
            data[counter] = data[counter] + " "
        else:
            data[counter] = data[counter] + ch
            
    # pull out relevant messages and text from data
    # If Emile is the first to text, the first item in chain will be populated. Otherwise, the first item will be null. 
    chain = [""]
    counter = 0
    user = "Emile" # Keeps track of the last person to text (Emile or end user) in order to combine messages where necessary
    for item in data: 
        if "text" in item: 
            # Parses out additional Slack messages and behaves differently based on who the last messager was. 
            if item.find("channel_join") == -1 and item.find("channel_topic") == -1 and item.find("channel_purpose") == -1:
                message = item
                message = message.rsplit("text: ")
                message = message[1]
                message = message.rsplit("\n")
                message = message[0]
                if 'username: them' in item:
                    if user == "end_user":
                        chain[counter] += "new_message" + message
                    else:
                        counter += 1
                        chain.append("")
                        chain[counter] = message
                    user = "end_user"
                else: 
                    if user == "Emile" or user == "":
                        chain[counter] += "new_message" + message
                    else:
                        counter += 1
                        chain.append("")
                        chain[counter] = message
                    user = "Emile"
    # Create a chain of messages and then return them to the combine_data method. 
    chain.append(user)
    return chain
