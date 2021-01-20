import os, sys, json
import pandas as pd
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.models.word2vec import Word2Vec

if __name__ == "__main__":
    
    # get path
    sys_path = sys.path[0]
    sep = sys_path.find("src")
    file_path = sys_path[0:sep]
    w2v_path = os.path.join(file_path, "data", "corpus_w2v.bin")
    lex_path = os.path.join(file_path, "lexicon", "emolex", "emolex_raw.txt")
    save_path = os.path.join(file_path, "lexicon", "emolex", "emolex.tsv")
    info_path = os.path.join(file_path, "lexicon", "emolex", "emolex_info.csv")
    f = open(save_path, "w")
    f_info = open(info_path, "w")
    f_info.write("type,token,count,origin\n")
    w2v = Word2Vec.load(w2v_path)
    
    # read file
    d = pd.read_csv(lex_path, sep = "\t")
    wnl = WordNetLemmatizer()
    type_box = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust", "negative", "positive"]
    for type in type_box:
        type_lem = wnl.lemmatize(type, "n")
        type_lem = wnl.lemmatize(type_lem, "v")
        f.write(type_lem)
        tmp = d[d["type"] == type]
        tmp = tmp[tmp["label"] == 1]
        tokens = tmp["token"].values
        tokens = [wnl.lemmatize(token, "n") for token in tokens] # lemmatization noun
        tokens = [wnl.lemmatize(token, "v") for token in tokens] # lemmatization verb
        tokens = list(set(tokens))
        to_save_list = []
        for token in tokens:
            if token in w2v.wv:
                to_save_list.append((token, str(w2v.wv.vocab[token].count), "original"))
                similars = w2v.wv.most_similar(token, topn = 20)
                for similar in similars:
                    if similar[1] >= 0.9 and similar[0] not in tokens:
                        to_save_list.append((similar[0], str(w2v.wv.vocab[similar[0]].count), "added"))
        to_save_list = list(set(to_save_list))
        for to_save in to_save_list:
            f.write("\t" + to_save[0])
            f_info.write(type + "," + to_save[0] + "," + to_save[1] + "," + to_save[2] + "\n")
        f.write("\n")
    f.close()
    f_info.close()
