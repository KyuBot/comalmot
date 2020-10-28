train_data_recommend = ['저렴한 게임용 컴퓨터 추천 해줘']
train_data_check = ['컴퓨터 전원이 안켜져']

get_data_list = train_data_recommend[0]

dict_entity = {
    'purpose' : ['게임','사무','영상편집','방송'],
    'price' : ['가성비','고가','저가','최저가','저렴'],
    'type' : ['컴퓨터','노트북','데스크탑','랩탑'],
    'problem' : ['전원','소리','키보드','모니터'],
}

length = 1
for key in list(dict_entity.keys()):
    length = length * len(dict_entity[key])
# print("Augmentation length is {0}".format(length))
#-> Augmentation length is 320

from eunjeon import Mecab
mecab = Mecab()
morpphed_text = mecab.pos(get_data_list)
# print(morpphed_text)
#-> [('저렴', 'XR'), ('한', 'XSA+ETM'), ('게임', 'NNG'), ('용', 'XSN'), ('컴퓨터', 'NNG'), ('추천', 'NNG'), ('해', 'XSV+EC'), ('줘', 'VX+EC')]

tagged_text = ''
for pos_tags in morpphed_text:
    if (pos_tags[1] in ['NNG','MAG', 'NNP','SL','XR'] and len(pos_tags[0]) > 1): #Check only Noun
        feature_value = pos_tags[0]
        tagged_text = tagged_text + pos_tags[0] + ' '
print(tagged_text)
#-> 저렴 게임 컴퓨터 추천

pattern = ''
for word in tagged_text.split(' '):
    entity = list(filter(lambda key:word in dict_entity[key],list(dict_entity.keys())))
    if(len(entity) > 0): 
        pattern = pattern + 'tag' + entity[0] + ' '
    else:
        pattern = pattern + word + ' '

print(pattern)


def augmentation_pattern(pattern, dict_entity):
    #입력된 패턴을 List로 바꿈
    aug_pattern = pattern.split(' ')
    #Augment된 Text List
    augmented_text_list = []
    #copy를 위한 임시 List
    temp_aug = []
    for i in range(0,len(aug_pattern)):
        #Entity에 해당하는 값일 경우 Entity List를 가져옴
        if(aug_pattern[i].find("tag") > -1):
            dict_list = dict_entity[aug_pattern[i].replace("tag","")]
            #각 Entity별로 값을 append하면서 Pattern구성
            for j in range(0,len(dict_list)):
                #최초 Entity값은 그냥 추가만함
                if(i == 0):
                    augmented_text_list.append(dict_list[j] + " ")
                elif(j == 1):
                    augmented_text_list = list(filter(lambda word:len(word.split(' ')) == i + 1 ,augmented_text_list))
                    copy_data_order = augmented_text_list * (len(dict_list)-2)
                    augmented_text_list = list(map(lambda x:x + dict_list[j] + " ",augmented_text_list))
                    augmented_text_list = augmented_text_list + temp_aug + copy_data_order
                else:
                    #List의 수를 체크하여 값을 추가
                    temp_aug = list(filter(lambda word:len(word.split(' ')) == i+1 ,augmented_text_list))
                    temp_aug = list(map(lambda x:x + dict_list[j] + " " ,temp_aug))
                    #추가된 List를 위해 기존 값 삭제
                    if(j != 0):
                        augmented_text_list = augmented_text_list[0:len(augmented_text_list) - len(temp_aug)]
                    augmented_text_list = augmented_text_list + temp_aug

        #Entity추가 대상이 아닐 경우 Pattern만 추가
        else:
            augmented_text_list = list(map(lambda x:x + aug_pattern[i] + " ",augmented_text_list))
        #N*N으로 증가시키기 위한 List
        temp_aug = augmented_text_list
    return augmented_text_list

augmented_text_list = augmentation_pattern(pattern, dict_entity)
# print(augmented_text_list)

def augmentation_bio_pattern(pattern, dict_entity):
    #입력된 패턴을 List로 바꿈
    aug_pattern = pattern.split(' ')
    #Augment된 Text List
    augmented_text_list = []
    #copy를 위한 임시 List
    temp_aug = []
    for i in range(0,len(aug_pattern)):
        #Entity에 해당하는 값일 경우 Entity List를 가져옴
        if(aug_pattern[i].find("tag") > -1):
            dict_list = dict_entity[aug_pattern[i].replace("tag","")]
            bio_tag = aug_pattern[i].replace("tag","B_")
            #각 Entity별로 값을 append하면서 Pattern구성
            for j in range(0,len(dict_list)):
                #최초 Entity값은 그냥 추가만함
                if(i == 0):
                    augmented_text_list.append(bio_tag + " ")
                elif(j == 1):
                    augmented_text_list = list(filter(lambda word:len(word.split(' ')) == i + 1 ,augmented_text_list))
                    copy_data_order = augmented_text_list * (len(dict_list)-2)
                    augmented_text_list = list(map(lambda x:x + bio_tag + " ",augmented_text_list))
                    augmented_text_list = augmented_text_list + temp_aug + copy_data_order
                else:
                    #List의 수를 체크하여 값을 추가
                    temp_aug = list(filter(lambda word:len(word.split(' ')) == i+1 ,augmented_text_list))
                    temp_aug = list(map(lambda x:x + bio_tag + " " ,temp_aug))
                    #추가된 List를 위해 기존 값 삭제
                    if(j != 0):
                        augmented_text_list = augmented_text_list[0:len(augmented_text_list) - len(temp_aug)]
                    augmented_text_list = augmented_text_list + temp_aug

        #Entity추가 대상이 아닐 경우 Pattern만 추가
        else:
            augmented_text_list = list(map(lambda x:x + aug_pattern[i] + " ",augmented_text_list))
        #N*N으로 증가시키기 위한 List
        temp_aug = augmented_text_list
    return augmented_text_list

bio_list = augmentation_bio_pattern(pattern, dict_entity)
#print(bio_list)

ner_train_text = [augmented_text_list, bio_list]
print(ner_train_text)