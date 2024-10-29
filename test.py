import fasttext
import time
import re
import dateparser

from underthesea import ner, word_tokenize, sent_tokenize

from SSMLTagger import SSMLTagger

model = fasttext.load_model(r'link-example')

text = """
ngày 20/10 địa chỉ 10 đường Nguyễn Văn Cừ, số điện thoại 09123748112
Dựa trên yêu cầu của bạn về một 3-bedroom apartment tại Ho Chi Minh City, Quận 3 với ngân sách 2.5 billion VND, here are some options:

1. Căn hộ Green Park: 3 phòng ngủ, 2 phòng tắm, diện tích: 120 m vuông, giá: 2.4 tỷ VNĐ, có hồ bơi và phòng gym.
2. Căn hộ Sunshine City: 3 phòng ngủ, 2 phòng tắm, diện tích: 130 m2, giá: 2.5 tỷ VND, gần trường học và siêu thị.
3. Căn hộ Star Light: 3 phòng ngủ, 1 phòng tắm, diện tích: 110 m^2, giá: 2.3 tỷ vNd, có chỗ đậu xe và khu vui chơi trẻ em.
"""

start_time = time.time()

def extract_address(text):
    match = re.search(r'(\d{1,2}(?:/\d{1,2})*)\s+đường', text)
    if match:
        return match.group(1)
    return None


def extract_phone_number(text):
    match = re.search(r'\b(\d{6,})\b', text)
    if match:
        return match.group(0)
    return None

def is_valid_phone_number(word):
    return re.match(r'^(?:\+?\d{1,3})?[-. ]?\(?\d{1,4}?\)?[-. ]?\d{1,4}[-. ]?\d{1,9}$', word)

def extract_date(text):
    match = re.search(r'(\d{1,2}/\d{1,2})', text)
    if match:
        return dateparser.parse(match.group(1), languages=['vi'])  # Ngôn ngữ là tiếng Việt
    return None

def extract_ordinal_numbers(text):
    #số thứ tự từ 1 đến 100000
    # pattern = r'\b(1[0-9]{0,4}|[1-9][0-9]{0,4})(st|nd|rd|th)?\b|\b(1|[1-9][0-9]{0,4})\b'
    # return re.findall(pattern, text)
    pattern = r'\b(1[0-9]{0,4}|[1-9][0-9]{0,4})(?:st|nd|rd|th)?\b'
    matches = re.findall(pattern, text)
    return matches

def is_valid_number(number):
    if number.isdigit():
        num = int(number)
        return 1 <= num <= 100000
    return False


# test nhận dạng các kiểu số trong câu
address = extract_address(text)
print("Địa chỉ:", address)

phone_number = extract_phone_number(text)
print("Số điện thoại:", phone_number)

date = extract_date(text)
print("Ngày:", date)

ordinal_numbers = extract_ordinal_numbers(text)
print("Số thứ tự:", ordinal_numbers)

# có dấu là tiếng việt
def is_vietnamese_word(word):
    return bool(re.search(r'[àáạảãâầấậẩẫêềếệểễôồốộổỗưừứựửữỳýỵỷỹ0-9]', word))

words = word_tokenize(text)

labels, probs = model.predict(words)

ssml_tagger = SSMLTagger()

def extract_entities(text):
    ner_results = ner(text)

    entities_with_labels = []

    for word, detailed_label, _,_ in ner_results:
        entities_with_labels.append((word, detailed_label,_,_))

    return entities_with_labels

# hàm logic xét tiếng anh không dấu
def is_proper_noun(word):
    entities = extract_entities(word)

    for _, pos_label,_, _ in entities:
        if pos_label == 'Np' or pos_label =='M' and pos_label != 'N':
            return True

    return False

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

def convert_to_ssml(text, labels):
    tagger = SSMLTagger()
    ssml_output = []

    english_words_set = set()

    tokens = word_tokenize(text)

    word_label_pairs = zip(tokens, labels)


    filtered_words = (
        word for word, label in word_label_pairs
        if not is_vietnamese_word(word) and label[0] != "__label__vi" and is_proper_noun(word)
    )

    english_words_set.update(filtered_words)

    print("Các từ tiếng anh (đã loại bỏ những từ tiếng việt không dấu):", english_words_set)

    ssml_output.append(tagger.open_voice())

    for word in word_tokenize(text):
        if address and word in address:
            ssml_output.append(tagger.add_say_as(address, interpret_as="address"))
            continue

        elif word in ordinal_numbers:
            ssml_output.append(tagger.add_say_as(word, interpret_as="ordinal"))
            continue

        elif phone_number and word in phone_number and is_valid_phone_number(word):
            ssml_output.append(tagger.add_say_as(phone_number, interpret_as="telephone"))
            continue

        elif date and word == date.strftime('%d/%m'):
            ssml_output.append(tagger.add_say_as(date.strftime('%d/%m'), interpret_as="date"))
            continue

        elif word in english_words_set:
            lang_code = "en-GB"
            ssml_output.append(tagger.add_lang(lang_code, word).ssml.strip())
        else:
            ssml_output.append(tagger.add_emphasis(word, level="moderate").ssml.strip())

    ssml_output.append(tagger.close_voice())
    return  tagger.build()



ssml_result = convert_to_ssml(text, labels)

print(ssml_result)

end_time = time.time()
execution_time = end_time - start_time
print(f"time: {execution_time:.4f} giây")