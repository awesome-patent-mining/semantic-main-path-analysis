"""
This code provides a series of basic functions for topic analysis of main path
"""

# Author: Liang Chen <squirrel_d@126.com>
# License: BSD 3 clause
from gensim import models
from semanticRoadMap import *
class PathTopic:
    def __init__(self, texts_serialAddress, pns_serialAddress, lsi_serializationAddress, dictionary_serialAddress, topic_num = 10):
        '''
        init PathTopic class
        :param texts_serialAddress: absolute path of texts serialization file
        :param pns_serialAddress: absolute path of patent NO file
        :param lsi_serializationAddress: absolute path of LSI model file
        :param dictionary_serialAddress: absolute path of dictionary file
        :param topic_num: topic number of LSI
        '''
        with open(texts_serialAddress, 'r') as f:
            self.texts = pickle.load(f)
        with open(pns_serialAddress, 'r') as f:
            self.pns = pickle.load(f)
        with open(lsi_serializationAddress, 'r') as f:
            self.index = pickle.load(f)
        with open(dictionary_serialAddress, 'r') as f:
            self.dictionary = pickle.load(f)
        corpus = [self.dictionary.doc2bow(text) for text in self.texts]
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        self.topic_number = topic_num;
        self.corpus_lsi_np = self.transformCorpusLsi2Numpy(self.index[corpus_tfidf])

    def transformCorpusLsi2Numpy(self,corpus_index):
        '''
        transform corpus
        :param corpus_index:
        :return: 2-D np array as np.zeros([corpus_index.__len__(),self.topic_number])
        '''
        # =
        doc_list_tmp = list()
        for doc in corpus_index:
            if len(doc)==0:
                doc_list_tmp.append([0.0 for i in range(self.topic_number)])
            else:
                doc_list_tmp.append([i[1] for i in doc])

        corpus_index_np = np.array(doc_list_tmp)
        return corpus_index_np;

    def normalize(self,v):
        '''
        return normalized vector
        :param v: vector
        :return: normalized vector
        '''
        norm = np.linalg.norm(v)
        if norm ==0:
            return v
        return 1.0*v/norm
    def generatePathTopic(self,path):
        '''
        return semantic topic representation of a path
        :param path: DiGraph
        :return: 1D np array
        '''
        topic_list_tuple = list()
        for nodeID in path.nodes():
            topic_dis_tmp = self.corpus_lsi_np[nodeID-1]
            topic_list_tuple.append(topic_dis_tmp)
        topic_dis_array = np.vstack(tuple(topic_list_tuple))
        return self.normalize(topic_dis_array.sum(axis=0))