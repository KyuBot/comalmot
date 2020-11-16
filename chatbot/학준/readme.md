### 형태소 분석

```
$pip install eunjeon

from eunjeon import Mecab
mecab = Mecab()
text = '노트북 추천좀 해줘'
preprocessed = mecab.pos(text)
print(preprocessed)

->
[('노트북', 'NNG'), ('추천', 'NNG'), ('좀', 'MAG'), ('해', 'VV+EC'), ('줘', 'VX+EC')]
```

koNLPy __(한글 토크나이징 라이브러리)__에서 제공하는 mecab __(형태소 분석 오픈소스)__은 윈도우에서 사용이 불가능하다.

KoNLPy의 하위프로젝트인 koshort 프로젝트의 pyeunjeon __(python + eunjeon)__을 통해 은전한닢 프로젝트의 mecab을 윈도우에서도 쉽게 설치가 가능하다.

#### [error]

* error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools": https://visualstudio.microsoft.com/downloads/

  -> 해결법:

  https://somjang.tistory.com/entry/Python-pip-install-%EC%8B%9C-error-Microsoft-Visual-C-140-is-required-%EC%98%A4%EB%A5%98-%ED%95%B4%EA%B2%B0-%EB%B0%A9%EB%B2%95 

  https://dololak.tistory.com/520

* ```
  Traceback (most recent call last): File "D:/workspace/pycharm/MecabTest/test2.py", line 3, in <module> mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic') File "D:\workspace\pycharm\MecabTest\venv2\lib\site-packages\eunjeon\_mecab.py", line 106, in __init__ raise Exception('The MeCab dictionary does not exist at "%s". Is the dictionary correctly installed?\nYou can also try entering the dictionary path when initializing the Mecab class: "Mecab(\'/some/dic/path\')"' % dicpath) Exception: The MeCab dictionary does not exist at "C:/mecab/mecab-ko-dic". Is the dictionary correctly installed? You can also try entering the dictionary path when initializing the Mecab class: "Mecab('/some/dic/path')"
  ```

  -> 가상환경에 설치했을때 발생했던 에러

  -> 가상환경 밖에 설치했더니 에러 안생김