my_list = ['pune','jcb','one']

# Create a dictionary to map string elements to integers
mapping = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20}

# Use a list comprehension to replace string elements with integers
my_list = [mapping[x] for x in my_list]

print(my_list)
