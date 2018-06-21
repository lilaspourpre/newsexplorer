from itertools import product

import os
from gensim.models import FastText

from NerAndClusering.entities.features.composite import FeatureComposite
from NerAndClusering.entities.features.part_of_speech import POSFeature
from NerAndClusering.entities.features.length import LengthFeature
from NerAndClusering.entities.features.numbers import NumbersInTokenFeature
from NerAndClusering.entities.features.case import CaseFeature
from NerAndClusering.entities.features.morpho_case import MorphoCaseFeature
from NerAndClusering.entities.features.context_feature import ContextFeature
from NerAndClusering.entities.features.special_chars import SpecCharsFeature
from NerAndClusering.entities.features.letters import LettersFeature
from NerAndClusering.entities.features.df import DFFeature
from NerAndClusering.entities.features.position_in_sentence import PositionFeature
from NerAndClusering.entities.features.not_in_stop_words import StopWordsFeature
from NerAndClusering.entities.features.case_concordance import ConcordCaseFeature
from NerAndClusering.entities.features.punctuation import PunctFeature
from NerAndClusering.entities.features.prefix_feature import PrefixFeature
from NerAndClusering.entities.features.suffix_feature import SuffixFeature
from NerAndClusering.entities.features.if_no_lowercase import LowerCaseFeature
from NerAndClusering.entities.features.gazetteer import GazetterFeature
from NerAndClusering.entities.features.embedding_feature import EmbeddingFeature
from NerAndClusering.entities.rnn_model import RNNModel
import pickle
import tensorflow as tf


def compute_feature_and_model():
    tags = compute_tags()
    embedding_model = None
    affixes = get_affixes()
    feature = get_composite_feature(2, affixes, 2, embedding_model)
    session = tf.Session()
    path = os.path.join("NerAndClusering")
    saver = tf.train.import_meta_graph(os.path.join(path, "rnn_model_2018.06.20-17.40.52",'rnn_model_2018.06.20-17.40.52.meta'))
    saver.restore(session, tf.train.latest_checkpoint(os.path.join(path, "rnn_model_2018.06.20-17.40.52")))
    #op = session.graph.get_operations()
    #print([m.values() for m in op])
    graph = tf.get_default_graph()
    x = graph.get_tensor_by_name("x:0")
    seqlen = graph.get_tensor_by_name("seqlen:0")
    outputs = graph.get_tensor_by_name("fc/BiasAdd:0")
    model = RNNModel(session, outputs, x, seqlen, tags, saver)
    return feature, model


def get_model_for_embeddings(model_path):
    model = FastText.load_fasttext_format(model_path)
    return model


def get_affixes():
    path = os.path.join("NerAndClusering", "affixes")
    with open(os.path.join(path, "prefixes.pickle"), 'rb') as pref:
        prefixes = pickle.load(pref)
    with open(os.path.join(path, "suffixes.pickle"), 'rb') as suf:
        suffixes = pickle.load(suf)
    return {"prefix": prefixes, "suffix": suffixes}


def compute_tags():
    tags = ["PER", "LOC", "ORG"]
    bilou = ["B", "I", "L", "U"]
    list_of_tags = ["O"]
    list_of_tags += [''.join(i) for i in product(bilou, tags)]
    return list_of_tags


def get_composite_feature(window, affixes, ngram_affixes, embedding_model):
    """
    Adding features to composite
    :return: composite (feature storing features)
    """
    list_of_features = [LengthFeature(), NumbersInTokenFeature(), PositionFeature(), DFFeature(), ConcordCaseFeature(),
                        GazetterFeature(), LowerCaseFeature(), SpecCharsFeature(),
                        StopWordsFeature()]#, EmbeddingFeature(embedding_model)]

    list_of_features.append(PrefixFeature(affixes["prefix"], ngram_affixes))
    list_of_features.append(SuffixFeature(affixes["suffix"], ngram_affixes))

    basic_features = [POSFeature(), CaseFeature(), MorphoCaseFeature(), LettersFeature(), PunctFeature()]
    for feature in basic_features:
        for offset in range(-window, window + 1):
            list_of_features.append(ContextFeature(feature, offset))
    composite = FeatureComposite(list_of_features)
    return composite

