input_data = '판교에 지금 주문해줘'

output_data = ' '

request = {
                "intent_id" : " ",
                "input_data" : input_data,
                "request_type" : "text",
                "story_slot_entity" : {},
                "output_data" : output_data,
               }

#기본 데이터셋(DB)
intent_list = {
                  "주문" : ["주문", "배달"],
                  "예약" : ["예약", "잡아줘"],
                  "정보" : ["정보", "알려"],
                 }

story_slot_entity = {"주문" : {"메뉴" : None, "장소" : None, "날짜" : None},
                          "예약" : {"장소" : None, "날짜" : None},
                          "정보" : {"대상" : None},
                          }

from eunjeon import Mecab

#형태소 분석
mecab = Mecab()
preprocessed = mecab.pos(input_data)
#.pos() 문장을 형태소 단위로 쓶고 형태소마다 품사 분석 
# ex) ('판교','NNG') NNG는 일반명사
print(preprocessed)

# Intent 도출(Rule Based)   
# Char CNN을 사용해서 연결하면 좀 더 쉽게 만들 수 있어
intent_id = '주문'

slot_value = story_slot_entity.get('주문')

#NER 도출 (Rule Based)  
# LSTM 기법을 사용해서 연결하면 좀 더 쉽게 만들 수 있어
menu_list = ['피자', '햄버거', '치킨']
loc_list = ['판교', '야탑', '서현']
date_list = ['지금', '내일', '모레']

# slot 구성
for pos_tag in preprocessed :
    if pos_tag[1] in ['NNG', 'NNP', 'SL', 'MAG'] :
        if pos_tag[0] in menu_list :
            slot_value['메뉴'] = pos_tag[0]
        elif pos_tag[0] in loc_list :
            slot_value['장소'] = pos_tag[0]
        elif pos_tag[0] in date_list :
            slot_value['날짜'] = pos_tag[0]

print(story_slot_entity.get('주문'))

# 빈슬롯 확인
if (None in slot_value.values()):
    key_values = " "
    for key in slot_value.keys():
        if(slot_value[key] is None):
            key_values = key_values + key + " "
    output_data = key_values + "선택해주세요"
else:
    output_data = "주문이 완료 되었습니다."

print(output_data)
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