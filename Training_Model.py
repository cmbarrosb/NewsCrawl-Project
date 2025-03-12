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
    unigram_file = "uni_" + train + ".json"
    with open(unigram_file, "w") as f:
        json.dump(unigram_model, f, indent=4)

    print("Trained and saved Unigram Model successfully.")
    return unigram_model

def train_bigram(train, smoothing=False):
    bigram_list = []  # Store all bigram tokens

    with open(train, 'r', encoding="utf-8") as file:
        for line in file:
            words = line.strip().split()
            for i in range(len(words) - 1):
                bigram = (words[i], words[i + 1])  
                bigram_list.append(bigram)  # Keep all occurrences

    bigram_counts = Counter(bigram_list)  # Count occurrences
    total_bigrams = len(bigram_list)  # Count all bigrams (including duplicates)

    # Apply Add-One Smoothing if requested
    if smoothing:
        vocab = len(set(bigram_counts.keys()))  # Vocabulary size (unique bigrams)
        bigram_model = {bigram: (count + 1) / (total_bigrams + vocab) for bigram, count in bigram_counts.items()}
        bigram_file = "bi_1_" + train + ".json"  # Save as Add-One smoothing version
    else:
        bigram_model = {bigram: count / total_bigrams for bigram, count in bigram_counts.items()}
        bigram_file = "bi_" + train + ".json"  # Save as standard bigram model

    # Save model to JSON
    with open(bigram_file, "w") as f:
        json.dump(
            {
                "bigrams": [str(k) for k in bigram_list],  # Store all occurrences
                "probabilities": {str(k): v for k, v in bigram_model.items()}
            },
            f, indent=4
        )

    print(f"Trained and saved {'Bigram Model with Add-One Smoothing' if smoothing else 'Bigram Model'} successfully.")
    return bigram_model, bigram_counts


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

        print("\nUnigram Language Model selected...")
        # Train the Unigram Model
        unigram = train_unigram(data_model)
        # Compute the sum of all unigram probabilities (must equal one)
        prob_sum = sum(unigram.values())

        # Print results. Total probability should be 1.
        print(f"\nSuccess!!")
        print(f"Sum of unigram probabilities: {prob_sum:.6f}")  # Format to 6 decimal places
        print(f"Total words in Corpus:{len(unigram)}")

    #2. Bigram Language Model
    elif switch == "2":
        print("\nBigram Language Model selected...")

        # Train the Bigram Model
        bigram, bigram_counts = train_bigram(data_model)
    
        # Print sample bigram probabilities
        print(f"\n Success!!")
        print("\nBigram Model (first 10 probabilities):")
        for bigram, prob in list(bigram.items())[:10]:  # Show first 10 bigrams
            print(f"{bigram}: {prob:.4f}")

        # Print total unique bigrams
        print(f"\nTotal Unique Bigrams: {len(bigram_counts)}")

    #3. Bigram Language Model with Add-One Smoothing
    elif switch == "3":
        print("\nTraining Bigram Language Model with Add-One Smoothing...")
        bigram_add_one, bigram_counts = train_bigram_add_one(data_model)
        
        # Print sample bigram probabilities
        print(f"\n Success!!")
        print("\nBigram Model with Add-One Smoothing (first 10 probabilities):")
        for bigram, prob in list(bigram_add_one.items())[:10]:  # Show first 10 bigrams
            print(f"{bigram}: {prob:.4f}")

        # Print total unique bigrams
        print(f"\nTotal Unique Bigrams: {len(bigram_counts)}")

    elif switch == "0":
        print("Exiting the program...")
        break
    else:
        print("Invalid input. Please enter a valid number.")
        continue