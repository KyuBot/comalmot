from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

import requests
import tensorflow as tf
import numpy as np
import os
from matplotlib.image import imread, imsave 
import matplotlib.pyplot as plt  
import pandas as pd
from eunjeon import Mecab
from gensim.models import word2vec

from .models import Cpus, Gpus
from .serializers import CpuSerializer, GpuSerializer

###Parameters
vector_size = 100
encode_length = 32
label_size = 2
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
                    '고사양 게임용 컴퓨터 추천좀',
                    '최저가 게임용 컴퓨터좀 알려줘',
                    '컴퓨터 추천좀 해줘',
                    '영상편집용 컴퓨터좀 알려줘',
                    '사무용 컴퓨터좀 알려줘',
                    '저렴한 컴퓨터 알려줘',
                    '가성비 컴퓨터 추천좀',
                    '방송용 컴퓨터 추천좀 해줘',
                    '컴퓨터좀 알려줘',
                    '컴퓨터 추천',

                    '저렴한 문서작업용 노트북 추천해줘',
                    '영상편집용 노트북좀 알려줘',
                    '최저가 게임용 노트북좀 알려줘',
                    '저렴한 노트북 추천해줘',
                    '노트북 추천',
                    '게임용 노트북좀 알려줘',
                    '고사양 게임용 노트북 추천좀',
                    '영상편집 노트북 추천좀해줘',
                    '문서작업용 노트북좀 알려줘',
                    '가성비 좋은 노트북 추천좀',

                    '모니터에 불이 안들어와',
                    '컴퓨터 화면이 안켜져',
                    '컴퓨터 전원이 안켜져',
                    '컴퓨터가 안되',
                    '노트북이 안되',
                    '컴퓨터가 안켜져',
                    '노트북이 안켜져',
                    '노트북 화면이 안켜져',
                    '노트북 전원이 안켜져',
                    '노트북이 너무 느려졌어',
                    '노트북 블루스크린 떳어요',
                    '컴퓨터 블루스크린 떳어요',
                    ],
                'decode' : ['0']*20 + ['1']*12
             }
train_data_list.get('encode')


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
# def run() : 
#     try : 
#         # get Data 
#         labels_train, labels_test, data_filter_train, data_filter_test = get_test_data()
#         # reset Graph
#         # tf.reset_default_graph()   
 
#         # Create Session
#         sess = tf.Session(config=tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth =True)))  
#         # create graph
#         if(filter_type == 'single') :
#             accuracy, x, y_target, keep_prob, train_step, y, cross_entropy, W_conv1 = create_s_graph(train=True)
#         else :
#             accuracy, x, y_target, keep_prob, train_step, y, cross_entropy, W_conv1 = create_m_graph(train=True)
            
#         # set saver
#         saver = tf.train.Saver(tf.all_variables())
#         # initialize the variables
#         sess.run(tf.global_variables_initializer())
    
#         # training the MLP
#         for i in range(100): 
#             sess.run(train_step, feed_dict={x: data_filter_train, y_target: labels_train, keep_prob: 0.5})
#             if i%10 == 0:
#                 train_accuracy = sess.run(accuracy, feed_dict={x:data_filter_train, y_target: labels_train, keep_prob: 1})
#                 print ("step %d, training accuracy: %.3f"%(i, train_accuracy))
                
#         # for given x, y_target data set
#         print  ("test accuracy: %g"% sess.run(accuracy, feed_dict={x:data_filter_test, y_target: labels_test, keep_prob: 1}))
        
#         # show weight matrix as image 
#         weight_vectors = sess.run(W_conv1, feed_dict={x: data_filter_train, y_target: labels_train, keep_prob: 1.0})
#         #show_layer(weight_vectors)
        
#         # Save Model
#         path = './model/'
#         if not os.path.exists(path):
#             os.makedirs(path)
#             print("path created")
#         saver.save(sess, path)
#         print("model saved")
#     except Exception as e : 
#         raise Exception ("error on training: {0}".format(e))
#     finally :
#         sess.close()

# # run stuff
# run()

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


@api_view(['POST'])
def word(request):
    text = request.data['text']
    intent_id = predict(np.array(inference_embed(input_data)).flatten())

    output_data = ' '

    request = {
                    "intent_id" : " ",
                    "input_data" : input_data,
                    "request_type" : "text",
                    "story_slot_entity" : {},
                    "output_data" : output_data,
                }

    #기본 데이터셋(DB)
    intent_list = ['추천','진단']

    sub_intent_list = {'게임':['배그','롤','피파','서든','카트','스타','워크','와우','로아','로스트아크','캐주얼','고사양'],
                        '전문가':['캐드','포토샵','일러스트레이트'],
                        '방송':['원컴','투컴']}

    story_slot_entity = {"추천" : {"종류" : None, "용도" : None, "가격" : None, '세부' : None},
                        "진단" : {"종류" : None, "사용시기" : None, "문제점" : None},
                            }

    #형태소 분석
    mecab = Mecab()
    preprocessed = mecab.pos(input_data)
    #.pos() 문장을 형태소 단위로 쓶고 형태소마다 품사 분석 
    # ex) ('판교','NNG') NNG는 일반명사
    print(preprocessed)

    # Intent 도출(Rule Based)   
    # Char CNN을 사용해서 연결하면 좀 더 쉽게 만들 수 있어

    slot_value = story_slot_entity.get(intent_list[intent_id])

    #NER 도출 (Rule Based)  
    # LSTM 기법을 사용해서 연결하면 좀 더 쉽게 만들 수 있어
    menu_list = ['컴퓨터', '데스크탑', '노트북','랩탑']
    loc_list = ['최저가', '고가', '저렴','가성']
    date_list = ['문서','사무', '방송','게임','영상편집','전문가',]


    if intent_id == 0:
        print('추천 서비스를 시작합니다.')
    elif intent_id == 1:
        print('컴퓨터 진단 서비스를 시작합니다.')

    # slot 구성
    for pos_tag in preprocessed :
        if pos_tag[1] in ['NNG', 'NNP', 'SL', 'MAG','XR','SN'] :
            if pos_tag[0] in menu_list :
                slot_value['종류'] = pos_tag[0]

            if pos_tag[0] in date_list :
                slot_value['용도'] = pos_tag[0]


            if (pos_tag[0] in loc_list) or pos_tag[1] == 'SN':
                slot_value['가격'] = pos_tag[0]


    print(story_slot_entity.get('추천'))

    # 빈슬롯 확인
    if (None in slot_value.values()):
        key_values = " "
        for key in slot_value.keys():
            if(slot_value[key] is None):
                if key == '종류':
                    output_data = '어떤종류를 구매하실 예정인가요?? ex) 컴퓨터,노트북,데스크탑,랩탑'
                    break
                if key == '용도':
                    output_data = '어떤 용도로 사용하실 예정인가요?? ex) 게임용,사무용,영상편집,전문가'
                    break
                #용도 정해졌을때 - 세부목적
                if key == '세부':
                    if slot_value.get('용도') == '게임':
                        output_data = '어떤게임을 주로 하시나요?'
                        break
                    elif slot_value.get('용도') == '방송':
                        output_data = '1컴방송 2컴방송?'
                        break
                    elif slot_value.get('용도') == '전문가':
                        output_data = '어떤 프로그램을 주로 사용하시나요?'
                        break

                if key == '가격':
                    output_data = '가격대는 얼마정도로 생각하고 계신가요?? ex)가성비, 최저가, 고가, XX만원대'
                    break
        #     if(slot_value[key] is None):
        #         key_values = key_values + key + " "
        # output_data = key_values + "선택해주세요"
    else:
        #cpu = CPU.objects.filter('용도')
        #gpu =  GPU.object.filter('')
        output_data = "종류:{} 용도:{} 가격:{} 추천이 완료 되었습니다.".format(slot_value.get('종류'),slot_value.get('용도'),slot_value.get('가격'))
        ##캐쉬 새로고침

    # print(output_data)
    # 빈슬롯 확인
    response = {
                    "intent_id" : " ",
                    "input_data" : input_data,
                    "request_type" : "text",
                    "story_slot_entity" : {},
                    "output_data" : " "
                    }

    response["output_data"] = output_data

    print(response["output_data"])
    print(response["story_slot_entity"])

    
    cpu = Cpus.objects.get(id=1)
    serializer = CpuSerializer(cpu)
    print(cpu)
    # context = {
    #     'message': message,
    #     'cpu':cpu
    # }
    
    return Response(serializer.data)

    # cpu 
    #사무 2000~9000
    #게임 9000~ 20000 // 9000~15000(저,중사양) 15000~20000(고사양)
    #영상편집 == 게임(고사양)
    #전문가
    #방송

    #gpu
    #사무 x
    #게임 1050~3070(게임에 따라서)
    #영상편집(4k면 높은거 아니면 1660super정도 ~ 2080)
    #전문가(1660super 이상)
    #방송

    #ram
    #사무 4~8
    #게임 8~16(캐주얼8 고사양16)
    #영상편집(16)
    #전문가(16이상)

    #메인보드
    # 사무 저가형보드(인텔,amd)
    # 게임 중급보드,고급
    # 영상편집 중급보드,고급
    # 전문가 고급보드