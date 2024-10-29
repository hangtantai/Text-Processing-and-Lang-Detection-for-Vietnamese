from underthesea import ner, sent_tokenize, pos_tag, word_tokenize
import time
import re
import fasttext
import multiprocessing as mp
# Load the language identification model
ft = fasttext.load_model("lid.176.bin")

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
    if word.isdigit():
        return None
    
    en_prob, vi_prob = predict_language(word, ft)
    return word if en_prob > vi_prob else None

# filtering english word from processing text
def filter_english_words(entities_per_sentence):
    english_words = []

    words = [entity[0].lower() for sentence in entities_per_sentence for entity in sentence]
    
    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.map(process_word, words)
    
    english_words = [word for word in results if word is not None]
    
    return english_words

# processing text
def process_text(text):
    # Text normalization: remove excess whitespace and lower all sentence
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

    return entities_per_sentence

### Test case
start_time = time.time()
ft = fasttext.load_model("lid.176.bin")
text = 'Nguyễn Minh Trí mua một căn hộ 3 tỷ VNĐ tại Thành phố Hồ Chí Minh, Hello, The Skyline, support, fix, counter.'
entities_per_sentence = process_text(text)
print(f"Entities: {entities_per_sentence}")
english_words = filter_english_words(entities_per_sentence)
print(f"English word: {english_words}")
end_time = time.time()
print(f"Response time {end_time-start_time}")
# just about 1 seconds for the first time