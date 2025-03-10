def add_pad(input, out): #automate way to add the padding to files
    with open(input, 'r') as old, open(out, 'w') as new: #opens a text file and creates a copy as a new text file
        for line in old:
            pad_sentence = f"<s> {line.strip()} </s>" #removes whitespace and adds padding
            new.write(pad_sentence + "\n")

add_pad("train-Spring2025.txt", "CBtrain_padded.txt")
add_pad("test.txt", "CBtest_padded.txt")
