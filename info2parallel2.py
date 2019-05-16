from win32com import client as wc
from pydocx import PyDocX
from bs4 import  BeautifulSoup
import re
import nltk
import chardet
import os


def doc2docx(_path_doc):
    word = wc.Dispatch('Word.Application')

    # doc = word.Documents.Open(r'G:\\T.doc')
    # path = r'E:\3101A0CV-20170615-H3C RPS800-A 用户手册-6PW101\06-正文.doc'
    # if path.endswith('.doc'):
    # doc = word.Documents.Open(r'E:\\3101A0CV-20170615-H3C RPS800-A 用户手册-6PW101\06-正文.doc')
    doc = word.Documents.Open(_path_doc)

    path_docx = _path_doc.split(r'\\')[-1]
    # doc.SaveAs(r'D:\\T.docx', 16)  # 使用参数16，表示将doc转成docx
    doc.SaveAs(path_docx, 16)  # 使用参数16，表示将doc转成docx
    doc.Close()
    word.Quit()
    return path_docx


def docx2html(_path_docx):

    # html = PyDocX.to_html("test.docx")
    # html = PyDocX.to_html(r'E:\\3101A0CV-20170615-H3C RPS800-A 用户手册-6PW101\06-正文.docx')
    html = PyDocX.to_html(_path_docx)
    # f = open("test.html", 'w', encoding="utf-8")
    path_html = _path_docx.split("\\")[-1].split(".")[0] + ".html"
    f = open(path_html, 'w', encoding="utf-8")
    f.write(html)
    f.close()
    return path_html


def cut_sent(paragraph,lang='zh'):
    if lang == 'zh':
        paragraph = re.sub('([。！？\?])([^”’])', r"\1\n\2", paragraph)  # 单字符断句符
        paragraph = re.sub('(\.{6})([^”’])', r"\1\n\2", paragraph)  # 英文省略号
        paragraph = re.sub('(\…{2})([^”’])', r"\1\n\2", paragraph)  # 中文省略号
        paragraph = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', paragraph)
        # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
        paragraph = paragraph.rstrip().split("\n")  # 段尾如果有多余的\n就去掉它
        # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    elif lang == 'en':
        paragraph = nltk.sent_tokenize(paragraph)
        # print(para)

    return paragraph


def html2txt(_path_html, _tar_path, lang='zh'):
    with open(_path_html, "rb") as f_html:
        data = f_html.read()
        encode = chardet.detect(data)['encoding']
        print(encode)

    html = open(_path_html, encoding=encode)

    # html = html.read()
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.text.strip())英
    # list = []
    # text = ''
    # with open('99.txt','w',encoding='utf-8') as f:
    with open(_tar_path,'w',encoding='utf-8') as f:
        for tag in ['p','h1','h2','h3','h4']:
            for a in soup.select(tag):
                content = a.text
                # list.append(content.replace('\n',''))
                if content != '\xa0' and content != '':
                    content = content.replace('\n',' ')
                    sent = cut_sent(content, lang)
                    print('\n'.join(sent))
                    f.write('\n'.join(sent)+'\n')
                # text += a.text
    # print(list)
    html.close()


def parser(srt_path, tar_path, lang='zh'):
    if srt_path.endswith(".htm") or srt_path.endswith(".html"):
        path_html = srt_path
        html2txt(path_html, tar_path, lang)
    elif srt_path.endswith(".docx"):
        path_docx = srt_path
        path_html = docx2html(path_docx)
        html2txt(path_html, tar_path, lang)

        # os.remove(path_html)
    elif srt_path.endswith(".doc"):
        path_doc = srt_path
        path_docx = doc2docx(path_doc)
        path_html = docx2html(path_docx)
        html2txt(path_html, tar_path, lang)

        # os.remove(path_docx)
        # os.remove(path_html)
    else:
        print("Form not matched")
        return

    # html2txt(path_html, tar_path, lang)


if __name__ == '__main__':
    # html2txt('//h3c-infoserver/06-H3C-中文手册/01-生产归档/02-以太网交换机/00-电源手册/3101A0CV-20170615-H3C RPS800-A 用户手册-6PW101/中文上网专用/html/99-整本手册.htm','zh.txt')
    # path_info = '//h3c-infoserver/06-H3C-中文手册/01-生产归档/02-以太网交换机/00-电源手册/3101A0CV-20170615-H3C RPS800-A 用户手册-6PW101/英文上网专用/html/99-book.htm'
    # path_info = r'\\h3c-infoserver\06-H3C-中文手册\01-生产归档\02-以太网交换机\00-电源手册\3101A0CV-20170615-H3C RPS800-A 用户手册-6PW101\中文上网专用\html\99-整本手册.htm'

    path_info = r'\\h3c-infoserver\06-H3C-中文手册\01-生产归档\02-以太网交换机\00-电源手册\3101A0CV-20170615-H3C RPS800-A 用户手册-6PW101\06-正文.docx'
    # path_info = r'\\h3c-infoserver\06-H3C-中文手册\01-生产归档\02-以太网交换机\00-电源手册\3101A0CV-20170615-H3C RPS800-A 用户手册-6PW101\03-Text.docx'
    # parser(path_info, 'zh.txt', lang = 'zh')
    parser(path_info, "zh_Text.zh", lang='zh')

