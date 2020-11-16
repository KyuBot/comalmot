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

model = word2vec.Word2Vec(size=50, window=2, min_count=1, iter=100)
model.build_vocab(train_data)
model.train(train_data,epochs=model.epochs ,total_examples=model.corpus_count)
print("model check : {0}".format(model))

import os  
file_path = './model'
if not os.path.exists(file_path):
    os.makedirs(file_path)
model.save(file_path + "/w2v.bin")
model = word2vec.Word2Vec.load("./model/w2v.bin")
print("model load check : {0}".format(model))


print(model['AI'])

result1 = model.most_similar(positive='누구', negative='', topn=10)
print(result1)

from sklearn.manifold import TSNE
import pandas as pd
import matplotlib 
import matplotlib.pyplot as plt

# font_name = matplotlib.font_manager.FontProperties(
#                 fname="/usr/share/fonts/truetype/nanum/NanumGothic.ttf"  # 한글 폰트 위치를 넣어주세요
#             ).get_name()
vocab = model.wv.index2word
X = model[vocab]
# matplotlib.rc('font', family=font_name)
tsne = TSNE(n_components=2)
X_tsne = tsne.fit_transform(X) #t-분포 확률적 임베딩(t-SNE)은 데이터의 차원 축소에 사용
df = pd.concat([pd.DataFrame(X_tsne),
                pd.Series(vocab)],
               axis=1)

df.columns = ['x', 'y', 'word']
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
print(df)
ax.scatter(df['x'], df['y'])
ax.set_xlim(df['x'].max(), df['x'].min())
ax.set_ylim(df['y'].max(), df['y'].min())
for i, txt in enumerate(df['word']):
    ax.annotate(txt, (df['x'].iloc[i], df['y'].iloc[i]))
plt.show()