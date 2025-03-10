#Description: This file contains the code for training the model.
    #Unigram language Model: Unigram language model assumes each word is independent of each other on a corpus. The probability of a particular sentence is the product of its individual word probabilities.
        #Functions:
            #train_unigram(train): This function trains the unigram language model on the training data and returns the total probability and total words in the corpus.

    #Bigram language Model: Bigram language model assumes that the probability of a word depends only on the previous word. The probability of a sentence is the product of the probabilities of each word given the previous word.

    #Bigram with Add-One Smoothing: Add-One smoothing is a technique used to handle unseen words in the training data. It adds a small constant to the count of each word to avoid zero probabilities.
    #Functions:

#Importing libraries
from collections import Counter, defaultdict 

print("Welcome user! This script is used to train the language model using the training data.")
while True:
    print("\n")
    print("Enter the number of the language model you want to train: ")
    print("1. Unigram Language Model")
    print("2. Bigram Language Model")
    print("3. Bigram Language Model with Add-One Smoothing")
    print("0. to exit the program.")
    switch = input()
    print("You entered:", switch)

     #1. Unigram Language Model
    if switch == "1":
        print("\nTraining Unigram Language Model...")

        #Function to train the Unigram Model
        def train_unigram(train):
            #variables to store word counts and total words
            word_counts = Counter()
            total_words = 0
            #handling the training data
            with open(train, 'r') as file:
                for line in file:
                    words = line.strip().split()
                    word_counts.update(words)
                    total_words += len(words)

            unigram_prob = {} #dictionary to store unigram probabilities

            for word, count in word_counts.items():
                unigram_prob[word] = count / total_words #probability of each word according to MLE formula

            return unigram_prob, word_counts, total_words

        # Train the Unigram Model
        unigram_model, word_counts, total_words = train_unigram("CBtrain_processed.txt")

        # Compute the sum of all unigram probabilities
        prob_sum = sum(unigram_model.values())

        # Print results. Total probability should be 1.
        print(f"\n✅ Success!!")
        print(f"Sum of unigram probabilities: {prob_sum:.6f}")  # Format to 6 decimal places
        print(f"Total Words in Corpus: {total_words}")


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