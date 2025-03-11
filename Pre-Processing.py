# Description: This script is used to pre-process the data by adding padding to the sentences in the training and testing data.
# Functions:
#   1. add_pad(input, out): Adds padding to the sentences in the input file and writes the padded sentences to the output file.
#   2. lowercase(file_path): Converts all the words in the file to lowercase.
#   3. replace_singletons(file_path, singletons): Replaces singleton words in the file with the token <unk>.
#   4. replace_unknowns(test, train): Replaces words in the test data that are not present in the training data with the token <unk>.
#   5. verify(file_path): Counts the total number of words and lines in the file to verify that padding has been successfully added.

from collections import Counter #importing counter to count the frequency of words


#1.Function to automate padding
def add_pad(input, out):
    with open(input, 'r') as old, open(out, 'w') as new: #opens a text file and creates a copy as a new text file
        for line in old:
            pad_sentence = f"<s> {line.strip()} </s>" #removes whitespace and adds padding
            new.write(pad_sentence + "\n")
    print("Padding added ")



# 2.Function to lowercase all words 
def lowercase(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip().lower() for line in file]  # Read and lowercase all lines

    with open(file_path, 'w') as file:
        file.write("\n".join(lines) + "\n")  # Overwrite file with lowercased text

    print("Lowercase applied")


# 3. Function to replace singleton words with token <unk> in the training data

# 3.1 Count word frequencies in training data
def word_frequency(file_path):
    word_freq = Counter()
    with open(file_path, 'r') as file:
        for line in file:
            words = line.strip().split()
            word_freq.update(words)  # Count each word occurrence
    return word_freq

# 3.2  Replace singleton words with <unk> 
def replace_singletons(file_path, singletons):
    lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            words = line.strip().split()
            processed_words = ["<unk>" if word in singletons else word for word in words]
            processed_line = " ".join(processed_words)
            lines.append(processed_line)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(lines) + "\n")  # Overwrite file


#4 Function to repace unique words in test data with <unk>
def replace_unknowns(test, train):
    lines =[] #Store processed lines
    with open(test, 'r') as file:
        for line in file:
            words = line.strip().split()  # Split the line into words
            processed_words = ["<unk>" if word not in train else word for word in words]  # Replace unknown words
            processed_line = " ".join(processed_words)  # Join words back into a sentence
            lines.append(processed_line)  # Store processed sentence
    with open(test, 'w') as file:
        file.write("\n".join(lines) + "\n")  # Overwrite file

# 5.Function to count total words and lines in a file to verify successfully added padding
def verify(file_path):
    word_count = 0
    line_count = 0
    with open(file_path, 'r') as file:
        for line in file:
            words = line.strip().split()  # split sentence into words
            word_count += len(words) # count words
            line_count += 1  # count lines
    return word_count, line_count


# User interface for pre-processing options
while True:
    print("\n")
    print("Select a pre-processing option:")
    print("1 - Automate padding (<s> and </s>)")
    print("2 - Convert text to lowercase")
    print("3 - Replace singletons in training data")
    print("4 - Replace unknown words in test data")
    print("5 - Verify padding and word counts")
    print("6 - Exit")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        add_pad("train.txt", "CBtrain_processed.txt")
        add_pad("test.txt", "CBtest_processed.txt") 

    elif choice == "2":  
        lowercase("CBtrain_processed.txt")
        lowercase("CBtest_processed.txt")

    elif choice == "3":
        freq = word_frequency("CBtrain_processed.txt") #get word frequency
        # Identify singletons
        singletons = {word for word, count in freq.items() if count == 1} #dictionary for singletons
        print(f"{len(singletons)} singleton words to be replaced with <unk>.")
        replace_singletons("CBtrain_processed.txt", singletons) #replace singletons with <unk>

    elif choice == "4":
        train= set(word_frequency("CBtrain_processed.txt").keys())
        # Apply replacement in test data
        replace_unknowns("CBtest_processed.txt", train)
        print("Replaced unseen words with <unk> in test data")  # Function to replace unknowns

    elif choice == "5":
        # Count words and lines in original and processed files
        original_train_words, original_train_lines = verify("train.txt")
        original_test_words, original_test_lines = verify("test.txt")
        processed_train_words, processed_train_lines = verify("CBtrain_processed.txt")
        processed_test_words, processed_test_lines = verify("CBtest_processed.txt")

        #added 2 words per line and need to normalize the count
        expected_train_words = original_train_words + (2 * original_train_lines)
        expected_test_words = original_test_words + (2 * original_test_lines)
        # Display counts
        print(f"Expected Train: {expected_train_words} words,Actual: {processed_train_words}" )
        print(f"Expected Test: {expected_test_words} words, Actual: {processed_test_words}")
        
    elif choice == "6":
        print("Exiting program.")
        break
    else:
        print("Invalid choice.")
        continue

