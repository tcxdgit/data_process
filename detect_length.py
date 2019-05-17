# coding:utf-8
"""
对平行语料的长度进行检测
剔除长度差别过大的
"""
import jieba
import nltk
import re

corpus_path = "D:\\Data\\nmt\\zh_en_del3.txt"

with open(corpus_path, "r", encoding="utf-8") as f_corpus:
    count = 0
    for line in f_corpus.readlines():
        zh, en, _ = line.strip().split("\t")

        zh_cws = []

        # 避免切开连接的英语单词
        # english_words = re.findall('[a-zA-Z0-9_-]+', zh)
        pattern = re.compile(r"[a-zA-Z0-9_-]+")

        r = re.search(pattern, zh)
        print(r)
        if r:
            print(r.span())
            print(r.group())

        # for w in english_words:
        #     jieba.suggest_freq(w, tune=True)





        for w in jieba.cut(zh.strip("【】")):
            if w.strip():
                zh_cws.append(w.strip())

        # print(zh_cws)
        zh_len = len(zh_cws)

        en_token = nltk.word_tokenize(en)
        # print(en_token)
        en_len = len(en_token)

        if en_len:
            ratio = float(zh_len) / en_len
        else:
            ratio = 0

        if ratio > 3 or ratio < 0.3:
            count += 1
            print(line)
            print(zh_cws)
            print(en_token)
            print("ratio: {}. not normal !!!".format(ratio))

            print("\n")

print(count)
