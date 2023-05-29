from tkinter import *           # GUI를 위해 tkinter 가져오기
from tkinter import filedialog  # 파일을 입력받기 위해 filedialog 별도로 가져오기
from PIL import ImageTk, Image  # 이미지 데이터 가공을 위해 ImageTk, Image 가져오기
import pandas as pd             # DataFrame을 사용하여 2차원 테이블 형태의 데이터를 편리하게 가공하기 위해 pandas 가져오기
import matplotlib.pyplot as plt # 그래프를 구현하기 위해 matplotlib.pyplot 가져오기
import pytesseract              # 이미지에서 텍스트를 추출하기 위해 pytesseract 가져오기


app = Tk()  # Tk 인스턴스 생성 후 app에 할당
text = ''   # 전역 변수로 사용하기 위해 text 선언 및 초기화
file = ''   # 전역 변수로 사용하기 위해 file 선언 및 초기화


# 함수 선언
def open_file_dialog():
    
    # 전역 변수 file을 사용하겠다고 선언
    global file
    
    # filedialog.askopenfile()를 호출하여 파일 시스템을 열고, 변수 file에 사용자가 선택한 파일 할당
    file = filedialog.askopenfile() 

    # 변수 file에 값이 있다면 조건문의 실행문을 실행
    if file:
        
        # 전역 변수 text를 사용하겠다고 선언
        global text
        
        # Image.open() 함수를 호출하여 인자로 file.name을 넘겨주며 해당 파일의 경로를 찾아서 화면에 띄움
        # 여기서 변수 image에 PIL의 Image 인스턴스를 할당
        image = Image.open(file.name)                   
        
        # Image 인스턴스의 크기를 인자로 넘겨줘서 크기를 조정
        # 변수 resized_image에 크기가 조정된 새로운 Imgae 인스턴스를 할당
        resized_image = image.resize((200, 200))        

        # Image 인스턴스를 ImageTk.PhotoImage() 함수의 인자로 넘겨주며, ImageTk 인스턴스로 변환
        # 이 작업을 추가한 이유는 Tkinter에서 사용할 수 있는 인스턴스로 변환 시키기 위함
        # 변수 tk_image에 ImageTk 인스턴스를 할당
        tk_image = ImageTk.PhotoImage(resized_image)

        # Label 위젯을 생성하며, 생성자 전달 인자에 Tk 인스턴스인 변수 app과 image에 ImageTk 인스턴스를 가지고 있는 변수 tk_image를 넘겨줌
        label = Label(app, image=tk_image)

        # .grid() 함수를 호출하여 Label 위젯의 위치를 column과 row로 설정
        label.grid(column=1, row=5)

        # pytesseract.image_to_string() 함수를 호출해서 인자로 image 인스턴스를 넘겨주면, 
        # Tesseract OCR 엔진을 사용하여 이미지에서 텍스트를 추출해준다.
        # 추출된 텍스트를 변수 text에 할당
        text = pytesseract.image_to_string(image)

        # 리소스 낭비를 방지하기 위해 파일 객체 닫아주기
        file.close()


# 함수 선언
def make_graph():

    # 전역 변수 text을 사용하겠다고 선언
    global text
    
    # 딕셔너리 타입을 사용하기 위해 변수 선언 및 초기화
    result = {}

    # 변수 text에 값이 있다면 조건문의 실행문 실행 
    if text:

        # 변수 text에서 공백을 기준으로 자른 텍스트를 리스트로 변환하여 변수 words에 반환
        words = text.split()

        # 단어 담겨 있는 변수 words를 for문을 활용하여 하나씩 변수 word에 담아준다.
        for word in words:

            # 단어의 양쪽 공백을 잘라 다시 변수 word에 할당
            word = word.strip()

            # 만약 변수 word에 값이 있다면 조건문의 실행문을 실행
            if word:

                # 딕셔너리 타입인 result의 key 값 중에 변수 word의 값이 있다면 조건문의 실행문을 실행
                if word in result:

                    # 변수 result의 key 값으로 value 값을 찾아 1을 더해준다.
                    result[word] += 1

                # 딕셔너리 타입인 result의 key 값 중에 변수 word의 값이 없다면 조건문의 else를 실행
                else:

                    # 변수 result의 key 값을 대입하여 새로운 key를 만들고, 해당 key의 value 값에 1을 할당.
                    result[word] = 1

        # 2차원 테이블 형태인 DataFrame 생성해서 변수 df에 DataFrame 인스턴스 할당
        df = pd.DataFrame({'Word': list(result.keys()), 'Count': list(result.values())})
        
        # bar()함수를 호출하여 막대 그래프 생성
        # 첫 번째 인자는 x축, 두 번째 인자는 y축에 데이터가 들어간다.
        plt.bar(df['Word'], df['Count'])

        # x축의 이름을 지정
        plt.xlabel('Word')

        # y축의 이름을 지정
        plt.ylabel('Count')

        # 그래프의 이름을 지정
        plt.title('Project')

        # x축의 눈금 레이블을 90도로 회전
        plt.xticks(rotation=90)

        # 그래프의 요소들을 자동으로 조정하여 적절한 간격 확보
        plt.tight_layout()

        # get_current_fig_manager() 함수를 호출하여 현재 활성화된 Matplotlib 그림 관리자를 반환하여 변수 mng에 할당
        mng = plt.get_current_fig_manager()

        # window의 state() 함수를 호출하여 그림 관리자에서 관리하는 그래프 창의 상태를 'zoomed'로 설정
        # 'zoomed' 상태는 그래프 창을 최대화하는 상태를 의미 (전체 화면)
        mng.window.state('zoomed')

        # 그래프를 화면에 보여줌
        plt.show()

    # 변수 text에 값이 없다면 조건문의 else 실행 
    else:

        # 이미지가 없다면 변수 text도 빈 값을 가지고 있기 때문에 빈 그래프 창을 띄우는 것을 방지하기 위해 방어적 코드 작성
        Label(app, text=('이미지를 먼저 선택해주세요.')).grid(column=1, row=13)


# 함수 선언
def add_count():

    # 전역 변수 file을 사용하겠다고 선언
    global file

    # 변수 file에 값이 있다면 조건문의 실행문 실행 
    if file:

        # 사용자의 입력 값을 받아 변수 user_input에 할당
        user_input = entry.get()

        # .strip() 함수를 호출하여 변수 user_input의 양쪽 공백을 지웠을 때의 값이 비어있지 않다면 if문의 실행문 실행
        if (user_input.strip()):

            # .strip() 함수를 호출하여 변수 user_input의 양쪽 공백을 지운 값을 반환
            # .count() 함수를 호출하여 변수 text에 user_input.strip()의 값과 일치하는 총 갯수를 반환
            # str() 함수를 호출하여 정수인 text.count(user_input.strip()) 의 반환 값을 문자열로 형변환
            # .grid() 함수를 호출하여 인자로 column과 row를 넘겨줘서 위치를 설정하고, 화면에 해당 Label 위젯을 띄운다.
            Label(app, text=("해당 이미지에 입력하신 텍스트가" + str(text.count(user_input.strip())) + "개 있습니다.")).grid(column=1, row=13)

        # .strip() 함수를 호출하여 변수 user_input의 양쪽 공백을 지웠을 때의 값이 비어있다면 if문의 else 실행
        else:

            # # .grid() 함수를 호출하여 인자로 column과 row를 넘겨줘서 위치를 설정하고, 화면에 해당 Label 위젯을 띄운다.
            Label(app, text=('올바른 값을 입력해주세요')).grid(column=1, row=13)
    
    # 변수 file에 값이 없다면 조건문의 else 실행 
    else:

        # .grid() 함수를 호출하여 인자로 column과 row를 넘겨줘서 위치를 설정하고, 화면에 해당 Label 위젯을 띄운다.
        Label(app, text=('이미지를 먼저 선택해주세요.')).grid(column=1, row=13)

# Button 위젯을 생성하여 생성자에 전달 인자로 Tk 인스턴스를 가지고 있는 변수 app,
# text에는 파일 선택
# 해당 Button 위젯에 이벤트가 발생했을 때 호출 할 함수를 command에 할당 
# .grid() 함수를 호출하여 인자로 column과 row를 넘겨줘서 위치를 설정하고, 화면에 해당 Button 위젯을 띄운다.
Button(app, text="파일 선택", command=open_file_dialog).grid(column=0, row=4)

# Label 위젯을 생성하여 생성자에 전달 인자로 Tk 인스턴스를 가지고 있는 변수 app,
# text에는 텍스트를 입력하세요.
# .grid() 함수를 호출하여 인자로 column과 row를 넘겨줘서 위치를 설정하고, 화면에 해당 Label 위젯을 띄운다.
Label(app, text="텍스트를 입력하세요.").grid(column=0, row=9)

# Entry 위젯을 생성하여 생성자에 전달 인자로 Tk 인스턴스를 가지고 있는 변수 app를 할당
# .grid() 함수를 호출하여 인자로 column과 row를 넘겨줘서 위치를 설정하고, 화면에 해당 Label 위젯을 띄운다.
entry = Entry(app)
entry.grid(column=0, row=10)

# Button 위젯을 생성하여 생성자에 전달 인자로 Tk 인스턴스를 가지고 있는 변수 app,
# text에는 총 갯수
# 해당 Button 위젯에 이벤트가 발생했을 때 호출 할 함수를 command에 할당 
# .grid() 함수를 호출하여 인자로 column과 row를 넘겨줘서 위치를 설정하고, 화면에 해당 Button 위젯을 띄운다.
add_count_button = Button(app, text="총 갯수", command=add_count).grid(column=0, row=11)

# Button 위젯을 생성하여 생성자에 전달 인자로 Tk 인스턴스를 가지고 있는 변수 app,
# text에는 그래프 보기
# 해당 Button 위젯에 이벤트가 발생했을 때 호출 할 함수를 command에 할당 
# .grid() 함수를 호출하여 인자로 column과 row를 넘겨줘서 위치를 설정하고, 화면에 해당 Button 위젯을 띄운다.
make_graph_button = Button(app, text="그래프 보기", command=make_graph).grid(column=1, row=11)

# Tk 인스턴스를 가지고 있는 변수 app에 접근하여 title() 함수를 호출해서 제목을 설정하기 위해 전달 인자로 문자열 프로젝트를 할당
app.title("프로젝트")

# Tk 인스턴스를 가지고 있는 변수 app에 접근하여 geometry() 함수를 호출해서 가로, 세로를 설정하기 위해 전달 인자로 문자열 "500x350"를 할당
app.geometry("500x350")

# Tk 인스턴스를 가지고 있는 변수 app에 접근하여 mainloop()를 호출한다.
# mainloop()를 호출해야 이벤트 루프를 시작하여 GUI창을 생성하고,
# 위에서 등록한 이벤트를 계속 감지하고 처리한다.
app.mainloop()

# Tkinter에서 이벤트 핸들러 함수로 등록된 함수는
# 애플리케이션의 실행 컨텍스트에서 호출된다.

# 해당 함수가 이벤트 발생 시 호출할 함수로 등록 되었고, 
# Entry 인스턴스가 생성되어 변수 entry에 할당 되는 그 순간 부터
# 해당 함수에서는 변수 entry를 함수 내에서 global 키워드 없이 접근할 수 있다.

