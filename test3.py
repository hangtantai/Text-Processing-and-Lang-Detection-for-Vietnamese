import re

# Original SSML string
ssml_string = "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'><voice name='vi-VN-HoaiMyNeural'>tư.  vấn.  bất.  động.  sản.  là.  một.  lĩnh.  vực.  đầy.  thách.  thức.  nhưng.  cũng.  rất.  hấp.  dẫn ..  mười lăm triệu sáu trăm tám mươi chín nghìn bốn trăm chín mươi.  năm.</voice></speak>"

# Extract content within the <voice> tag
voice_content = re.search(r'<voice name=\'vi-VN-HoaiMyNeural\'>(.*?)</voice>', ssml_string).group(1)

# Remove single periods
voice_content = re.sub(r'(?<!\.)\.(?!\.)', '', voice_content)

# Replace sequences of two or more periods with a single period
voice_content = re.sub(r'\.{2,}', '.', voice_content)

# Replace the original content within the <voice> tag with the transformed content
ssml_string = re.sub(r'(<voice name=\'vi-VN-HoaiMyNeural\'>).*?(</voice>)', r'\1' + voice_content + r'\2', ssml_string)

print(ssml_string)