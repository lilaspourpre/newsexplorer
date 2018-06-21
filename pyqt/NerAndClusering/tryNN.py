import texterra
import pymorphy2

from NerAndClusering.entities.document import Document
from NerAndClusering.entities.token import Token
from NerAndClusering.entities.tagged_token import TaggedToken
from NerAndClusering.entities.tagged_vector import TaggedVector
from NerAndClusering.feature_model_computer import compute_feature_and_model
from NerAndClusering.from_bilou import untag

class RuNER_NN():
    def __init__(self):
        self.t = texterra.API("c41d9b98960e6f6bdfb3452f6b174e5a6554f992")

    def process(self, text, textname):
        morph_analyzer = pymorphy2.MorphAnalyzer()
        tokenslist = list(self.t.tokenization(text, language="ru"))[0]
        print(tokenslist)
        test_documents = self.get_documents_without_tags_from(tokenslist, morph_analyzer, textname)
        feature, model = compute_feature_and_model()
        return self.toList(self.compute_nes(test_documents, feature, model), text)

    def toList(self, result, text):
        ne_list = []
        for i in range(len(result)):
            if result[i][0] == "PER":
                ne_list.append(text[result[i][1]:result[i][1] + result[i][2]])
        return ne_list

    def character_recognition(self, textname):
        if '.txt' not in textname:
            textname+='.txt'
        text = open(textname, 'r', encoding='utf-8').read()
        return self.process(text.strip(), textname)

    def compute_nes(self, documents, feature, model):
        dict_of_docs_with_vectors = self.create_dict_of_vectors_for_each_doc(documents, feature)
        for document_name, untagged_vectors_list in dict_of_docs_with_vectors.items():
            list_of_vectors = [untagged_vector.get_vector() for untagged_vector in untagged_vectors_list]
            split_lenghts = documents[document_name].get_sentences_lengths()
            ne_list = self.__define_nes(model, list_of_vectors, documents[document_name].get_tokens(), split_lenghts)
            return ne_list

    def __define_nes(self, model, vectors_list, tokens, split_lengths):
        list_of_tags = model.split_batch_predict(vectors_list, split_lengths)
        return untag(list_of_tags=list_of_tags, list_of_tokens=tokens)

    def get_documents_without_tags_from(self, tokenslist, morph_analyzer, textname):
        dict_of_documents = {}
        document = self.__create_document_from(tokenslist, morph_analyzer)
        dict_of_documents[textname] = document
        return dict_of_documents

    def __create_document_from(self, tokenslist, morph_analyzer):
        """
        :param filename: which document to parse (name without extension)
        :return: document class
        """
        tokens = self.__get_tokens_from(tokenslist)
        tagged_tokens = [TaggedToken(None, tokens[i]) for i in range(len(tokens))]
        document = Document(tagged_tokens, morph_analyzer=morph_analyzer)
        return document

    def __get_tokens_from(self, tokenslist):
        """
        :param filename: filename without extension (.tokens) to parse
        :return: list of token classes
        """
        tokens = []
        for i in range(len(tokenslist)):
            token = Token(tokenid=i, position=tokenslist[i][0],
                          length=tokenslist[i][1]-tokenslist[i][0], text=tokenslist[i][2])
            tokens.append(token)
        return tuple(tokens)

    def create_dict_of_vectors_for_each_doc(self, documents, feature):
        """
        :param documents:
        :param feature:
        :return:
        """
        dict_of_tagged_vectors_for_each_doc = {}
        for doc_id, document in documents.items():
            vectors_in_document = self.create_list_of_tagged_vectors({doc_id: document}, feature)
            dict_of_tagged_vectors_for_each_doc[doc_id] = vectors_in_document
        return dict_of_tagged_vectors_for_each_doc

    def create_list_of_tagged_vectors(self, documents, feature):
        """
        :param documents:
        :param feature:
        :return:
        """
        list_of_tagged_vectors = []

        for document in documents.values():
            for taggedtoken in document.get_tagged_tokens():
                list_of_tagged_vectors.append(self.__create_tagged_vector_for(taggedtoken, document, feature))
        return list_of_tagged_vectors

    def __create_tagged_vector_for(self, taggedtoken, document, feature):
        tag = taggedtoken.get_tag()
        vector = feature.compute_vector_for(taggedtoken.get_token(), document)
        return TaggedVector(vector=vector, tag=tag)



ner = RuNER_NN()
r = "Мама мыла  Инна рума. Раму мыла Кошка Марина мама Владимир Путин. Хе-хе"
dic = ner.process(r, "r")
print(dic)