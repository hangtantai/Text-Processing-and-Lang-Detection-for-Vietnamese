import re
import regex as rex
import time


class TextClassifier:
    def __init__(self):
        self.patterns = {
            ### Time
            'time': [
                re.compile(r"(?i)\b(?:2[0-3]|[01]?[0-9]):[0-5][0-9]:[0-5][0-9]\b(\s?-?)", re.IGNORECASE | re.VERBOSE)  ,
                re.compile(r"(?i)\b\d{1,2}\s?[hg]\s?\d{1,2}\s?[ap]?[m]?\b(\s?-?)", re.IGNORECASE | re.VERBOSE)  ,
                re.compile(r"(?i)\b\d{1,2}\s?[hg]\b(\s?-?)", re.IGNORECASE | re.VERBOSE)  ,
                re.compile(r"(?i)\b(?:2[0-4]|[01]?[1-9])\s?[:hg]\s?[0-5][0-9]\s?[ap]?[m]?\b(\s?-?)", re.IGNORECASE | re.VERBOSE)  ,
            ],

            ### Month
            'month': [
                re.compile(r"(?i)\btháng\s?(0?[1-9]|1[0-2])\b", re.IGNORECASE | re.VERBOSE),
                re.compile(r"(?i)\btháng\s?(0?[1-9]|1[0-2])\s?[\/.-]\s?\d{4}\b", re.IGNORECASE | re.VERBOSE),
            ],

            ### DATES
            'date': [
                re.compile(r"\b[0-3]?[0-9]\s?-\s?[01]?\d\s?-\s?[12]\d{3}\b", re.IGNORECASE | re.VERBOSE),
                re.compile(r"\b[0-3]?[0-9]\s?\.\s?[01]?\d\s?\.\s?[12]\d{3}\b", re.IGNORECASE | re.VERBOSE),
                re.compile(r"\s+([ivx]+)[\s\-\/]([12]\d{3})\b", re.IGNORECASE | re.VERBOSE),
                re.compile(r"\b(ngày|sáng|trưa|chiều|tối|đêm|hôm|nay|hai|ba|tư|năm|sáu|bảy|nhật|qua|lúc|từ|đến)\s+[0-3]?[0-9]\s?[\/.-]\s?[01]?\d\b", re.IGNORECASE | re.VERBOSE),
                re.compile(r"\b[0-3]?[0-9]\s?\/\s?[01]?\d\s?\/\s?\d{2}\b", re.IGNORECASE | re.VERBOSE)
            ],

            ### Email
            'email': re.compile(r"[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*"),

            ### Address
            'address': [
                re.compile(r"""(?i)\b(?:đường|số|số nhà|nhà|địa chỉ|tọa lạc|xã|thôn|ấp|khu phố|căn hộ|cư xá|Đ\/c)[\s:]\s?[^\s]*\d[^\s]*(?:\b|$)""", re.VERBOSE),
                re.compile(r"\d{1,5}(\/\d{1,5})*\s\w+(\s\w+)*")
            ],
            ### Phone Number
            'phone': [
                re.compile(r"(?:[^(\w|\d|\.)]|^)((\+\d{1,3})|0)[-\s.]?\d{1,3}[-\s.]?\d{3}[-\s.]?\d{4}\b", re.IGNORECASE | re.VERBOSE),
                re.compile(r"(?:[^(\w|\d|\.)]|^)((\+\d{1,3})|0)[-\s.]?\d{2,3}[-\s.]?\d{2}[- .]?\d{2}[- .]?\d{2}\b", re.IGNORECASE | re.VERBOSE),
                re.compile(r"(?:[^(\w|\d|\.)]|^)((\+\d{1,3})|0)[-\s.]?\d{1,3}[-\s.]?\d{1,2}[-\s.]?\d{2,3}[-\s.]?\d{3}\b", re.IGNORECASE | re.VERBOSE),
                re.compile(r"b1[89]00[\s\.]?[\d\s\.]{4,8}\b", re.IGNORECASE | re.VERBOSE),
                re.compile(r"\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b"),  
                re.compile(r"\b\d{4}[-.\s]??\d{3}[-.\s]??\d{3}\b"), 
            ],

            ### Normal Number
            'normal number': [
                re.compile(r"(?i)(\s|^)\d+(\.\d{3})+(,\d+)?(:?\b|$)", re.IGNORECASE | re.VERBOSE),
                re.compile(r"(?i)(\s|^)\d+(,\d{3})+(\.\d+)?(:?\b|$)", re.IGNORECASE | re.VERBOSE),
                re.compile(r"(?i)(\s|^|\s-)\d+(,\d+)(:?\b|$)", re.IGNORECASE | re.VERBOSE),
                re.compile(r"(?i)(\s|^|\s-)\d+(\.\d+)?(:?\b|$)", re.IGNORECASE | re.VERBOSE)
            ],

            ### Roman Symbol
            'roman symbol': [
                re.compile(r"(?i)(?:\b|^)[IVXLCDM]{1,7}(?:\b|$)", re.IGNORECASE | re.VERBOSE),  
                re.compile(r"(?i)(?:\b|^)[IVXLCDM]{1,7}\s+(?:thứ|lần|kỷ|kỉ|kì|kỳ|khóa)(?:\b|$)", re.IGNORECASE | re.VERBOSE)  
            ],

            ### Website
            'website': [
                re.compile(r"(?i)\b(https?:\/\/|ftp:\/\/|www\.|[^\s:=]+@www\.)?((\w+)\.)+(?:com|au\.uk|co\.in|net|org|info|coop|int|co\.uk|org\.uk|ac\.uk|uk)([\.\/][^\s]*)*([^(w|\d)]|$)", re.IGNORECASE | re.VERBOSE),
                re.compile(r"(?i)\b((https?:\/\/|ftp:\/\/|sftp:\/\/|www\.|[^\s:=]+@www\.))(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\d]+-[a-z\d])*[a-z\d]+)(?:\.(?:[a-z\d]+-?)*[a-z\d]+)*(?:\.(?:[a-z]{2,})))(?::\d{2,5})?(?:\/[^\s]*)?([^(w|\d)]|$)", re.IGNORECASE | re.VERBOSE)
            ],



            # # ### Measurement
            # 'measurement': [
            #      # Measurement of Vietnam
            #     rex.compile(r"(?i)\b(\d+(?:\.\d{3})+(?:,\d+)?)\s?(việt nam đồng|đồng|vnd|vnđ|đồng việt nam)(?:\b|$)(\s?-?)", re.IGNORECASE | re.VERBOSE),
            #     rex.compile(r"(?i)\b(\d+(?:,\d{3})+(?:\.\d+)?)\s?(việt nam đồng|đồng|vnd|vnđ|đồng việt nam)(?:\b|$)(\s?-?)", re.IGNORECASE | re.VERBOSE),
            #     rex.compile(r"(?i)\b(\d+(?:,\d+))\s?(việt nam đồng|đồng|vnd|vnđ|đồng việt nam)(?:\b|$)(\s?-?)", re.IGNORECASE | re.VERBOSE),
            #     rex.compile(r"(?i)\b(\d+(?:\.\d+)?)\s?(việt nam đồng|đồng|vnd|vnđ|đồng việt nam)(?:\b|$)(\s?-?)", re.IGNORECASE | re.VERBOSE),
            #     rex.compile(r"(?i)\b(\d+(?:\.\d{3})+(?:,\d+)?)\s?([°|\p{Alphabetic}]+[2|3]?)(?:\/(\p{Alphabetic}+[2|3]?))?(?:\b|$)(\s?-?)", re.IGNORECASE | re.VERBOSE),
            #     rex.compile(r"(?i)\b(\d+(?:,\d{3})+(?:\.\d+)?)\s?([°|\p{Alphabetic}]+[2|3]?)(?:\/(\p{Alphabetic}+[2|3]?))?(?:\b|$)(\s?-?)", re.IGNORECASE | re.VERBOSE),
            #     rex.compile(r"(?i)\b(\d+(?:,\d+))\s?([°|\p{Alphabetic}]+[2|3]?)(?:\/(\p{Alphabetic}+[2|3]?))?(?:\b|$)(\s?-?)", re.IGNORECASE | re.VERBOSE),
            #     rex.compile(r"(?i)\b(\d+(?:\.\d+)?)\s?([°|\p{Alphabetic}]+[2|3]?)(?:\/(\p{Alphabetic}+[2|3]?))?(?:\b|$)(\s?-?)", re.IGNORECASE | re.VERBOSE),


            #     # Measurement of foreign country
            #     rex.compile(r"(?i)(?:\b|^)(\d+(?:\.\d{3})+(?:,\d+)?)\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)(\s-|$|-|\s)", re.IGNORECASE | re.VERBOSE),
            #     rex.compile(r"(?i)(?:\b|^)(\d+(?:,\d{3})+(?:\.\d+)?)\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)(\s-|$|-|\s)", re.IGNORECASE | re.VERBOSE),
            #     rex.compile(r"(?i)(?:\b|^)(\d+(?:,\d+))\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)(\s-|$|-|\s)", re.IGNORECASE | re.VERBOSE),
            #     rex.compile(r"(?i)(?:\b|^)(\d+(?:\.\d+)?)\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)(\s-|$|-|\s)", re.IGNORECASE | re.VERBOSE),
            #     rex.compile(r"(?i)(?:\b|^)(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)?\s?(\d+(?:\.\d{3})+(?:,\d+)?)(\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω))?(\s-|$|-|\s)", re.IGNORECASE | re.VERBOSE),
            #     rex.compile(r"(?i)(?:\b|^)(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)?\s?(\d+(?:,\d{3})+(?:\.\d+)?)(\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω))?(\s-|$|-|\s)", re.IGNORECASE | re.VERBOSE),
            #     rex.compile(r"(?i)(?:\b|^)(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)?\s?(\d+(?:,\d+))(\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω))?(\s-|$|-|\s)", re.IGNORECASE | re.VERBOSE),
            #     rex.compile(r"(?i)(?:\b|^)(\%|\$|฿|₱|₭|₩|¥|€|£|Ω)?\s?(\d+(?:\.\d+)?)(\s?(\%|\$|฿|₱|₭|₩|¥|€|£|Ω))?(\s-|$|-|\s)", re.IGNORECASE | re.VERBOSE)
            # ],

            ### Vietnamsese word
            'vietnamese_word': re.compile(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹ]')
        }

    def classify(self, text):
        for category, patterns in self.patterns.items():
            if isinstance(patterns, list):
                for pattern in patterns:
                    if pattern.search(text.lower()):
                        return category
            else:
                if patterns.search(text.lower()):
                    return category
        return 'unknown'
    

# # Example usage
# start_time = time.time()
# classifier = TextClassifier()
# print(classifier.classify("hòa"))  # vietnamese_word
# print(classifier.classify("example@example.com"))  # email
# print(classifier.classify("12-12-2020"))  # date
# print(classifier.classify("123/13/27/14 đường Mã Lò"))  # address
# print(classifier.classify("123-456-7890"))  # phone
# print(classifier.classify("123.55.6"))  # normal_number
# print(classifier.classify("XII"))  # roman
# print(classifier.classify("12:30 PM"))  # time
# print(classifier.classify("tháng 12/2024"))  # month
# print(classifier.classify("random text"))  # unknown
# print(classifier.classify("The Vitas"))
# end_time = time.time()
# print(f"Response time {end_time-start_time}")