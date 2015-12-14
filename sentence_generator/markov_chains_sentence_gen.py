# Markov Chains sentence generator using states with two words
# Based on: https://pythonadventures.wordpress.com/2014/01/23/generating-pseudo-random-text-using-markov-chains/ 

# NOTE: this is a toy implementation and it was written with clarity in mind, for example,
# in some place variables could've been reused, but were not, just to make the naming make more sense

# This example is in no way perfect, it might cause "bad" outputs for some inputs, because again,
# this is just a toy implementation.

from random import choice
import argparse

EOS = ['.', '!', '?'] # end of sentence ponctuation
STATE_SIZE = 2 # number of words in state (used to respect list bound rules below)
WORD_SEPARATOR = ' ' # how words in a sentence are separated

def build_states_map(words:list):
	"""
	Build a dictionary from the provided words list, acts as a state machine.
	"""
	num_words = len(words)
	states_map = {} # maps pair of words to a string
	for i in range(num_words - STATE_SIZE):
		first, second, third = words[i], words[i+1], words[i+2]
		# Create sate(s) key -> value
		key = (first, second)
		states_map.setdefault((first, second), []).append(third) 
	return states_map

def generate_sentence_list(states_map:dict):
	"""
	Given a states_map, generates and returns a list of words which represents
	a sentence.
	"""
	# First, let's select a pair that begins with an uppercase letter,
	# since sentences begin with uppercase letters.
	# We're also making sure that the last character of the first word of the key
	# is not an "End Of Sentence" char, this prevents words starting with a capital letter
	# at he end of the sentece to be selected as a beginning of a new sentence
	# (for example to make sure that "Terry." is not selected as the beginning of the
	# word, when generatig states_map from "One of the best defenders 
	# in Premier League is John Terry.")
	upper_states = [key for key in states_map.keys() if key[0][0].isupper() & (key[0][-1] not in EOS)]
	key = choice(upper_states) # randomly select the inital state from the list

	first, second = key
	sentence = [first, second] # the resulting sentence
	
	while True:
		third_list = states_map.get(key) # list of words to which the state (word_1, word_2) maps 
		
		# If the states_map doesn't have the specified key, break from loop
		if third_list is None:
			break

		third = choice(third_list) # select a word at random from the list
		sentence.append(third)
		
		# End of sentence reached
		if (third[-1] in EOS):
			break
		
		key = (second, third) # update the key
		second = third # update "second" for next iteration

	return sentence

def generate_sentence_string(states_map:dict):
	return WORD_SEPARATOR.join(generate_sentence_list(states_map))

def main(in_fname:str, out_fname:str = None, num_iterations:int = 1):
	file_text = ''
	# NOTE: This is far from efficient
	with open(in_fname, mode='rt', encoding='utf-8') as f:
		file_text = f.read()

	words = file_text.split()
	states_map = build_states_map(words)

	# if output file is defined
	if (out_fname):
		# Clear file contents
		with open("out.txt", "w", encoding="utf-8") as f:
			pass
	
	for i in range(0, num_iterations):
		sentence = generate_sentence_string(states_map)
		if (out_fname):
			with open("out.txt", "a", encoding="utf-8") as f:
				f.write(sentence)
		else: # no output file defined, print result to console
			print(sentence)

# Helper functions (not related to Markov Chains)

def positive_check(value:str):
	"""
	Checks if the provided string is a positive integer.
	"""
	val = int(value)
	if val > 0:
		return val
	raise argparse.ArgumentTypeError('{} is not a positive integer'.format(value))


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('in_file', help='input file name', type=str)
	parser.add_argument('-o', '--out_file', help='output file name', type=str)
	parser.add_argument('-i', '--iterations', help='number of iterations (number of sentences to generate)',
							type=positive_check)
	args = parser.parse_args()

	main(args.in_file, args.out_file, args.iterations)	
	


