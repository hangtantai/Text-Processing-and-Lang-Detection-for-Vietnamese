class SSMLTagger:
    ssml_template = ('<speak xmlns="http://www.w3.org/2001/10/synthesis"\n'
                     'xmlns:mstts="https://www.w3.org/2001/mstts"\n'
                     'xmlns:emo="http://www.w3.org/2009/10/emotionml"\n'
                     'version="1.0"\n'
                     'xml:lang="en-GB">\n')

    def __init__(self):
        # Khởi tạo biến instance từ biến tĩnh
        self.ssml = self.ssml_template
        self.processed_words = set()  # Thêm thuộc tính để theo dõi các từ đã được xử lý

    # <voice> tùy chỉnh được
    def open_voice(self, name="en-GB-AdaMultilingualNeural", effect=None):
        self.ssml += f'<voice name="{name}"'
        if effect:
            self.ssml += f' effect="{effect}"'
        self.ssml += '>'  # Đóng thẻ mở
        return self

    def close_voice(self):
        self.ssml += '</voice>'  # Đóng thẻ voice
        return self


    # <break>
    def add_break(self, time=None, strength=None):
        if time:
            self.ssml += f'<break time="{time}" />'
        elif strength:
            self.ssml += f'<break strength="{strength}" />'
        return self

    # <emphasis>
    def add_emphasis(self, content, level="moderate"):
        self.ssml += f'<emphasis level="{level}">{content}</emphasis>'
        return self

    # <lang>
    def add_lang(self, lang_code, content):
        self.ssml += f'<lang xml:lang="{lang_code}">{content}</lang>'
        return self

    # <lexicon>
    def add_lexicon(self, uri):
        self.ssml += f'<lexicon uri="{uri}"/>'
        return self


    # <mstts:audioduration> : giới hạn độ dài âm thanh
    # def add_audioduration(self, value):
    #     self.ssml += f'<mstts:audioduration value="{value}"/>'
    #     return self

    # <mstts:embedding>
    def add_embedding(self, speakerProfileId):
        self.ssml += f'<mstts:ttsembedding speakerProfileId="{speakerProfileId}"></mstts:ttsembedding>'
        return self

    # <mstts:express-as>
    def add_express_as(self, style, styledegree=None, role=None):
        self.ssml += f'<mstts:express-as style="{style}"'
        if styledegree:
            self.ssml += f' styledegree="{styledegree}"'
        if role:
            self.ssml += f' role="{role}"'
        self.ssml += f'></mstts:express-as>'
        return self

    # <mstts:silence> : time im lặng
    def add_silence(self, silence_type, value):
        self.ssml += f'<mstts:silence type="{silence_type}" value="{value}"/>'
        return self

    # <mstts:viseme> : biểu cảm
    # def add_viseme(self, viseme_type):
    #     self.ssml += f'<mstts:viseme type="{viseme_type}"/>'
    #     return self

    # <p> và <s>
    def add_paragraph(self, content):
        self.ssml += f'<p>{content}</p>'
        return self

    def add_sentence(self, content):
        self.ssml += f'<s>{content}</s>'
        return self

    # ví dụ <p>
    #             <s>Xin chào</s>
    #             <s>Hôm nay, tôi sẽ nói về tầm quan trọng của việc học</s>
    #         </p>

    # T<sub> : định nghĩa tử khác dễ phát âm hơn
    def add_sub(self, alias, content):
        self.ssml += f'<sub alias="{alias}">{content}</sub>'
        return self

    # phoneme> : phát âm chính xác
    def add_phoneme(self, content, ph=None, alphabet="ipa"):
        if ph:
            self.ssml += f'<phoneme alphabet="{alphabet}" ph="{ph}">{content}</phoneme>'
        return self

    # <prosody> : điểu chỉnh pitch và rate
    def add_prosody(self, content, rate="medium", pitch="medium", volume="medium"):
        self.ssml += f'<prosody rate="{rate}" pitch="{pitch}" volume="{volume}">{content}</prosody>'
        return self

    # <say-as>
    def add_say_as(self, content, interpret_as=None, format=None, detail=None):
        self.ssml += f'<say-as'
        if interpret_as:
            self.ssml += f' interpret-as="{interpret_as}"'
        if format:
            self.ssml += f' format="{format}"'
        if detail:
            self.ssml += f' detail="{detail}"'
        self.ssml += f'>{content}</say-as>'
        return self

    # cần cover các trường hợp sau:
    # characters: Phát âm từng ký tự.
    # digits: Phát âm từng chữ số.
    # date: Phát âm theo định dạng ngày tháng.
    # time: Phát âm theo định dạng thời gian.
    # telephone: Phát âm theo định dạng số điện thoại.
    # email


    def build(self):
        return self.ssml + '</speak>'
