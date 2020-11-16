from gensim.models import Word2Vec
import matplotlib.pyplot as plt
from eunjeon import Mecab
# 단어와 2차원 X축의 값, Y축의 값을 입력받아 2차원 그래프를 그린다
def plot_2d_graph(vocabs, xs, ys):
    plt.figure(figsize=(8 ,6))
    plt.scatter(xs, ys, marker = 'o')
    for i, v in enumerate(vocabs):
        plt.annotate(v, xy=(xs[i], ys[i]))

sentences = [
                 [ '안녕', '만나서 반가워'],
                 ['넌 누구니', ' 나는 AI봇이란다.'],
                 ['피자 주문 할게', '음료도 주문해줘'],
                 ['음료는 뭘로', '콜라로 해줘']
            ]

mecab = Mecab()
sentences = list(map(lambda x : mecab.morphs(' '.join(x)), sentences))

# 문장을 이용하여 단어와 벡터를 생성한다.
model = Word2Vec(sentences, size=50, window=2, min_count=1, iter=100)

# 단어벡터를 구한다.
word_vectors = model.wv

vocabs            = word_vectors.vocab.keys()
word_vectors_list = [word_vectors[v] for v in vocabs]

# 단어간 유사도를 확인하다
print(word_vectors.similarity(w1='피자', w2='음료'))

from sklearn.decomposition import PCA
pca = PCA(n_components=2)
xys = pca.fit_transform(word_vectors_list)
xs = xys[:,0]
ys = xys[:,1]

plot_2d_graph(vocabs, xs, ys)