 #automate way to add the padding to files

# def add_pad(input, out):
#     with open(input, 'r') as old, open(out, 'w') as new: #opens a text file and creates a copy as a new text file
#         for line in old:
#             pad_sentence = f"<s> {line.strip()} </s>" #removes whitespace and adds padding
#             new.write(pad_sentence + "\n")

# add_pad("train.txt", "CBtrain_padded.txt")
# add_pad("test.txt", "CBtest_padded.txt")


# # Function to count total words and lines in a file
# def count_words_and_lines(file_path):
#     word_count = 0
#     line_count = 0
#     with open(file_path, 'r', encoding='utf-8') as file:
#         for line in file:
#             words = line.strip().split()  # Split sentence into words
#             word_count += len(words)
#             line_count += 1  # Count lines
#     return word_count, line_count

# # Count words and lines in original and processed files
# original_train_words, original_train_lines = count_words_and_lines("train.txt")
# original_test_words, original_test_lines = count_words_and_lines("test.txt")
# processed_train_words, processed_train_lines = count_words_and_lines("CBtrain_padded.txt")
# processed_test_words, processed_test_lines = count_words_and_lines("CBtest_padded.txt")

# # Display results
# print(f"Original Train - Words: {original_train_words}, Lines: {original_train_lines}")
# print(f"Processed Train - Words: {processed_train_words}, Lines: {processed_train_lines}")
# print(f"Original Test - Words: {original_test_words}, Lines: {original_test_lines}")
# print(f"Processed Test - Words: {processed_test_words}, Lines: {processed_test_lines}")

# # Verification Check
# expected_train_words = original_train_words + (2 * original_train_lines)
# expected_test_words = original_test_words + (2 * original_test_lines)

# print("\nVerification:")
# print(f"Expected Processed Train Words: {expected_train_words}, Actual: {processed_train_words}")
# print(f"Expected Processed Test Words: {expected_test_words}, Actual: {processed_test_words}")