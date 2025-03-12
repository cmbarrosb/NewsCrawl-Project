# This final python file will answer questions in the homework based on the work done in Pre-Processing.py and Training_Model.py.


import json
import math
from collections import Counter

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

#Question 4:


#WARNING THIS FUNCTION ASSUMES YOU HAVE REATED TWO BIGRAM JSON FILES FOR TRAIN AND TEST DATA
#IF YOU HAVE NOT DONE SO, PLEASE RUN THE TRAINING_MODEL.PY FILE TO CREATE THE BIGRAM JSON FILES

#Computes the percentage of unseen bigram types and tokens in the test set
def compute_unseen_bigrams(train_bigram_file, test_bigram_file):
    
    with open(train_bigram_file, "r") as f:
        train_bigrams = set(eval(k) for k in json.load(f)["bigrams"])  # Load bigrams as a set

    with open(test_bigram_file, "r") as f:
        test_bigram_data = json.load(f)
        test_bigrams = test_bigram_data["bigrams"]

   # Count occurrences of bigrams in the test set
    test_bigram_counts = Counter(eval(k) for k in test_bigrams)

    # Identify unseen bigram types
    unseen_bigram_types = set(test_bigram_counts.keys()) - train_bigrams

    # Count unseen bigram tokens
    unseen_bigram_tokens = sum(count for bigram, count in test_bigram_counts.items() if bigram not in train_bigrams)

    # Compute percentages
    unseen_bigram_type_percentage = (len(unseen_bigram_types) / len(set(test_bigram_counts.keys()))) * 100
    unseen_bigram_token_percentage = (unseen_bigram_tokens / sum(test_bigram_counts.values())) * 100

    return unseen_bigram_type_percentage, unseen_bigram_token_percentage       

#Question 5: 
    #Compute the log probability of the following sentence under the three models:
        # I look forward to hearing your reply .
    # Please list all of the parameters required to compute the probabilities and show the complete calculation. Which of the parameters have zero values under each model? Use log base 2 in your calculations.


#the following function loads the models from a json file and computer the log probabilities for the given sentence
#The function returns the log probabilities for the unigram model, bigram model, and bigram model with Add-One smoothing.
#The functions also offers calculations for the unseen bigrams in the bigram model and bigram model with Add-One smoothing.

def log_probability(sentence, unigram_file, bigram_file, bigram_smooth):
    
    # Load unigram probabilities
    with open(unigram_file, "r") as f:
        unigram_model = json.load(f)

    # Load bigram probabilities (MLE)
    with open(bigram_file, "r") as f:
        bigram_data = json.load(f)
        bigram_model = {eval(k): v for k, v in bigram_data["probabilities"].items()}

    # Load Add-One smoothing data
    with open(bigram_smooth, "r") as f:
        smooth_data = json.load(f)
        bigram_smooth = {eval(k): v for k, v in smooth_data["probabilities"].items()}
        unigram_counts = smooth_data["unigram_counts"]
        vocab_size = smooth_data["vocab_size"]

    # Initialize log probabilities
    log_unigram = 0
    log_bigram = 0
    log_smooth = 0

    # Compute unigram log probability
    for word in sentence:
        prob_unigram = unigram_model.get(word, unigram_model["<unk>"])  # unseen words mapped to <unk>
        log_unigram += math.log2(prob_unigram)

    # Compute bigram
    for i in range(1, len(sentence)):
        prev_word, current_word = sentence[i-1], sentence[i]
        bigram_pair = (prev_word, current_word) #prev_word = n-1, current_word = n

        # Bigram probability 
        prob_bigram = bigram_model.get(bigram_pair, 0)
        if prob_bigram > 0:
            log_bigram += math.log2(prob_bigram)
        else: # unseen bigram, set log probability to negative infinity
            log_bigram = float('-inf')
            break

    # Compute bigram with Add-One smoothing
    for i in range(1, len(sentence)):
        prev_word, current_word = sentence[i-1], sentence[i]
        bigram_pair = (prev_word, current_word) #prev_word = n-1, current_word = n

        # Bigram Add-One 
        prob_smooth = bigram_smooth.get(bigram_pair)
        if prob_smooth == 0 :  # unseen bigram, compute explicitly
            prob_smooth = 1 / (unigram_counts.get(prev_word, 0) + vocab_size)
        log_smooth += math.log2(prob_smooth)

    return log_unigram, log_bigram, log_smooth





# Main function to interact with the user
print("Welcome. This program will answer questions based on the pre-processing and training steps.")


while True:
    question = input("Enter the question number (1-4) or '0': ").strip()
  
    if question == "1":
        unigram=input("Enter the path to the unigram model: ")
        vocab_size = vocabulary(unigram)
        print(f"Vocabulary size (excluding <s>): {vocab_size}")

    elif question == "2":
        file_path =input("Enter the path to the data to count tokens: ")
        total_tokens = count_tokens(file_path)
        print(f"Total word tokens (excluding <s>): {total_tokens}")

    elif question == "3":
        train = input("Enter the path to the training data: ")
        test = input("Enter the path to the test data: ")
        
        result= unseen_percentage(train, test)  
        print(f"Percentage of unseen word tokens in the test data: {result[0]:.2f}%")
        print(f"Percentage of unseen word types in the test data: {result[1]:.2f}%")

    elif question == "4":
        train_bigram_json = input("Enter the path to the training bigram model: ")
        test_bigram_json = input("Enter the path to the test bigram model: ")

        unseen_type_pct, unseen_token_pct = compute_unseen_bigrams(train_bigram_json, test_bigram_json)
        print(f"Unseen bigram types: {unseen_type_pct:.2f}%")
        print(f"Unseen bigram tokens: {unseen_token_pct:.2f}%")

    elif question == "5":
        # Prompt user for file names
        data=input("Enter the file to compute log probabilities: ")
        unigram_file = input("Enter the unigram JSON file name: ")
        bigram_file = input("Enter the bigram JSON file name: ")
        bigram_add_one_file = input("Enter the bigram (Add-One smoothing) JSON file name: ")`

        # Compute log probabilities
        log_unigram, log_bigram, log_smooth = log_probability(data, unigram_file, bigram_file, bigram_add_one_file)

        # Display
        print(f"Log Probability (Unigram Model): {log_unigram:.4f}")
        print(f"Log Probability (Bigram MLE): {log_bigram if log_bigram != float('-inf') else '-inf (zero probability)'}")
        print(f"Log Probability (Bigram Add-One Smoothing): {log_smooth:.4f}")

    elif question == "0":
        print("Exiting the program...")
        break

    else:
        print("Invalid question number. Please enter a valid question number (1-4) or 'exit'.")