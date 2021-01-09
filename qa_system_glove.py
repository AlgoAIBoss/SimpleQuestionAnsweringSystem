from sklearn.metrics.pairwise import cosine_similarity
from utils import question_list, answer_list, preprocessing_corpus, word_segmentation, get_sentence_vector
import pickle
import numpy as np

# 导入GloVe向量化后的问题列表
vectorized_question_list = pickle.load(open('model/vectorized_question_list_glove.pkl', 'rb'))
# 导入向量化器
vectorizer = pickle.load(open('model/vectorizer.pkl', 'rb'))
# 导入倒排表索引
inverted_index = pickle.load(open('model/inverted_index.pkl', 'rb'))
# 导入GloVe中的词头
glove_words = pickle.load(open('model/glove_words.pkl', 'rb'))
# 导入GloVe矩阵
embeddings = pickle.load(open('model/glove_embeddings.pkl', 'rb'))


def get_answers_glove_optimized(input_question):
    # 假设问题列表中第一项为匹配的问句，取绝对值便于后续进行对比
    abs_vec = abs(vectorized_question_list[0])
    # 初始化结果索引列表
    res = []
    # 对输入的问题进行倒排表索引的匹配
    index_list = []
    for sentence in word_segmentation([input_question]):
        for word in sentence:
            if word in inverted_index.keys():
                index_list += inverted_index[word]
    # 对匹配的索引进行去重
    index_list = list(set(index_list))
    # 对输入的问题进行预处理
    preprocessed_input_question = preprocessing_corpus([input_question])
    # 计算输入的问题的向量
    vectorized_input_question = get_sentence_vector(preprocessed_input_question[0], glove_words, embeddings, 100)
    # 计算余弦相似度
    res = cosine_similarity([np.asarray(vectorized_input_question)], vectorized_question_list[index_list])[0]
    res_index = res.argsort()[-5:].tolist()[::-1]
    for index in res_index:
        print(question_list[index], answer_list[index])


get_answers_glove_optimized('''In which decade did Beyonce become famous''')
print('----------')
get_answers_glove_optimized('''What areas did Beyonce compete in when she was growing up?''')
print('----------')
get_answers_glove_optimized('''What was the latest version of iTunes as of mid-2015?''')
print('----------')
get_answers_glove_optimized('''What products were exported along with indigo from the Lowcountry?''')
print('----------')
get_answers_glove_optimized('''What supply port was opened late in 1944?''')
