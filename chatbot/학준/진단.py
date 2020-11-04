
import requests
import tensorflow as tf
import numpy as np
import os
from matplotlib.image import imread, imsave 
import matplotlib.pyplot as plt  
import pandas as pd
from eunjeon import Mecab
from gensim.models import word2vec

###Parameters
vector_size = 100
encode_length = 90
label_size = 9
embed_type = "onehot" #onehot or w2v
# Choose single test
# filter_type = "single"
# filter_number = 32
# filter_size = 2

# Choose multi test
filter_type = "multi"
filter_sizes = [2,3,4,2,3,4,2,3,4]
num_filters = len(filter_sizes)

train_data_list =  {
                'encode' : [
                    # 아예 전원이 안 켜지는 경우(1)
                    '컴퓨터 전원이 안켜져',
                    '노트북 전원이 안켜져',
                    '컴퓨터가 안되',
                    '노트북이 안되',
                    '컴퓨터가 안켜져',
                    '노트북이 안켜져',
                    '전원이 안켜짐',
                    '전원 문제',
                    '불이 안켜짐',
                    '전원 버튼 눌러도 반응이 없음',
                    # 불은 들어오는 경우(2)
                    '컴퓨터 화면이 안켜져',
                    '노트북 화면이 안켜져',
                    '모니터에 불이 안들어와',
                    '전원은 켰는데 화면에 불이 안들어와',
                    '전원은 들어오는데 화면이 안켜져요',
                    '부팅이 되다 말아요',
                    '부팅이 되다 꺼죠요',
                    '불은 들어오는데 화면이 안나와',
                    '전원은 있는데 화면이 안켜짐',
                    '전원은 들어오는데 모니터가 먹통',
                    # 커졌다가 꺼지는 경우(3)
                    '컴퓨터를 켰는데 다시 꺼져요',
                    '노트북을 켰는데 다시 꺼져요',
                    '켜졌다가 꺼저요',
                    '켰는데 다시 꺼저요',
                    '전원이 들어왔다가 다시 꺼저요',
                    '컴퓨터가 계속 재부팅',
                    '노특북 계속 재부팅',
                    '무한 재부팅',
                    '계속 꺼저요',
                    '전원이 나가요',
                    # 화면 상태가 이상한 경우(4)
                    '화면에 줄무늬가 생겨요',
                    '화면이 이상해요',
                    '화면이 깨져요',
                    '디스플레이가 이상해요',
                    '화면에 문제가 있어요',
                    '화면 색이 이상해요',
                    '화면이 겹쳐요',
                    '그래픽카드가 이상해요',
                    '화면이 찌그러져요',
                    '화면 문제',
                    # 부팅이 안 되고 오류 메세지가 나오는 경우(5)
                    '부팅이 안되고 오류 메세지가 떠요',
                    '부팅할 때 에러 메세지',
                    'NTLDR is Missing, BOOTMGR is Missing, BOOTMGR is compressed',
                    '노트북 블루스크린 떳어요',
                    '컴퓨터 블루스크린 떳어요',
                    '부팅할 때 오류 메세지',
                    '부팅할 때 에러 메세지',
                    '컴퓨터 부팅하면 에러 메세지',
                    '노트북 부팅하면 에러 메세지',
                    '부팅하면 이상한 메세지',
                    # 인터넷 사용 불능(6)
                    '노특북에서 인터넷이 안되요',
                    '컴퓨터에서 인터넷이 안되요',
                    '인터넷이 안됨',
                    '인터넷 연결 하는 법',
                    '인터넷이 고장',
                    '인터넷이 갑자기 안되요',
                    '인터넷 사용하는법',
                    '인터넷이 끊김',
                    '인터넷 문제',
                    '인터넷이 갑자기 안되요',
                    # 주변기기 작동 불량(스피커,프린터,마우스,키보드)(7)
                    '노트북에서 스피커가 안되요',
                    '컴퓨터에서 스피커가 안되요',
                    '소리가 안나와',
                    '컴퓨터 소리 고장',
                    '노트북 소리 고장',
                    '스피커가 이상해',
                    '소리가 이상해',
                    '소리 문제 해결',
                    '스피커 고치는법',
                    '소리문제 고치는법',

                    '프린터기가 안되요',
                    '프린터 연결하는법',
                    '프린터 작동하는법',
                    '프린터가 고장남',
                    '프린터 문제',
                    '프린터 고치는법',
                    '컴퓨터 프린트 연결하는법',
                    '프린터 고장문제 해결',
                    '프린터가 갑자기 이상해요',
                    '프린터 연결',
                    # 속도 문제(11)
                    '노트북이 너무 느려졌어',
                    '컴퓨터가 너무 느려',
                    '컴퓨터 속도 빠르게 하는법',
                    '노트북 속도 빠르게 하는법',
                    '너무 느려요',
                    '속도 빠르게 하는법',
                    '갑자기 느려졌어요',
                    '속도 문제 해결',
                    '컴퓨터 빠르게 하는 법',
                    '노트북 빠르게 하는 법',
                    ],
                'decode' : ['0']*10 + ['1']*10 + ['2']*10 + ['3']*10 + ['4']*10 + ['5']*10 + ['6']*10 + ['7']*10 + ['8']*10
             }
train_data_list.get('encode')
train_data_list.get('encode')
print(len(train_data_list.get('encode')),len(train_data_list.get('decode')))

###Vector model
def train_vector_model(str_buf):

    mecab = Mecab()
    str_buf = train_data_list['encode']
    pos1 = mecab.pos(''.join(str_buf))
    # print(1,pos1)
    pos2 = ' '.join(list(map(lambda x : '\n' if x[1] in ['SF'] else x[0], pos1))).split('\n')
    # print(2,pos2)

    morphs=list()
    for word in pos1:
        morphs.append(word[0])
    morphs = [morphs]

    # morphs = list(map(lambda x : mecab.morphs(x) , pos2))
    # print(3,morphs)
    # print(4,str_buf)
    model = word2vec.Word2Vec(size=vector_size, window=2, min_count=1)
    model.build_vocab(morphs)
    model.train(morphs,epochs=model.epochs,total_examples=model.corpus_count)
    return model

model = train_vector_model(train_data_list)
print(model)


###Load Train Data
def load_csv(data_path):
    df_csv_read = pd.DataFrame(data_path)
    return df_csv_read


###Embed word to vector
def embed(data) : 
    mecab = Mecab()
    inputs = []
    labels = []
    for encode_raw in data['encode'] : 
        encode_raw = mecab.morphs(encode_raw)
        encode_raw = list(map(lambda x : encode_raw[x] if x < len(encode_raw) else '#', range(encode_length)))
        if(embed_type == 'onehot') :
            bucket = np.zeros(vector_size, dtype=float).copy()
            input = np.array(list(map(lambda x : onehot_vectorize(bucket, x) if x in model.wv.index2word else np.zeros(vector_size,dtype=float) , encode_raw)))
        else : 
            input = np.array(list(map(lambda x : model[x] if x in model.wv.index2word else np.zeros(vector_size,dtype=float) , encode_raw)))
        inputs.append(input.flatten())
        
    for decode_raw in data['decode']: 
        label = np.zeros(label_size, dtype=float)
        np.put(label, decode_raw, 1)
        labels.append(label)
    return inputs, labels

def onehot_vectorize(bucket, x):
    np.put(bucket, model.wv.index2word.index(x),1)
    return bucket

###Embed word to vector on predict step
def inference_embed(data) : 
    mecab = Mecab()
    encode_raw = mecab.morphs(data)
    encode_raw = list(map(lambda x : encode_raw[x] if x < len(encode_raw) else '#', range(encode_length)))
    if(embed_type == 'onehot') :
        bucket = np.zeros(vector_size, dtype=float).copy()
        input = np.array(list(map(lambda x : onehot_vectorize(bucket, x) if x in model.wv.index2word else np.zeros(vector_size,dtype=float) , encode_raw)))
    else : 
        input = np.array(list(map(lambda x : model[x] if x in model.wv.index2word else np.zeros(vector_size,dtype=float) , encode_raw)))
    return input

###get train and test data for feed on tensorflow session
def get_test_data():
    train_data, train_label = embed(load_csv(train_data_list))
    test_data, test_label = embed(load_csv(train_data_list))
    return train_label, test_label, train_data, test_data


###create graph with single filter size
def create_s_graph(train=True):
    # placeholder is used for feeding data.
    x = tf.placeholder("float", shape=[None, encode_length * vector_size], name = 'x') 
    y_target = tf.placeholder("float", shape=[None, label_size], name = 'y_target') 

    # reshape input data
    x_image = tf.reshape(x, [-1,encode_length,vector_size,1], name="x_image")
    
    # Build a convolutional layer and maxpooling with random initialization
    W_conv1 = tf.Variable(tf.truncated_normal([filter_size, filter_size, 1, filter_number], stddev=0.1), name="W_conv1") # W is [row, col, channel, feature]
    b_conv1 = tf.Variable(tf.zeros([filter_number]), name="b_conv1")
    h_conv1 = tf.nn.relu(tf.nn.conv2d(x_image, W_conv1, strides=[1, 1, 1, 1], padding='SAME') + b_conv1, name="h_conv1")
    h_pool1 = tf.nn.max_pool( h_conv1 , ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name = "h_pool1")
    
    # Build a fully connected layer
    h_pool2_flat = tf.reshape(h_pool1, [-1, int((encode_length/2)*(vector_size/2))*filter_number], name="h_pool2_flat")
    W_fc1 = tf.Variable(tf.truncated_normal([int((encode_length/2)*(vector_size/2))*filter_number, 256], stddev=0.1), name = 'W_fc1')
    b_fc1 = tf.Variable(tf.zeros([256]), name = 'b_fc1')
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1, name="h_fc1")
    
    keep_prob = 1.0
    if(train) : 
        # Dropout Layer
        keep_prob = tf.placeholder("float", name="keep_prob")
        h_fc1 = tf.nn.dropout(h_fc1, keep_prob, name="h_fc1_drop")
    
    # Build a fully connected layer with softmax 
    W_fc2 = tf.Variable(tf.truncated_normal([256, label_size], stddev=0.1), name = 'W_fc2')
    b_fc2 = tf.Variable(tf.zeros([label_size]), name = 'b_fc2')
    #y=tf.nn.softmax(tf.matmul(h_fc1, W_fc2) + b_fc2, name="y")
    y=tf.matmul(h_fc1, W_fc2) + b_fc2
    
    # define the Loss function
    #cross_entropy = -tf.reduce_sum(y_target*tf.log(y), name = 'cross_entropy')
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y, labels=y_target))
    
    # define optimization algorithm
    #train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_target, 1))
    # correct_prediction is list of boolean which is the result of comparing(model prediction , data)

    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float")) 
    # tf.cast() : changes true -> 1 / false -> 0
    # tf.reduce_mean() : calculate the mean
    
    return accuracy, x, y_target, keep_prob, train_step, y, cross_entropy, W_conv1
    
print("define cnn graph func")

###create graph with multi filter size
def create_m_graph(train=True):
    # placeholder is used for feeding data.
    x = tf.placeholder("float", shape=[None, encode_length * vector_size], name = 'x') 
    y_target = tf.placeholder("float", shape=[None, label_size], name = 'y_target') 

    # reshape input data
    x_image = tf.reshape(x, [-1,encode_length,vector_size,1], name="x_image")
    # Keeping track of l2 regularization loss (optional)
    l2_loss = tf.constant(0.0)
    
    pooled_outputs = []
    for i, filter_size in enumerate(filter_sizes):
        with tf.name_scope("conv-maxpool-%s" % filter_size):
            # Convolution Layer
            filter_shape = [filter_size, vector_size, 1, num_filters]
            W_conv1 = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1), name="W")
            b_conv1 = tf.Variable(tf.constant(0.1, shape=[num_filters]), name="b")
            
            conv = tf.nn.conv2d(
                x_image,
                W_conv1,
                strides=[1, 1, 1, 1],
                padding="VALID",
                name="conv")
            
            # Apply nonlinearity
            h = tf.nn.relu(tf.nn.bias_add(conv, b_conv1), name="relu")
            # Maxpooling over the outputs
            pooled = tf.nn.max_pool(
                h,
                ksize=[1, encode_length - filter_size + 1, 1, 1],
                strides=[1, 1, 1, 1],
                padding='VALID',
                name="pool")
            pooled_outputs.append(pooled)

    # Combine all the pooled features
    num_filters_total = num_filters * len(filter_sizes)
    h_pool = tf.concat(pooled_outputs, 3)
    h_pool_flat = tf.reshape(h_pool, [-1, num_filters_total])
 
    # Add dropout
    keep_prob = 1.0
    if(train) : 
        keep_prob = tf.placeholder("float", name="keep_prob")
        h_pool_flat = tf.nn.dropout(h_pool_flat, keep_prob)

    # Final (unnormalized) scores and predictions
    W_fc1 = tf.get_variable(
        "W_fc1",
        shape=[num_filters_total, label_size],
        initializer=tf.contrib.layers.xavier_initializer())
    b_fc1 = tf.Variable(tf.constant(0.1, shape=[label_size]), name="b")
    l2_loss += tf.nn.l2_loss(W_fc1)
    l2_loss += tf.nn.l2_loss(b_fc1)
    y = tf.nn.xw_plus_b(h_pool_flat, W_fc1, b_fc1, name="scores")
    predictions = tf.argmax(y, 1, name="predictions")

    # CalculateMean cross-entropy loss
    losses = tf.nn.softmax_cross_entropy_with_logits(logits=y, labels=y_target)
    cross_entropy = tf.reduce_mean(losses)

    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    
    # Accuracy
    correct_predictions = tf.equal(predictions, tf.argmax(y_target, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_predictions, "float"), name="accuracy")
    
    return accuracy, x, y_target, keep_prob, train_step, y, cross_entropy, W_conv1
    
print("define cnn graph func")


###visualize weight matrix function
def show_layer(weight_list) :
    if(filter_type == 'multi') : 
        show = np.array(weight_list).reshape(num_filters, filter_sizes[np.argmax(filter_sizes)], vector_size)
        for i, matrix in enumerate(show) :
            fig = plt.figure()
            plt.imshow(matrix)
        plt.show()
    else : 
        show = np.array(weight_list).reshape(32, 2, 2)
        for i, matrix in enumerate(show) :
            fig = plt.figure()
            plt.imshow(matrix)
        plt.show()


##run train
def run() : 
    try : 
        # get Data 
        labels_train, labels_test, data_filter_train, data_filter_test = get_test_data()
        # reset Graph
        # tf.reset_default_graph()   
 
        # Create Session
        sess = tf.Session(config=tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth =True)))  
        # create graph
        if(filter_type == 'single') :
            accuracy, x, y_target, keep_prob, train_step, y, cross_entropy, W_conv1 = create_s_graph(train=True)
        else :
            accuracy, x, y_target, keep_prob, train_step, y, cross_entropy, W_conv1 = create_m_graph(train=True)
            
        # set saver
        saver = tf.train.Saver(tf.all_variables())
        # initialize the variables
        sess.run(tf.global_variables_initializer())
    
        # training the MLP
        for i in range(500): 
            sess.run(train_step, feed_dict={x: data_filter_train, y_target: labels_train, keep_prob: 0.5})
            if i%10 == 0:
                train_accuracy = sess.run(accuracy, feed_dict={x:data_filter_train, y_target: labels_train, keep_prob: 1})
                print ("step %d, training accuracy: %.3f"%(i, train_accuracy))
                
        # for given x, y_target data set
        print  ("test accuracy: %g"% sess.run(accuracy, feed_dict={x:data_filter_test, y_target: labels_test, keep_prob: 1}))
        
        # show weight matrix as image 
        weight_vectors = sess.run(W_conv1, feed_dict={x: data_filter_train, y_target: labels_train, keep_prob: 1.0})
        #show_layer(weight_vectors)
        
        # Save Model
        path = './model/'
        if not os.path.exists(path):
            os.makedirs(path)
            print("path created")
        saver.save(sess, path)
        print("model saved")
    except Exception as e : 
        raise Exception ("error on training: {0}".format(e))
    finally :
        sess.close()

# run stuff
run()

###predict test set
def predict(test_data) : 
    try : 
        # reset Graph
        tf.reset_default_graph()   
        # Create Session
        sess = tf.Session(config=tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth =True)))  
        # create graph
        if(filter_type == 'single') :
            _, x, _, _, _, y, _, _ = create_s_graph(train=False)
        else : 
            _, x, _, _, _, y, _, _ = create_m_graph(train=False)
        
        # initialize the variables
        sess.run(tf.global_variables_initializer())
        
        # set saver
        saver = tf.train.Saver()
        
        # Restore Model
        path = './model/'
        if os.path.exists(path):
            saver.restore(sess, path)
            print("model restored")

        # training the MLP
        #print("input data : {0}".format(test_data))
        y = sess.run([y], feed_dict={x: np.array([test_data])})
        print("result : {0}".format(y))
        print("result : {0}".format(np.argmax(y)))
        
        return np.argmax(y)

    except Exception as e : 
        raise Exception ("error on training: {0}".format(e))
    finally :
        sess.close()

print("words in dict : {0}".format(model.wv.index2word))

input_data = '컴퓨터 추천좀 게이ㅁ'
a = predict(np.array(inference_embed(input_data))).flatten()

print(a)
if a == 0:
    print('1. 파워서플라이 고장\n2. 수은전지 방전\n3. 전원버튼 고장\n4. 메인보드 고장(컴퓨터 사망)')
elif a == 1:
    print('1.키보드 우측상단의 NumLock의 LED점멸버튼의 작동여부를 확인하세요\n2. 램 접촉불량이 발생할 수 있습니다\n3. 그래픽카드 접촉불량이 발생할 수 있습니다')
elif a == 2:
    print('컴퓨터는 CPU에 과열이 관측되면 자동적으로 전원을 내리거나 재부팅을 시전하게 된다. 따라서 CPU 쿨링 팬이 역할을 제대로 하지 못하면 발생한다. 쿨링 팬의 고장이나 장착이 제대로 되었는지, 쿨링 팬과 방열판 사이에 먼지가 잔뜩 껴서 단열재 역할을 하고 있지는 않은지, 도포된 서멀구리스를 점검해볼 필요가 있다')
elif a == 3:
    print(' 그래픽 카드를 의심해봐야 한다. 블루스크린에서 오류번호가 0x00000116이면 그래픽 카드 이상이다. 그 외에도 컴퓨터 수리점에서는 그래픽 카드 불량이 의심된다면 그래픽 카드를 뽑아서 점검 PC에 꽂아보므로 바로 알 수 있다.')
elif a == 4:
    print('고장 유형 중 제일 양호한 편이다. 이게 뜨는 이유는 대부분 소프트웨어적 고장인데, Windows 재설치+CMOS 초기화 콤보로 하면 거의 다 해결가능')
elif a == 5:
    print('컴퓨터를 부팅시 특정 시스템에서 그래픽카드와 CPU 쪽에서 한동안 굉음을 냈다가 부팅이 되며 잠잠해지는 경우가 있는데 부품 특성이며 고장이 아니다. 만약, 팬이 굉음을 내며 모니터에 불이 안들어오고 부팅이 안된다면, 그래픽카드 불량을 의심해봐야 된다. 노트북의 경우 써멀이 굳었거나 밀착이 제대로 안되어 열전도에 문제가 생겼을 때에도 이런 현상이 나타난다.')
elif a == 6:
    print('1. 먼지 냄새, 썩는 냄새가 나는 경우에는 컴퓨터 청소 불량으로 인한 먼지, 벌레 시체, 음식물 등이 원인이다. 가끔씩이라도 컴퓨터를 내외부 모두 청소해주면 된다\n2. 타는 냄새가 나는 경우는 대부분 누전이나 과부하등의 원인으로 인해 부품이 타는 경우이므로 전원을 빨리 차단하고 내부를 열어서 탄 부품을 교체해야 한다')
elif a == 7:
    print('1. 허브와 컴퓨터가 연결되는 회선불량\n2. 허브포트의 문제\n3. 컴퓨터 랜포트의 문제\n4. 아이피전화기를 사용하고 있다면 아이피전화기 포트 문제\n5. 아이피전화기 컴퓨터가 연결되어있으면 연결된 회선문제\n6. 아이피를 잘못 입력했거나, DNS주소가 잘못되었을때\n7. Windows의 DHCP 서비스가 실행이 안되어있을때')
elif a == 8:
    print('먼저 스피커 선이 본체에 꽂혀있는지, 똑바로 꽂혀있는지 확인한다. PC방의 경우 꽂았다 뺐다 하는 과정에서 헤드셋 선을 연결했다가 원래대로 스피커 선을 꽂아놓지 않거나 스피커 선(초록색)과 마이크 선(빨간색)을 헷갈려서 잘못 꽂은 경우가 많다. 최근들어 USB 방식의 헤드폰이 보급되면서 바탕화면에 스피커/헤드폰을 전환하는 단축 아이콘을 이용할 수 있는 경우도 있다.')
elif a == 9:
    print('- USB 케이블로 연결되어 있을 경우\n1. 케이블 불량\n2. 컴퓨터 포트 불량\n3. 프린터 포트 불량\n4. 프린터 스풀러 문제로 스풀러 중지후 재시작\n- 랜선 및 프린터 서버로 연결되어 있을 경우\n1. 서버 컴퓨터 전원 꺼짐\n2. 서버 컴퓨터에 프린터 스풀러 오류\n3. 랜선 불량\n3. 허브 불량\n4. 허브 포트 불량\n5. RJ45 포트 불량')
elif a == 10:
    print('1. 인터넷을 이용해서 이런 저런 프로그램들은 많이 내려 받아서\n2. 바이러스 혹은 치료가 안되는 악성코드에 감염된 경우\n3. 시작 프로그램이 컴퓨터의 리소스를 많이 차지하는 경우\n 4. 레지스트리(윈도우가 실행되는 데 필요한 정보가 등록돼 있는 데이터베이스)나 불필요한 파일로 인한 경우\n5. 드라이버 설치\n6. 잦은 응용 프로그램 설치와 제거')