# Text Summarization of an online article

import bs4 as BeautifulSoup
import urllib.request  

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from nltk.tokenize import word_tokenize, sent_tokenize

# Fetching the content from the URL
fetched_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Automatic_summarization')

article_read = fetched_data.read()

# Parsing the URL content and storing in a variable
article_parsed = BeautifulSoup.BeautifulSoup(article_read,'html.parser')

# Returning <p> tags
paragraphs = article_parsed.find_all('p')

article_content = ''

# Looping through the paragraphs and adding them to the variable
for p in paragraphs:  
    article_content += p.text

print("ARTICLE CONTENT")
print("==========================================================================")
print(article_content)
print("==========================================================================")

# PREPROCESSING

def create_dictionary_table(text_string) -> dict:
   
    # Removing stop words
    stop_words = set(stopwords.words("english"))
    
    words = word_tokenize(text_string)
    
    # Reducing words to their root form
    stem = PorterStemmer()
    
    # Creating dictionary for the word frequency table
    frequency_table = dict()
    for wd in words:
        wd = stem.stem(wd)
        if wd in stop_words:
            continue
        if wd in frequency_table:
            frequency_table[wd] += 1
        else:
            frequency_table[wd] = 1

    return frequency_table

frequency_table = create_dictionary_table(article_content);
print("FREQUENCY TABLE")
print("==========================================================================")
print(frequency_table)
print("==========================================================================")

# TOKENIZING THE ARTICLE INTO SENTENCES

sentences = sent_tokenize(article_content)

# FINDING WEIGHTED FREQUENCY OF SENTENCES

def calculate_sentence_scores(sentences, frequency_table) -> dict:   

    # Algorithm for scoring a sentence by its words
    sentence_weight = dict()

    for sentence in sentences:
        sentence_wordcount = (len(word_tokenize(sentence)))
        sentence_wordcount_without_stop_words = 0
        for word_weight in frequency_table:
            if word_weight in sentence.lower():
                sentence_wordcount_without_stop_words += 1
                if sentence[:7] in sentence_weight:
                    sentence_weight[sentence[:7]] += frequency_table[word_weight]
                else:
                    sentence_weight[sentence[:7]] = frequency_table[word_weight]

        sentence_weight[sentence[:7]] = sentence_weight[sentence[:7]] / sentence_wordcount_without_stop_words
      
    return sentence_weight

sentence_weight = calculate_sentence_scores(sentences, frequency_table)
print("SENTENCE WEIGHT")
print("==========================================================================")
print(sentence_weight)
print("==========================================================================")

def calculate_average_score(sentence_weight) -> int:
   
    # Calculating the average score for the sentences
    sum_values = 0
    for entry in sentence_weight:
        sum_values += sentence_weight[entry]

    # Getting sentence average value from source text
    average_score = (sum_values / len(sentence_weight))

    return average_score

average_score = calculate_average_score(sentence_weight)
print("AVERAGE SCORE")
print("==========================================================================")
print(average_score)
print("==========================================================================")

def get_article_summary(sentences, sentence_weight, threshold):
    sentence_counter = 0
    article_summary = ''

    for sentence in sentences:
        if sentence[:7] in sentence_weight and sentence_weight[sentence[:7]] >= (threshold):
            article_summary += " " + sentence
            sentence_counter += 1

    return article_summary

article_summary = get_article_summary(sentences, sentence_weight, average_score)

print("ARTICLE SUMMARY")
print("==========================================================================")
print(article_summary)
print("==========================================================================")