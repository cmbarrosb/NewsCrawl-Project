# This final python file will answer questions in the homework based on the work done in Pre-Processing.py and Training_Model.py.


import json

#Question 1:
# How many word types (unique words) are there in the training corpus? Please include the end-of-sentence padding symbol </s> and the unknown token <unk>. Do not include the start of sentence padding symbol <s>.

#Answer 1:
# The Vocabulary size for the training date CBtrain_processed.txt is 41738. 
# The vocabulary size is the number of unique words
# The function vocabulary(json_path) calculates the vocabulary size.
# The function loads the unigram model from the JSON file and counts the unique words in the model.

def vocabulary(json_path):
    #Count unique words in the unigram JSON file, excluding <s>
    with open(json_path, "r") as file:
        unigram_model = json.load(file) # Load the JSON content into a dictionary
    # Remove <s> if it exists in the dictionary
    if "<s>" in unigram_model:
        del unigram_model["<s>"]
    return len(unigram_model)
json_path = "unigram_model.json"  # Adjust if needed
vocab_size = vocabulary(json_path)
print(f"Vocabulary size (excluding <s>): {vocab_size}")

#Question 2:
#How many word tokens are there in the training corpus? Do not include the start of sentence padding symbol <s>.

#Answer 2:
# The number of word tokens in the training data CBtrain_processed.txt is 2468210

def count_tokens(file):
    #Counts total word tokens in a file, excluding <s>
    total_tokens = 0
    with open(file, "r") as file:
        for line in file:
            words = line.strip().split()
            total_tokens += len(words) - words.count("<s>")  # Exclude <s>

    return total_tokens

# Example usage
file_path = "CBtrain_processed.txt"  # Adjust path if needed
total_tokens = count_tokens(file_path)
print(f"Total word tokens (excluding <s>): {total_tokens}")


#Question 3:
# What percentage of word tokens and word types in the test corpus did not occur in
# training (before you mapped the unknown words to <unk> in training and test data)?
# Please include the padding symbol </s> in your calculations. Do not include the start
# of sentence padding symbol <s>.

#Answer 3:
# The percentage of word tokens in the test data that did not occur in training is 1.60%
# The percentage of word types in the test data that did not occur in training is 3.60%


#WARNING this code needs to be run on the processed data withouth the unknown words replaced with <unk>
#If needed create new processed data WITHOUT options 3 and 4 in Pre-Processing.py

#This function calculates the percentage of unseen word tokens and word types in the test data.
def unseen_percentage(train, test):

    #Gets the unique words in the training data
    train_vocab = {word for line in open(train, "r") for word in line.strip().split()}

    #Get the words in the test data
    test_words = [word for line in open(test, "r") for word in line.strip().split()]

    #Get the unique words in the test data
    test_vocab = set(test_words)

    #Calculate unseen tokens and types
    unseen_tokens = sum(1 for word in test_words if word not in train_vocab)
    unseen_types = len(test_vocab - train_vocab)

    #Calculate percentages
    unseen_token_percentage = (unseen_tokens / len(test_words)) * 100
    unseen_type_percentage = (unseen_types / len(test_vocab)) * 100

    return unseen_token_percentage, unseen_type_percentage

train = "CBtrain_processed.txt"
test = "CBtest_processed.txt"
result= unseen_percentage(train, test)
print(f"Percentage of unseen word tokens in the test data: {result[0]:.2f}%")
print(f"Percentage of unseen word types in the test data: {result[1]:.2f}%")