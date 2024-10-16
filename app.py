# Import Library
import streamlit as st # user-friend app 
import azure.cognitiveservices.speech as speechsdk

# utilization
from dotenv import load_dotenv
import os # file
from vinorm import TTSnorm # mapping word by word
from langdetect import detect, DetectorFactory, LangDetectException # detect vi or en
import re # search


# Set a seed for consistent language detection results
DetectorFactory.seed = 0
load_dotenv()

# Set the key 
speech_key = os.getenv('SPEECH_KEY')
service_region = os.getenv('SERVICE_REGION')

# page title and set the language
st.set_page_config(page_title="Azure SST", page_icon="🗣️",initial_sidebar_state="auto",layout='centered')
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
default_lang="Vietnamese"
lang_codes = {'Arabic': 'ar-EG','Bahasa Indonesian': 'id-ID','Bengali': 'bn-IN',
            'Chinese Mandarin': 'zh-CN','Dutch': 'nl-NL','English': 'en-US','French': 'fr-FR',
            'German': 'de-DE','Hindi': 'hi-IN','Italian': 'it-IT','Japanese': 'ja-JP','Korean': 'ko-KR',
            'Russian': 'ru-RU','Spanish': 'es-ES','Telugu': 'te-IN', 'Vietnamese': 'vi-VN'}

# selected box
with st.sidebar:
    option = st.selectbox('Select Option',('Speech-to-Text','Text-to-Speech'))
    lang=st.selectbox('Choose the language',list(lang_codes.keys()), index=5)     
    lang_code=lang_codes[lang]

    # check option
    if(option=="Speech-to-Text"): 
        req_type='stt'
    else: 
        req_type='tts'

    st.markdown("[Source Code](https://github.com/Sgvkamalakar/Azure_AI_Speech_Services)")
    st.markdown("[Explore my Codes](https://github.com/sgvkamalakar)")
    st.markdown("[Connect with me on LinkedIn](https://www.linkedin.com/in/sgvkamlakar)")
    
if req_type=="stt":
    icon='🗣️'
else:
    icon='📝'     

st.title(f"{option} with Azure AI"+icon)

def text_to_speech(text,lang_code):
    try:
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

        # Set the voice for TTS
        # if lang_code == 'vi-VN':
        #     speech_config.speech_synthesis_voice_name = 'vi-VN-HoaiMyNeural'
        # speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoMultilingualNeural"

        # speech_config.speech_synthesis_language=lang_code
        audio_output_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config,audio_config=audio_output_config)
        # result = speech_synthesizer.speak_text_async(text).get()


        # Initialize SSML string
        ssml_string = "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>"

        # Split the input into words for better language detection
        words = text.split()
        current_language = None
        phrase = ""

        for word in words:
            # Detect the language of the current word
            if word.isdigit():
                word = TTSnorm(word)
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

                # if current_language == 'vi':
                #     ssml_string += f"<voice name='zh-CN-XiaoxiaoMultilingualNeural'>{phrase.strip()}</voice>"
                # else:
                #     ssml_string += f"<voice name='zh-CN-XiaoxiaoMultilingualNeural'>{phrase.strip()}</voice>"
                
                # Reset for the new language
                phrase = word
                current_language = language
            else:
                phrase += " " + word

        # # Add the last phrase to SSML
        if current_language == 'vi':
            ssml_string += f"<voice name='vi-VN-HoaiMyNeural'>{phrase.strip()}</voice>"
        else:
            ssml_string += f"<voice name='en-US-AvaMultilingualNeural'>{phrase.strip()}</voice>"

        # # Add the last phrase to SSML
        # if current_language == 'vi':
        #     ssml_string += f"<voice name='zh-CN-XiaoxiaoMultilingualNeural'>{phrase.strip()}</voice>"
        # else:
        #     ssml_string += f"<voice name='zh-CN-XiaoxiaoMultilingualNeural'>{phrase.strip()}</voice>"

        ssml_string += "</speak>"
        print(ssml_string)
        with st.spinner("Speaking 🗣️..."):
            try:
                # Ensure the SSML string is properly encoded
                ssml_string = re.sub(r'[\ud800-\udfff]', '', ssml_string)
                ssml_string = ssml_string.encode('utf-8').decode('utf-8')
                print(ssml_string)
                # Synthesize the SSML
                result = speech_synthesizer.speak_ssml_async(ssml_string).get()

                # Check the result
                if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                    print("Speech synthesized for text.")
                elif result.reason == speechsdk.ResultReason.Canceled:
                    cancellation_details = result.cancellation_details
                    print(f"Speech synthesis canceled: {cancellation_details.reason}")
            except UnicodeEncodeError as e:
                print(f"Encoding error: {e}")

            # with st.spinner("Speaking 🗣️..."):
            #     result = speech_synthesizer.speak_text_async(text).get()
            #     if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            #         st.success("Synthesized Speech !")
            #     elif result.reason == speechsdk.ResultReason.Canceled:
            #         cancellation_details = result.cancellation_details
            #         st.error("Speech synthesis canceled due to ⚠{}".format(cancellation_details.reason))
            #         if cancellation_details.reason == speechsdk.CancellationReason.Error:
            #             if cancellation_details.error_details:
            #                 st.error("Error details: {}".format(cancellation_details.error_details))
    except Exception as e:
        st.error(f"An error occurred: {e}")                    

def transcribe_real_time_audio(lang_code):
    st.info("Speak into your microphone 🗣️...", icon="💡")
    try:
        speech_config.speech_recognition_language=lang_code
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,audio_config=audio_config)
        with st.spinner("Listening🧏🏻..."):
            result = speech_recognizer.recognize_once_async().get()
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                st.subheader("Transcription")
                st.success("{}".format(result.text))
                if lang_code == 'vi-VN':
                    speech_config.speech_synthesis_voice_name = 'vi-VN-HoaiMyNeural'
                # speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoMultilingualNeural"
                speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
                result = speech_synthesizer.speak_text_async(result.text).get()
            elif result.reason == speechsdk.ResultReason.NoMatch:
                st.error("No speech could be recognized")
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                st.error("Speech Recognition canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    st.error("Error details: {}".format(cancellation_details.error_details))
                    
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

if req_type=="stt":
    st.info("Speak in "+lang)
    if st.button("Start Transcription"):
        transcribe_real_time_audio(lang_code)
else:
    st.info("Type text in "+lang)
    text = st.text_area("Enter text for Text-to-Speech")
    if st.button("Generate Speech"):
        if text.strip()=="":
            st.error('Dont leave it empty😪! Enter text 😁')
        else:  
            text_to_speech(text,lang_code)
            
footer = """<style>
a:link , a:visited{
    color: #00aadd;
    background-color: transparent;
}

a:hover, a:active {
    color: red;
    background-color: transparent;
    text-decoration: underline;
}

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color:black;
    color: white;
    text-align: center;
    padding: 10px;  /* Added padding for better appearance */
}

.footer p {
    margin-bottom: 5px;  /* Adjusted margin for better spacing */
}

.footer a {
    text-decoration: none;
}
.red-heart {
    color: red;  /* Set the color of the heart emoji to red */
}
.footer a:hover {
    text-decoration: underline;
}
</style>
<div class="footer">
    <p>Developed with <span class="red-heart">❤</span> using <a href="https://speech.microsoft.com/" target="_blank">Azure Speech Services</a>  by Hang Tai</p>
</div>
"""

st.markdown(footer, unsafe_allow_html=True)
