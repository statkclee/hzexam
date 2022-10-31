# hzexam.sty

hzexam.sty는 시험지 또는 문제집을 만들기 위한 레이텍 패키지이다.
주요 매크로는 다음과 같다.


    \QAsetup{
        file=undefined, 
        counter=1, 
        overwrite=true, 
        zeros=3, 
        teacher=true,   
        answer-sheet=true,
        question-no=1
    }

    \begin{premise}*[숫자]
    지문 또는 문제
    \end{premise}

    \qa{문제}[보기| 보기; ...]{객관식 또는 단답형 정답}
    \qa|{문제}[보기| 보기; ...]{서술형 정답}
    \qa*{하위 문제}[보기| 보기; ...]{서술형 정답}
    \ca{숫자}
    \ca*{단답}

    \begin{QAwrite}
    \end{QAwrite}

    \QAinput{.../...}{숫자, 숫자-숫자, 숫자}
    \QAinput{.../...}{*}

    \InputAnswerSheet

# texmodule.py

texmodule.py는 텍 파일들을 데이터베이스 파일에 저장하고 관리하는 파이썬 스크립트이다.
데이터베이스에 파일 내용을 저장할 때 파일 이름이 섹션 이름으로 사용된다.
여기에서 섹션은 처리 단위로서 레코드와 유사한데, 데이터베이스 테이블과 달리 정형화되어 있지 않다.
여러 섹션들을 조합하여 하나의 문서로 만들 수 있다.
이 스크립트는 hzexam.sty를 염두에 둔 것이지만, 그것과 무관하게 사용할 수 있다.
이를테면, 사양서 같은 모듈화 가능한 문서들을 만드는 데에 응용할 수 있을 것이다.

    삽입하기
    C:\>texmodule.py -i foo.tex goo*.tex ...
    
    갱신하기
    C:\>texmodule.py -u foo.tex goo*.tex ...

    삭제하기
    C:\>texmodule.py -r foo goo* ...

    섹션 목록 보기
    C:\>texmodule.py -l 

    모든 섹션을 꺼내기
    C:\>texmodule.py -b

    섹션들을 조합하기
    C:\>texmodule.py -a head-oblivoir foo goo* ...

마지막 예에서 head-oblivoir는 다른 내용들 앞에 붙일 전제부(preamble)를 가리킨다.
스크립트는 첫 인자가 "head-"로 시작하는지 확인하고, 그렇다면 "tail-"로 시작하는 같은 이름을 가진 섹션을 찾아 마지막에 덧붙인다.
이 예의 경우, tail-oblivoir를 찾는다. 없으면 \end{document}를 덧붙인다.
수집된 섹션들이 assembled.tex 파일에 쓰여진다.
다른 파일 이름을 지정하려면 -o 옵션을 사용한다.