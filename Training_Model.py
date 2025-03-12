#Description: This file contains the code for training the model.
    #Unigram language Model: Unigram language model assumes each word is independent of each other on a corpus. The probability of a particular sentence is the product of its individual word probabilities.
        #Functions:
            #train_unigram(train): This function trains the unigram language model on the training data and returns the total probability and total words in the corpus.

    #Bigram language Model: Bigram language model assumes that the probability of a word depends only on the previous word. The probability of a sentence is the product of the probabilities of each word given the previous word.

    #Bigram with Add-One Smoothing: Add-One smoothing is a technique used to handle unseen words in the training data. It adds a small constant to the count of each word to avoid zero probabilities.
    #Functions:

#Importing libraries
import json
import math
import os
from collections import Counter, defaultdict 

#Functions:
#Unigram Function
def train_unigram(train):
    #variables to store word counts and total words
    word_counts = Counter()
    total_words = 0
    with open(train, 'r') as file: #handling the training data
        for line in file:
            words = line.strip().split()
            word_counts.update(words)
            total_words += len(words)
    unigram_model = {} #dictionary to store unigram probabilities

    #probability of each word
    for word, count in word_counts.items():
        unigram_model[word] = count / total_words 

    # Save model to JSON
    unigram_file = "unigram_model_" + train + ".json"
    with open(unigram_file, "w") as f:
        json.dump(unigram_model, f, indent=4)

    print("Trained and saved Unigram Model successfully.")
    return unigram_model

#Bigram Function
def train_bigram(train):
    unigram_counts = Counter()  # Store word frequencies
    bigram_counts = defaultdict(int)  # Store bigram frequencies as integer
    with open(train, 'r') as file:
        for line in file:
            words = line.strip().split()
            unigram_counts.update(words)  # Update unigram counts which are necessary for MLE calculation
            
            for i in range(len(words) - 1):
                bigram = (words[i], words[i + 1])  # Create bigram using a tuple
                bigram_counts[bigram]+= 1  # Count bigram occurrences

    bigram_model = {} #dictionary to store bigram probabilities
    for bigram, count in bigram_counts.items():
        prev_word = bigram[0]
        bigram_model[bigram] = count / unigram_counts[prev_word]

    # Save model to JSON
    bigram_file = "bigram_model" + train +".json"
    with open(bigram_file, "w") as f:
        json.dump({str(k): v for k, v in bigram_model.items()}, f, indent=4)

    print("Trained and saved Bigram Model successfully.")
    return bigram_model, bigram_counts, unigram_counts



print("Welcome user! This script is used to train the language model using the training data.")
print("Please make sure you have the training data in the same directory as this script.")

data_model= input("Enter the name of the file that you will work with:").strip()


while True:
    print("\n")
    print("Enter the number of the language model you want to work with: ")
    print("1. Unigram Language Model")
    print("2. Bigram Language Model")
    print("3. Bigram Language Model with Add-One Smoothing")
    print("0. to exit the program.")
    switch = input()

     #1. Unigram Language Model
    if switch == "1":
        #Check if unigram model exists
        unigram_file = "unigram_model.json"
        print("\nUnigram Language Model selected...")

        if os.path.exists(unigram_file):
            print(" A saved unigram model exists. What would you like to do?")
            print("1. Train a new model")
            print("2. Load an existing model")
            uni_choice = input("Enter your choice (1/2): ").strip()
        else:
            print("No existing model found. You must train a new model.")
            uni_choice = "1"

        if uni_choice == "1":
            print(" Unigram Language Model...")
            # Train the Unigram Model
            unigram = train_unigram(data_model)

        elif uni_choice == "2":
                print("Loading existing unigram model...")
                with open(unigram_file, 'r') as file:
                    unigram = json.load(file)

        else:
            print("Invalid input. Please enter a valid number.")
            continue

        # Compute the sum of all unigram probabilities (must equal one)
        prob_sum = sum(unigram.values())

        # Print results. Total probability should be 1.
        print(f"\nSuccess!!")
        print(f"Sum of unigram probabilities: {prob_sum:.6f}")  # Format to 6 decimal places
        print(f"Total words in Corpus:{len(unigram)}")

        


    #2. Bigram Language Model
    elif switch == "2":
        bigram_file = "bigram_model.json"
        print("\nBigram Language Model selected...")

        if os.path.exists(bigram_file):
            print(" A saved bigram model exists. What would you like to do?")
            print("1. Train a new model")
            print("2. Load an existing model")
            bi_choice = input("Enter your choice (1/2): ")
        else:
            print("No existing model found. You must train a new model.")
            bi_choice = "1"

        if bi_choice == "1":
            print("Training Bigram Language Model...")
            # Train the Bigram Model
            bigram, bigram_counts, unigram_counts = train_bigram(data_model)

        elif bi_choice == "2":
            print("Loading existing bigram model...")
            with open(bigram_file, "r") as f:
                bigram = {eval(k): v for k, v in json.load(f).items()}

        else:
            print("Invalid input. Please enter a valid number.")
            continue
        
    
        # Print sample bigram probabilities
        print(f"\n Success!!")
        print("\nBigram Model (first 10 probabilities):")
        for bigram, prob in list(bigram.items())[:10]:  # Show first 10 bigrams
            print(f"{bigram}: {prob:.6f}")

        # Print total unique bigrams
        print(f"\nTotal Unique Bigrams: {len(bigram)}")



    elif switch == "3":
        #3. Bigram Language Model with Add-One Smoothing
        print("\nTraining Bigram Language Model with Add-One Smoothing...")

    elif switch == "0":
        print("Exiting the program...")
        break
    else:
        print("Invalid input. Please enter a valid number.")
        continue