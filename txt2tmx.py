'''
-*- coding: utf-8 -*-
@Author  :wu jiefang
@Time    : 2019/2/21 17:42
@Software: PyCharm
@Email   :wu.jiefang@h3c.com    
@File    : txt2tmx.py
'''
head = '''
<tmx version="1.4">
  <header
    creationtool="XYZTool" creationtoolversion="1.01-023"
    datatype="PlainText" segtype="sentence"
    adminlang="en-us" srclang="en"
    o-tmf="ABCTransMem"/>
  <body>
  '''
tail = '''
  </body>
</tmx>'''
import chardet

# f = open('C:\\Users\w19975\Documents\\translor-toolkit\en.txt','rb')
#
# data = f.read()
# print(data)
# print(chardet.detect(data).get("encoding"))
#

def txt2tml(zh_path,en_path,add=0):
   zh_file = open(zh_path,encoding='utf-8')
   en_file = open(en_path,encoding='utf-8')
   zh_data = zh_file.readlines()
   en_data = en_file.readlines()
   assert len(zh_data)==len(en_data)
   str = ''
   data =''
   for i in range(len(zh_data)):
       str += '''
    <tu>
      <tuv xml:lang="zh-Hans">
        <seg>''' + zh_data[i].strip('\n') + '''</seg>
      </tuv>
      <tuv xml:lang="en">
        <seg>''' + en_data[i].strip('\n') + '''</seg>
      </tuv>
    </tu>'''
   if add == 0:
       with open('./zh_en.tmx','w',encoding='utf-8') as f_w:
       # f_w = open('./zh_en.tmx','w',encoding='utf-8')

           f_w.write(head + str + tail)
   else:
       with open('./zh_en.tmx','r',encoding='utf-8') as f_r:
           lines = f_r.readlines()
           for line in lines[:-2]:
               data += line
               # print(data)
               # print(type(data))
           with open('./zh_en.tmx', 'w', encoding='utf-8') as f_w:
                   f_w.write(data + str + tail)


   zh_file.close()
   en_file.close()
           # for line in f_w.readlines()[:-3]:
           #      data += line
           # print(data)
            # f_w.write(data + str + tail)



   # print(zh_data[1])

if __name__=='__main__':
    add = 0
    txt2tml('C:\\Users\w19975\Documents\\translor-toolkit\zh.txt','C:\\Users\w19975\Documents\\translor-toolkit\en.txt',add=add)