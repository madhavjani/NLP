You will first write a program to tokenize text, and output it in a format that is particularly easy to work with. Your program will read NunavutHansard.en.gz or NunavutHansard.iu.ICI.utf8. norm.gz. For each line in the file, it will tokenize the text, and print each token on a separate line, with a blank line after each sentence.5 Your program should print to standard output.
To tokenize the text, use regular expressions. The following describes the tokenization:
• Any sequence of alphanumeric characters, underscores, hyphens, or apostrophes, that option-
ally begins with $, is a token.
• Any sequence of other non-whitespace characters is a token;
• Any sequence of whitespace characters is a token boundary. (Whitespace does not appear as tokens in the output.)
sample.tokens is an example showing the expected output of the tokenizer when run on sample. txt.gz.
Your program should be called as follows:
python tokenize.py FILE > FILE.tokens
where FILE is either NunavutHansard.en.gz or NunavutHansard.iu.ICI.utf8.norm.gz. This will create a file called tokens containing the tokenized corpus.
