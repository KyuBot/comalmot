from eunjeon import Mecab
import numpy as np
from sklearn.svm import SVC
from gensim.models import word2vec


train_data_list =  {
                    'encode' : ['판교에 오늘 피자 주문해줘','오늘 날짜에 호텔 예약 해줄레','모래 날짜에 판교 여행 정보 알려줘'],
                    'decode' : ['0','1','2']
                   }

embed_type = 'onehot'
encode_length = 8 #문장의 최대 길이 나머지는 Padding로 채움
vector_size = 50
label_size = 3 #Label의 수

def onehot_vectorize(bucket, x):
    #W2V의 Vocab의 해당 index값을 onehot으로 만듬
    np.put(bucket, model.wv.index2word.index(x),1)
    return bucket


def train_vector_model(str_buf):
    mecab = Mecab()
    str_buf = train_data_list['encode']
    #mecab로 POS Tagging
    pos1 = mecab.pos(''.join(str_buf))
    #문장별로 list로 나눔 마침표등이 존재시 줄바꾸기 (문장이길경우)
    pos2 = ' '.join(list(map(lambda x : '\n' if x[1] in ['SF'] else x[0], pos1))).split('\n')
    #단어구성을 위한 형태소단위 문장 쪼개기 
    morphs = list(map(lambda x : mecab.morphs(x) , pos2))
    model = word2vec.Word2Vec(size=vector_size, window=2, min_count=1)
    model.build_vocab(morphs)
    model.train(morphs,total_examples=model.corpus_count,epochs=model.iter)
    return model
# W2V Vector 모델 생성
model = train_vector_model(train_data_list)
print(model)
print(model.wv.index2word) #Word List를 구함


def embed(data) : 
    mecab = Mecab()
    inputs = []
#   labels = []
    for encode_raw in data['encode'] : 
        encode_raw = mecab.morphs(encode_raw)
        encode_raw = list(map(lambda x : encode_raw[x] if x < len(encode_raw) else '#', range(encode_length)))
        if(embed_type == 'onehot') :
            bucket = np.zeros(vector_size, dtype=float).copy()
            input = np.array(list(map(lambda x : onehot_vectorize(bucket, x) if x in model.wv.index2word else np.zeros(vector_size,dtype=float) , encode_raw)))
        inputs.append(input.flatten())
        print(encode_raw)
#     for decode_raw in data['decode']: 
#         label = np.zeros(label_size, dtype=float)
#         np.put(label, decode_raw, 1)
#         labels.append(label)
    return inputs #labels

#X, y = embed(train_data_list) #Encode와 Decode Data를 X와 y값에 Vector값을 담음
X = [embed(train_data_list)] #Encode와 Decode Data를 X와 y값에 Vector값을 담음
y = [train_data_list['decode']]
print(X)
print(y)


clf = SVC()
clf.fit(X, y) 
SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
    decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
    max_iter=-1, probability=False, random_state=None, shrinking=True,
    tol=0.001, verbose=False)
# print(clf.predict([[2, 2]]))
print(clf.predict(X[0]))