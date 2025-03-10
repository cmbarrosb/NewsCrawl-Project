#Description: This file contains the code for training the model.
    #Unigram language Model: Unigram language model assumes each word is independent of each other on a corpus. The probability of a particular sentence is the product of its individual word probabilities.
        #Functions:

    #Bigram language Model: Bigram language model assumes that the probability of a word depends only on the previous word. The probability of a sentence is the product of the probabilities of each word given the previous word.

    #Bigram with Add-One Smoothing: Add-One smoothing is a technique used to handle unseen words in the training data. It adds a small constant to the count of each word to avoid zero probabilities.
    #Functions:

from collections import Counter #importing counter to count the frequency of words

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
    if switch == "1":
        print("\nTraining Unigram Language Model...")
        #1. Unigram Language Model
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

        # Print total probability = 1
        sum=0
        for word, prob in list(unigram_model.items()): 
            sum+=prob
        print("\nSum of probabilities:",sum)
        # Print total words
        print(f"\nSucess!!\nTotal Words in Corpus: {total_words}")
    
    elif switch == "2":
        #2. Bigram Language Model
        print("\nTraining Bigram Language Model...")

    elif switch == "3":
        #3. Bigram Language Model with Add-One Smoothing
        print("\nTraining Bigram Language Model with Add-One Smoothing...")

    elif switch == "0":
        print("Exiting the program...")
        break
    else:
        print("Invalid input. Please enter a valid number.")
        continue