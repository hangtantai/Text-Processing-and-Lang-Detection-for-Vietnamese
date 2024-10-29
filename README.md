# Text-Processing-and-Lang-Detection-for-Vietnamese
This repository provides tools for text processing and language detection specifically tailored for Vietnamese. The project leverages the [underthesea](https://github.com/undertheseanlp/underthesea) library for **comprehensive text processing tasks** and [fastText](https://fasttext.cc/) for **efficient language detection**.

# Introduction about Underthesea
Underthesea is a powerful NLP toolkit for Vietnamese language processing. It offers a wide range of functionalities but We just use:
- **Sentence Segmentation**: Breaking down text into individual sentences.
- **Word Tokenization**: Splitting sentences into words.
- **POS Tagging**: Assigning parts of speech to each word. [DOCUMENT](https://github.com/undertheseanlp/underthesea/wiki/M%C3%B4-t%E1%BA%A3-d%E1%BB%AF-li%E1%BB%87u-b%C3%A0i-to%C3%A1n-POS-Tag)
- **Named Entity Recognition (NER)**: Identifying and classifying entities in text.

**Note**: Underthesea has compatibility issues with Python version 3.12 and above. Before using it, please set up Python version 3.11 or an older version.
```bash
    pip install underthesea
```
# Introduction about Fasttext
FastText is an open-source, free, lightweight library that allows users to learn text representations and text classifiers. It is particularly known for its efficiency and accuracy in language detection tasks. 

We use Language Identification of library.

Use it in Window:
```bash
    curl -O https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
```

Use it in Linux:
```bash
    wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
```
