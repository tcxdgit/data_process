import nltk
from nltk.translate.bleu_score import sentence_bleu
import random
import os

# score = sentence_bleu(ref, can)


def load_data(parallel_path):
    zh_sentences = []
    en_sentences = []
    # parallel_path = "/tcxia/data_process/training-parallel-nc-v13"
    for file in os.listdir(parallel_path):
        if file.endswith("zh-en.zh"):
            print("Read {}".format(file))
            with open(os.path.join(parallel_path, file), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    zh_sentences.append(line.strip())
        elif file.endswith("zh-en.en"):
            print("Read {}".format(file))
            with open(os.path.join(parallel_path, file), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    en_sentences.append(line.strip())

    return zh_sentences, en_sentences


def create_samples(zh_sentences, en_sentences):

    assert len(zh_sentences) == len(en_sentences)

    length_sentence = len(zh_sentences)

    results = dict()

    for i, s_zh in enumerate(zh_sentences):

        # s_zh_wc = jieba
        # s_zh_list = jieba.cut(s_zh)  # 默认是精确模式
        # print(", ".join(seg_list))

        pos_en = en_sentences[i]
        pos_en_list = nltk.sent_tokenize(pos_en)
        pos_en_list_2 = [pos_en_list]

        indices = random.sample(range(length_sentence), 20)
        # if i in indices:
        #     indices.remove(indices[i])

        lowest_score = 100
        for _i in indices:
            tmp_s_en = en_sentences[_i]
            tmp_s_en_list = nltk.sent_tokenize(tmp_s_en)
            score = sentence_bleu(pos_en_list_2, tmp_s_en_list)
            if score < lowest_score:
                lowest_score = score
                neg_en = tmp_s_en

        print(lowest_score, s_zh, neg_en)

        results[s_zh] = [pos_en, neg_en]

    return results


def main(parallel_path, output_dir):
    zh_sentences, en_sentences = load_data(parallel_path)
    results = create_samples(zh_sentences, en_sentences)
    count = len(results)

    counts = random.sample(range(count), 2500)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    f_train = open(os.path.join(output_dir, "train.tsv"), "w", encoding="utf-8")
    f_dev = open(os.path.join(output_dir, "dev.tsv"), "w", encoding="utf-8")
    for i, (s_zh, v) in enumerate(results.items()):
        pos_en, neg_en = v
        if i in counts:
            f_dev.write("1\t{}\t{}\n".format(s_zh, pos_en))
            f_dev.write("0\t{}\t{}\n".format(s_zh, neg_en))
        else:
            f_train.write("1\t{}\t{}\n".format(s_zh, pos_en))
            f_train.write("0\t{}\t{}\n".format(s_zh, neg_en))

    f_train.close()
    f_dev.close()


if __name__ == '__main__':
    main(parallel_path="/tcxia/data_process/training-parallel-nc-v13",
         output_dir="dataset")



