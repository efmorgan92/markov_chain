'''This file will run the Emile chat bot program, in which Emile responds to user input about setting and achieving goals.
This file combines the functions of the get_raw_data and cc_markov files to output the final program. '''

# combine the code to collect database information and run the Markov chain program. 
from markov_python.cc_markov import MarkovChain
from get_raw_data import combine_end_users, combine_data, fetch_data
from time import sleep

# aggregate the raw data into a Markov chain and initialize a MarkovChain class instance
raw_data = combine_end_users()
emile_mc = MarkovChain()

# Run the interactive program. The initial steps are hard coded to reflect the "onboarding" process
print "Emile: Hi! I'm Emile, a self improvement AI. Would you like to work on sleep or exercise? \n"
user_input = raw_input("User entry (or q to Quit): ")
while user_input != 'q':
    if user_input.lower() == "sleep":
        print "\nEmile: Do you want to focus on your bed time, your wake time, or simply the number of hours of sleep you get per night? \n"
    elif user_input.lower() == "exercise":
        print "\nEmile: Great! As a baseline, how many days did you exercise last week, and what's your ideal number of exercise days?\n"
    else:
        emile_ans = emile_mc.generate_text(user_input, raw_data)
        if emile_ans == "no response": # Emile will only respond to input he has "seen" in the past
            print "\n","No known response. Try again!","\n"
        else:
            print "\n","Emile:",emile_ans[0][0],"\n"
            
            if len(emile_ans[0]) > 1: # If Emile's response contains 2+ continuous texts, he will respond again before prompting for user input
                sleep(1)
                print "Emile:",emile_ans[0][1],"\n"
    user_input = raw_input("User entry (or q to Quit): ") # continue until user quits out of the program
