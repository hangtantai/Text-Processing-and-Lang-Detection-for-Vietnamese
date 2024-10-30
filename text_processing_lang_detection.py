from underthesea import ner, sent_tokenize, pos_tag, word_tokenize
import time
import re
import fasttext
import multiprocessing as mp
from function_util import TextClassifier

# Load the language identification model
ft = fasttext.load_model("lid.176.bin")
# Initialize the TextClassifier
classifier = TextClassifier()

# OOV
out_vocab = ["de", "van", ""]

# Get prediction language with two option en or vi
def predict_language(text, model, languages=('__label__en', '__label__vi')):
    # Get predictions
    predictions = model.predict(text, k=-1)  # k=-1 returns all predictions
    labels, probabilities = predictions
    
    # Filter predictions for the specified languages
    filtered_predictions = {label: prob for label, prob in zip(labels, probabilities) if label in languages}
    
    # Return the probabilities for 'en' and 'vi'
    en_prob = filtered_predictions.get('__label__en', 0)
    vi_prob = filtered_predictions.get('__label__vi', 0)
    
    return en_prob, vi_prob

# processing word: comparing vi or en word
def process_word(word):    
    if word[1] == "O":
        return None
    en_prob, vi_prob = predict_language(word[0], ft)
    return word if en_prob > vi_prob else None

# filtering english word from processing text
def filter_english_words(entities_per_sentence):
    english_words = []

    words = [(sentence[0].lower(), sentence[3]) for sentence in entities_per_sentence ]
    
    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.map(process_word, words)
    
    english_words = [word for word in results if word is not None]
    
    return english_words

# processing text
def process_text(text):
    # Text normalization: remove excess whitespace and lower all sentence
    processed_sentences = []
    text = text.strip()
    text = re.sub(r"\s+", " ", text) 

    # Sentence Segmentation before NER: This step reduces the text chunk that NER has to process at one time, improving both accuracy and speed.
    sentences = sent_tokenize(text)
    # Word Segmentation
    for elem in sentences:
        word_list = word_tokenize(elem)

        # POS Tagging to Aid NER: helps identify nouns, numbers, and other parts of speech
        tagged_sentences = [pos_tag(sentence) for sentence in word_list]

        # Apply NER Selectively Based on POS Tags
        entities_per_sentence = [ner(sentence) for sentence, tags in zip(word_list, tagged_sentences) if any(tag[1] in ['N', 'M', 'Np'] for tag in tags)]
        processed_sentences.extend(entities_per_sentence)
    return processed_sentences



def process_sentence(sentence):
    word_list = word_tokenize(sentence)
    tagged_sentences = [pos_tag(sentence) for sentence in word_list]
    entities_per_sentence = [ner(sentence) for sentence, tags in zip(word_list, tagged_sentences) if any(tag[1] in ['N', 'M', 'Np'] for tag in tags)]
    return entities_per_sentence

def process_sentences(sentences):
    processed_sentences = []
    sentences = sentences.strip()
    sentences = re.sub(r"\s+", " ", sentences) 
    sentences = sent_tokenize(sentences)

    # print(sentences)
    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.map(process_sentence, sentences)
    print(results)
    for result in results:
        processed_sentences.extend(result)
    
    return processed_sentences

# Function to detect unknown entities
def detect_unknown_entities(entities_per_sentence):
    unknown_entities = []
    for sentence in entities_per_sentence:
        for entity in sentence:
            entity_text = entity[0]
            category = classifier.classify(entity_text)
            if category == 'unknown':
                unknown_entities.append(entity)
    return unknown_entities

### Test case

# ft = fasttext.load_model("lid.176.bin")
text = """
Nguyễn Văn Linh Parkway , Pasteur Street, Alexander de Rhodes Street, Charles De Gaulle Street
"""
print("WIHOUT MULTIPROCESSING")
start_time = time.time()

entities_per_sentence = process_text(text)
print(f"Entities: {entities_per_sentence}")
unknown_word = detect_unknown_entities(entities_per_sentence)
print(f"Unknown Word: {unknown_word}")
english_words = filter_english_words(unknown_word)
print(f"English word: {english_words}")
end_time = time.time()
print(f"Response time {end_time-start_time}")
# just about 1 seconds for the first time


print("WITH MULTIPROCESSING")
start_time = time.time()
entities_per_sentence = process_text(text)
print(f"Entities: {entities_per_sentence}")
unknown_word = detect_unknown_entities(entities_per_sentence)
print(f"Unknown Word: {unknown_word}")
english_words = filter_english_words(unknown_word)
print(f"English word: {english_words}")
end_time = time.time()
print(f"Response time {end_time-start_time}")