from eunjeon import Mecab
mecab = Mecab()
text = '가성비 좋은 사무용 컴퓨터 추천'
preprocessed = mecab.pos(text)
print(preprocessed)