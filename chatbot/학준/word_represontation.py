# One Hot Vector를 통한 출력
from eunjeon import Mecab

ona_data = [ 
                 [ '안녕', '만나서 반가워'],
                 ['넌 누구니', ' 나는 AI봇이란다.'],
                 ['피자 주문 할게', '음료도 주문해줘'],
                 ['음료는 뭘로', '콜라로 해줘']
]

mecab = Mecab()
train_Data = list(map(lambda x : mecab.morphs(' '.join(x)), ona_data))
# .morphs() 문장을 형태소 단위로 끊어준다.
import itertools

train_data = list(itertools.chain.from_iterable(train_Data))
print(list(train_data))


import numpy as np

bucket = np.zeros(len(train_data), dtype = np.float)
for word in train_data :
    bucket_temp = bucket.copy()
    np.put(bucket_temp, train_data.index(word),  1)
    #print(bucket_temp)

# Word to Vector (By Gensim) 
# W2V를 통해 출력해보자
from gensim.models import word2vec

train_data = [train_data]
print(train_data)

model = word2vec.Word2Vec(size=50, window=2, min_count=1)
model.build_vocab(train_data)
model.train(train_data)
print("model check : {0}".format(model))