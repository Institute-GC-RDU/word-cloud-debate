import csv
from collections import Counter
import string

def remove_punctuation_except_apostrophe(text):
    # Create a translation table that maps each punctuation character to None, except for apostrophe
    punctuation_to_remove = string.punctuation.replace("'", "")
    translator = str.maketrans('', '', punctuation_to_remove)
    # Use this table to remove all punctuation except apostrophe
    return text.translate(translator)

def get_word_frequencies(text):
    # Remove punctuation (except apostrophe), convert to lowercase, and split into words
    words = remove_punctuation_except_apostrophe(text.lower()).split()
    return Counter(words)

def write_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Word', 'Frequency'])
        writer.writerows(data)

# Read the transcripts
with open('trump_statements.txt', 'r', encoding='utf-8') as file:
    trump_text = file.read()

with open('harris_statements.txt', 'r', encoding='utf-8') as file:
    harris_text = file.read()

# Get word frequencies
trump_freq = get_word_frequencies(trump_text)
harris_freq = get_word_frequencies(harris_text)

# Combined frequencies
combined_freq = trump_freq + harris_freq

# Get top 500 words for combined frequency
combined_top_500 = dict(combined_freq.most_common(1000))

# Find words said more than twice as often by Trump
trump_dominant = {word: trump_freq[word] for word in combined_top_500 
                  if word in trump_freq and word in harris_freq 
                  and trump_freq[word] > 1.5 * harris_freq[word]}

# Find words said more than twice as often by Harris
harris_dominant = {word: harris_freq[word] for word in combined_top_500 
                   if word in trump_freq and word in harris_freq 
                   and harris_freq[word] > 1.5 * trump_freq[word]}

# Write CSV files
write_csv('Combined_top_500.csv', combined_top_500.items())
write_csv('Trump_dominant_words.csv', trump_dominant.items())
write_csv('Harris_dominant_words.csv', harris_dominant.items())

print("CSV files have been generated: Combined_top_500.csv, Trump_dominant_words.csv, Harris_dominant_words.csv")