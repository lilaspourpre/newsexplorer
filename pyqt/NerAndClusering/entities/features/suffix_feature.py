# -*- coding: utf-8 -*-
from NerAndClusering.entities.features.check_element_feature import CheckElementFeature


class SuffixFeature(CheckElementFeature):
    def __init__(self, suffixes, length):
        super().__init__('suffix', suffixes, lambda x: x[-length:])
