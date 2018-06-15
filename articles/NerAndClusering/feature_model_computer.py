from itertools import product

from gensim.models import FastText

from entities.features.composite import FeatureComposite
from entities.features.part_of_speech import POSFeature
from entities.features.length import LengthFeature
from entities.features.numbers import NumbersInTokenFeature
from entities.features.case import CaseFeature
from entities.features.morpho_case import MorphoCaseFeature
from entities.features.context_feature import ContextFeature
from entities.features.special_chars import SpecCharsFeature
from entities.features.letters import LettersFeature
from entities.features.df import DFFeature
from entities.features.position_in_sentence import PositionFeature
from entities.features.not_in_stop_words import StopWordsFeature
from entities.features.case_concordance import ConcordCaseFeature
from entities.features.punctuation import PunctFeature
from entities.features.prefix_feature import PrefixFeature
from entities.features.suffix_feature import SuffixFeature
from entities.features.if_no_lowercase import LowerCaseFeature
from entities.features.gazetteer import GazetterFeature
from entities.features.embedding_feature import EmbeddingFeature
from entities.rnn_model import RNNModel

import tensorflow as tf


def compute_feature_and_model():
    tags = compute_tags()
    embedding_model = None
    affixes = get_affixes()
    feature = get_composite_feature(2, affixes, 2, embedding_model)
    saver = tf.train.Saver()
    with tf.Session() as session:
        initialize(session)

    model = RNNModel(session, outputs, x, seqlen, tags, saver)
    return feature, model

def initialize(session):
    tf.train.Saver().restore(session, "rnn_model_2018.06.05-13.49.09" + '/variables/variables')


def get_model_for_embeddings(model_path):
    model = FastText.load_fasttext_format(model_path)
    return model

def get_affixes():
    return {"prefix": set(), "suffix": set()}

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

