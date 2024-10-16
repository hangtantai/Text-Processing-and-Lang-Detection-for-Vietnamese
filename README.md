# TTS-and-STT
I developed a program within the Streamlit environment that leverages Azure’s Text-to-Speech (TTS) and Speech-to-Text (STT) services. This application provides a user-friendly interface for real-time audio transcription and speech synthesis, utilizing Azure’s powerful AI capabilities.

# Clone code and set up
1 **Clone code from my github:**
```bash
    git clone https://github.com/hangtantai/TTS-and-STT.git
```
2. **Note: Tnorm library haven't supported in Window system, change Linux system or MacOS system, In terminal, you type like that:**
```bash
    wsl -d ubuntu
```
3. **Set up necessary lirbary**
```bash
    pip install -r requirements.txt
```
# Set up Azure Services
Tutorial: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-speech-to-text?tabs=windows%2Cterminal&pivots=programming-language-python

# Run program
```bash
    streamlit run app.py
