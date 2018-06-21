# -*- coding: utf-8 -*-
from NerAndClusering.entities.features.check_element_feature import CheckElementFeature


class PrefixFeature(CheckElementFeature):
    def __init__(self, prefixes, length):
        super().__init__('prefix', prefixes, lambda x: x[:length])
