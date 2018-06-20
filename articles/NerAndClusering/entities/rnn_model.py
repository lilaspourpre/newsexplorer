# -*- coding: utf-8 -*-
import os
import time
import tensorflow as tf
from entities.model import Model
from wrapper import complement_data, format_data


class RNNModel(Model):
    def __init__(self, session, outputs, x, seqlen, tags, saver):
        super().__init__()
        self.session = session
        self.x = x
        self.outputs = outputs
        self.seqlen = seqlen
        self.tags = tags
        self.saver = saver

    def split_batch_predict(self, list_of_vectors, division):
        splitted_vectors, seqlen_list = format_data(list_of_vectors, division)
        array_of_vectors = complement_data(splitted_vectors)
        correct_prediction = tf.argmax(self.outputs, 2)

        index_list, output___ = self.session.run([correct_prediction, self.outputs],
                                                  feed_dict = {self.x: array_of_vectors,
                                                               self.seqlen: seqlen_list})
        return [self.tags[index_list[j][i]] for j in range(len(index_list)) for i in range(seqlen_list[j])]

    def __repr__(self):
        return 'rnn_model'

    def save_model(self, path):
        save_path = os.path.join(path, '{}_{}'.format(self.__repr__(), time.strftime('%Y.%m.%d-%H.%M.%S')))
        model_saver = tf.saved_model.builder.SavedModelBuilder(save_path)
        model_saver.add_meta_graph_and_variables(
            self.session,
            [tf.saved_model.tag_constants.SERVING])
        model_saver.save()
        print("Model saved to {}".format(save_path))

