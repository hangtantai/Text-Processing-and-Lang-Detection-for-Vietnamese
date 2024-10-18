import azure.cognitiveservices.speech as speechsdk
from langdetect import detect, DetectorFactory, LangDetectException
import re
# Set a seed for consistent language detection results
DetectorFactory.seed = 0

# Replace with your own subscription key and service region
subscription_key = "your key"
service_region = "your region"

# Create a speech configuration
speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

def synthesize_multilingual_text(user_input):
    # Initialize SSML string
    ssml_string = "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>"

    # Split the input into words for better language detection
    words = user_input.split()
    current_language = None
    phrase = ""

    for word in words:
        # Detect the language of the current word
        # Detect if the word is a number
        if word.isdigit():
            language = 'vi'
        else:
            try:
                language = detect(word)
            except LangDetectException:
                print(f"Could not detect language for word: {word}")
                continue

        # If the language changes, synthesize the previous phrase
        if current_language is None:
            current_language = language

        if language != current_language:
            # Add the previous phrase to SSML
            if current_language == 'vi':
                ssml_string += f"<voice name='vi-VN-HoaiMyNeural'>{phrase.strip()}</voice>"
            else:
                ssml_string += f"<voice name='en-US-AvaMultilingualNeural'>{phrase.strip()}</voice>"
            
            # Reset for the new language
            phrase = word
            current_language = language
        else:
            phrase += " " + word

    # Add the last phrase to SSML
    if current_language == 'vi':
        ssml_string += f"<voice name='vi-VN-HoaiMyNeural'>{phrase.strip()}</voice>"
    else:
        ssml_string += f"<voice name='en-US-AvaMultilingualNeural'>{phrase.strip()}</voice>"

    ssml_string += "</speak>"

    try:
        # Ensure the SSML string is properly encoded
        ssml_string = re.sub(r'[\ud800-\udfff]', '', ssml_string)
        ssml_string = ssml_string.encode('utf-8').decode('utf-8')
        print(ssml_string)
        # Synthesize the SSML
        result = synthesizer.speak_ssml_async(ssml_string).get()

        # Check the result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text.")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech synthesis canceled: {cancellation_details.reason}")
    except UnicodeEncodeError as e:
        print(f"Encoding error: {e}")

# Get user input
<<<<<<< HEAD
user_input = input("Enter text in English and Vietnamese: ")
synthesize_multilingual_text(user_input)
=======
user_input = "Tư vấn bất động sản là một lĩnh vực đầy thách thức nhưng cũng rất hấp dẫn. Các chuyên gia tư vấn bất động sản không chỉ giúp khách hàng tìm kiếm và mua bán nhà đất mà còn cung cấp các dịch vụ tư vấn về đầu tư, pháp lý và quản lý tài sản. Họ cần có kiến thức sâu rộng về thị trường, khả năng phân tích và dự đoán xu hướng, cũng như kỹ năng giao tiếp và đàm phán xuất sắc. Một tư vấn viên giỏi sẽ giúp khách hàng đưa ra những quyết định thông minh, tối ưu hóa lợi nhuận và giảm thiểu rủi ro. Trong bối cảnh thị trường bất động sản luôn biến động, vai trò của các chuyên gia tư vấn càng trở nên quan trọng hơn bao giờ hết. Họ không chỉ là người hướng dẫn mà còn là người bạn đồng hành đáng tin cậy của khách hàng trên con đường đầu tư và phát triển tài sản."
synthesize_multilingual_text(user_input)
>>>>>>> a3cbcbf (Your commit message here)
