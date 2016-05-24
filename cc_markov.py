'''This code is inspired by the Codecademy code found in in the markov_chain/markov_python folder. The goal of this file is to use
a Markov chain database and user input to return a response. In this case, we can expect the response to align with something similar
to the way the goal-setting chat bot Emile would respond.'''

import random

'''The goal of this class is to define an input as a Markov Chain, look for any instance where end user input is found within our
Markov chain, and then randomly select the next item in the list to serve as Emile's response.'''

class MarkovChain:
  
  def generate_text(self, user_input, raw_data): # Called by run.py to generate a response to user input at the command line
    user_input = user_input.lower()
    response = []
    for individual in raw_data:
      for text in individual[1::2]: # Only looks through even-index values to match user input with end user messages. (i.e. filters out responses from Emile)
        if user_input in text.lower():
          if len(individual) > (individual.index(text)+1): # Makes sure there is a response from Emile available
            if individual[individual.index(text)+1].split("new_message")[0] != '': # Separates subsequent texts from Emile
              response_text = individual[individual.index(text)+1].split("new_message")
              response.append(response_text) # Creates a list of possible responses from Emile
    final_response = self.select_response(response)
    return final_response
    
  # Method to randomly select a response from Emile
  def select_response(self, response):
    if len(response) < 1: 
      response = "no response" # Emile will respond with "No known response. Try again!" if there is no match to the user input in the chain.
    elif len(response) > 1: 
      index = random.randint(1,len(response)) # Randomly select an available response. 
      response = [response[index - 1]]
    return response
    
