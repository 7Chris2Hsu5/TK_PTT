# 引入套件
import requests
from bs4 import BeautifulSoup
from tkinter import *


def first_page(url, NewOld):
    if NewOld == 'new':
        return url
    elif NewOld == 'old':
        rq = requests.get(url)
        soup = BeautifulSoup(rq.text, 'html.parser')
        tags = soup.find_all('a', class_='btn wide')
        return 'https://www.ptt.cc/' + tags[0].get('href')


# 下一頁
def next_page(url, NewOld):
    rq = requests.get(url)
    soup = BeautifulSoup(rq.text, 'html.parser')
    tags = soup.find_all('a', class_='btn wide')

    header = 'https://www.ptt.cc/'
    if NewOld == 'new':
        rtn_url = header + tags[1].get('href')
        return rtn_url
    elif NewOld == 'old':
        if len(tags) == 3:
            rtn_url = header + tags[1].get('href')
            return rtn_url
        else:
            rtn_url = header + tags[2].get('href')
            return rtn_url


# 搜尋頁面
def search_page(window, value, NewOld, num):
    search = Toplevel(window)
    # 標題
    search.title("搜尋結果")
    # 長寬 (string)
    search.geometry("500x500")
    # 是否可以更改大⼩(0 or 1) (x, y)
    search.resizable(1, 1)

    # label
    label_1 = Label(search, text=value + '看板的搜尋結果', font=("標楷體", 24))
    label_1.pack()

    # 載入資料
    blank_url = 'https://www.ptt.cc/bbs/' + value + '/index.html'
    blank_url = first_page(blank_url, NewOld)

    List_url = []
    List_title = []
    for n in range(1, num + 1):
        List_url.append(n)
        List_title.append('---------------第 ' + str(n) + ' 頁---------------')

        print('blank_url', blank_url)
        rq = requests.get(blank_url)
        soup = BeautifulSoup(rq.text, 'html.parser')
        tags = soup.find_all('div', class_='title')

        head = 'https://www.ptt.cc/'
        for i in tags:
            try:
                url = i.find('a')
                List_url.append(head + url.get('href'))
                List_title.append(i.text.strip())
            except:
                pass

        blank_url = next_page(blank_url, NewOld)

    # Listbox
    Lb1 = Listbox(search, selectmode=SINGLE, bd=4, width=60, fg='blue', font=("標楷體", 16))
    for i in List_title:
        Lb1.insert(END, i)

    Lb1.pack(fill=Y, expand=YES)

    # button
    btn1 = Button(search,
                  command=lambda: content_page(search, List_url, int(Lb1.curselection()[0]),
                                               Lb1.get(Lb1.curselection())),
                  text="進入", bg='RED', fg='WHITE', font=("標楷體", 24))
    btn1.pack()


# 文章內容頁面
def content_page(search, url_List, index, value):
    # 產生新頁面
    content = Toplevel(search)
    # 標題
    content.title(value)
    # 長寬 (string)
    content.geometry("600x600")
    # 是否可以更改大⼩(0 or 1) (x, y)
    content.resizable(1, 1)

    # text & scrollbar
    sco_1 = Scrollbar(content)
    text_1 = Text(content, height=600, width=600, font=("標楷體", 16))

    sco_1.pack(side=RIGHT, fill=Y)
    text_1.pack(side=LEFT, fill=Y)

    sco_1.config(command=text_1.yview)
    text_1.config(yscrollcommand=sco_1.set)

    # 載入資料
    url = url_List[index]
    rq = requests.get(url)
    soup = BeautifulSoup(rq.text, 'html.parser')
    tags = soup.find('div', id="main-container")
    content = tags.text

    # 將內容載入Text
    text_1.insert(END, content)


# main-----------------------------------------------------------------
window = Tk()
# 標題
window.title("PTT")
# 長寬 (string)
window.geometry("500x500")
# 是否可以更改大⼩(0 or 1) (x, y)
window.resizable(0, 0)

# label
label_1 = Label(window, text='輸入看板名稱', font=("標楷體", 28))
label_1.pack(fill=BOTH, expand=YES)

# entry
ipt_1 = Entry(window, bd=2, width=35)
ipt_1.pack()

# label
label_2 = Label(window, text='顯示頁數', font=("標楷體", 18))
label_2.pack(fill=BOTH, expand=YES)

# entry
ipt_2 = Entry(window, bd=2, width=10)
ipt_2.pack()

# radiobutton
var = StringVar()
var.set('new')
R1 = Radiobutton(window, text="最新", font=("標楷體", 13), variable=var, value='new')
R1.pack(fill=BOTH, expand=YES)
R2 = Radiobutton(window, text="最舊", font=("標楷體", 13), variable=var, value='old')
R2.pack(fill=BOTH, expand=NO)

# button
btn1 = Button(window, text="搜尋", font=('標楷體', 18),
              command=lambda: search_page(window, ipt_1.get(), var.get(), int(ipt_2.get())))
btn1.pack(fill=X, expand=YES)

# 運行主程式
window.mainloop()