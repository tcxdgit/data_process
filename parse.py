
from bs4 import BeautifulSoup
import re
import nltk

def cut_sent(para,lang='zh'):
    if lang == 'zh':
        para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
        para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
        para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
        para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
        # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
        para = para.rstrip().split("\n")  # 段尾如果有多余的\n就去掉它
        # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    elif lang == 'en':
        para = nltk.sent_tokenize(para)
        # print(para)

    return para


def html2txt(srt_path,tar_path,lang='zh'):
    #中文文本
    if lang == 'zh':
        encode = 'gb2312'
        html = open(srt_path,encoding=encode)
    #英文文本
    elif lang == 'en':
        encode = 'windows-1252'
        html = open(srt_path,encoding=encode)
    # html = html.read()
    soup = BeautifulSoup(html,'html.parser')
    # print(soup.text.strip())英
    list = []
    # text = ''
    # with open('99.txt','w',encoding='utf-8') as f:
    with open(tar_path,'w',encoding='utf-8') as f:
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


if __name__ == '__main__':
    # html2txt('//h3c-infoserver/06-H3C-中文手册/01-生产归档/02-以太网交换机/00-电源手册/3101A0CV-20170615-H3C RPS800-A 用户手册-6PW101/中文上网专用/html/99-整本手册.htm','zh.txt')
    html2txt('//h3c-infoserver/06-H3C-中文手册/01-生产归档/02-以太网交换机/00-电源手册/3101A0CV-20170615-H3C RPS800-A 用户手册-6PW101/英文上网专用/html/99-book.htm','en.txt',lang = 'en')