# coding:utf-8

f_zh = open("zh_info.txt", "w", encoding="utf-8")
f_en = open("en_info.txt", "w", encoding="utf-8")

with open('02.txt', 'r', encoding="utf-8") as f:
    for line in f.readlines():
        print(line)
        zh_text, en_text = line.strip().split("\t")[2:4]
        f_zh.write(zh_text + '\n')
        f_en.write(en_text + '\n')


f_zh.close()
f_en.close()
