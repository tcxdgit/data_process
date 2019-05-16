from win32com import client as wc
from pydocx import PyDocX



def doc2docx():
    word = wc.Dispatch('Word.Application')

    # doc = word.Documents.Open(r'G:\\T.doc')
    # path = r'E:\3101A0CV-20170615-H3C RPS800-A 用户手册-6PW101\06-正文.doc'
    # if path.endswith('.doc'):
    doc = word.Documents.Open(r'E:\\3101A0CV-20170615-H3C RPS800-A 用户手册-6PW101\06-正文.doc')

    doc.SaveAs(r'D:\\T.docx', 16)  # 使用参数16，表示将doc转成docx

    doc.Close()

    word.Quit()

# html = PyDocX.to_html("test.docx")
html = PyDocX.to_html(r'E:\\3101A0CV-20170615-H3C RPS800-A 用户手册-6PW101\06-正文.docx')
f = open("test.html", 'w', encoding="utf-8")
f.write(html)
f.close()
