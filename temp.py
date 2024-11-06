# Định nghĩa hàm apply_stemming để áp dụng quá trình stemming cho văn bản
def apply_stemming(text):
    ps = PorterStemmer()
    words = word_tokenize(text)  # Tách văn bản thành danh sách các từ
    stemmed_words = [ps.stem(word) for word in words]  # Áp dụng stemming cho từng từ trong danh sách
    return ' '.join(stemmed_words)  # Kết hợp các từ sau khi stemming thành một chuỗi văn bản

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

# Hàm lemmatization
def lemmatize_text(text):
    # Khởi tạo WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()

    # Tách từ
    tokens = word_tokenize(text)

    # Gắn thẻ từ loại
    tagged_tokens = nltk.pos_tag(tokens)

    # Lemmatization cho mỗi từ
    lemmatized_text = []
    for token, tag in tagged_tokens:
        wordnet_pos = get_wordnet_pos(tag) or wordnet.NOUN
        lemmatized_text.append(lemmatizer.lemmatize(token, wordnet_pos))

    # Ghép các từ lại thành chuỗi
    return ' '.join(lemmatized_text)
