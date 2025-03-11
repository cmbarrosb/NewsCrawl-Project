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

print("Welcome user! This script is used to train the language model using the training data.")
while True:
    print("\n")
    print("Enter the number of the language model you want to work with: ")
    print("1. Unigram Language Model")
    print("2. Bigram Language Model")
    print("3. Bigram Language Model with Add-One Smoothing")
    print("0. to exit the program.")
    switch = input()
    print("You entered:", switch)

     #1. Unigram Language Model
    if switch == "1":
        unigram_file = "unigram_model.json"
        print("\nUnigram Language Model selected...")

        if os.path.exists(unigram_file):
            print(" A saved unigram model exists. What would you like to do?")
            print("1. Train a new model")
            print("2. Load an existing model")
            user_choice = input("Enter your choice (1/2): ").strip()
        else:
            print("No existing model found. You must train a new model.")
            user_choice = "1"

        if user_choice == "1":
            print("Training Unigram Language Model...")
            

            #This function checks if theres an existing unigram model or allows you to train a new one. 
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
                with open(unigram_file, "w") as f:
                    json.dump(unigram_model, f, indent=4)

                print("Trained and saved Unigram Model successfully.")
                return unigram_model
            
            # Train the Unigram Model
            unigram_model = train_unigram("CBtrain_processed.txt")

        elif user_choice == "2":
                print("Loading existing unigram model...")
                with open(unigram_file, 'r') as file:
                    unigram_model = json.load(file)

        # Compute the sum of all unigram probabilities (must equal one)
        prob_sum = sum(unigram_model.values())

        # Print results. Total probability should be 1.
        print(f"\nSuccess!!")
        print(f"Sum of unigram probabilities: {prob_sum:.6f}")  # Format to 6 decimal places
        print(f"Total words in Corpus:{len(unigram_model)}")


    #2. Bigram Language Model
    elif switch == "2":
        print("\nTraining Bigram Language Model...")

        #Function to train the Bigram Model
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

            bigram_prob = {} #dictionary to store bigram probabilities
            for bigram, count in bigram_counts.items():
                prev_word = bigram[0]
                bigram_prob[bigram] = count / unigram_counts[prev_word]

            return bigram_prob, bigram_counts, unigram_counts

        # Train the Bigram Model
        bigram_model, bigram_counts, unigram_counts = train_bigram("CBtrain_processed.txt")

        # Print sample bigram probabilities
        print(f"\n✅ Success!!")
        print("\nBigram Model (first 10 probabilities):")
        for bigram, prob in list(bigram_model.items())[:10]:  # Show first 10 bigrams
            print(f"{bigram}: {prob:.6f}")

        # Print total unique bigrams
        print(f"\nTotal Unique Bigrams: {len(bigram_model)}")



    elif switch == "3":
        #3. Bigram Language Model with Add-One Smoothing
        print("\nTraining Bigram Language Model with Add-One Smoothing...")

    elif switch == "0":
        print("Exiting the program...")
        break
    else:
        print("Invalid input. Please enter a valid number.")
        continue