import logging
import datasets
import pandas as pd

import config
import src.elements.master as mr
import src.elements.s3_parameters as s3p

import src.algorithms.reference as rf
import src.algorithms.preference as pf
import src.algorithms.mappings
import src.algorithms.recode


class Interface:

    def __init__(self, master: mr.Master, s3_parameters: s3p.S3Parameters, arguments: dict):

        self.__data: datasets.DatasetDict = master.data
        self.__s3_parameters = s3_parameters
        self.__arguments: dict = arguments

        self.__configurations = config.Config()

    @staticmethod
    def __get_features(preference: pd.DataFrame) -> datasets.Features:

        classes = preference['label'].tolist()

        features = datasets.Features(
            {'id': datasets.Value('string', id=None),
             'tokens': datasets.Sequence(feature=datasets.Value(dtype='string', id=None), length=-1, id=None),
             'fine_ner_tags': datasets.Sequence(feature=datasets.ClassLabel(names=classes), length=-1, id=None)
             })

        return features

    def __persist(self, packets: datasets.DatasetDict):
        """

        :param packets:
        :return:
        """

        dataset_dict_path = 's3://' + self.__s3_parameters.internal + '/' + self.__configurations.destination
        packets.save_to_disk(dataset_dict_path=dataset_dict_path)

        logging.info('The special datasets.DatasetDict has been written to prefix: %s',
                     self.__configurations.destination)

    def exc(self):

        # Preference
        preference = pf.Preference(
            arguments=self.__arguments).__call__()

        # Reference
        reference = rf.Reference(id2label=self.__arguments.get('id2label'))

        # Mapping the old set up, reference, to the tags in focus, preference
        mappings = src.algorithms.mappings.Mappings(
            reference=reference(), preference=preference).exc()

        # The datasets.Features
        features = self.__get_features(preference=preference)

        # Recoding
        recode = src.algorithms.recode.Recode(mappings=mappings, features=features)
        packets = datasets.DatasetDict({
            'train': recode(feed=self.__data['train']),
            'validation': recode(feed=self.__data['validation']),
            'test': recode(feed=self.__data['test'])
        })
        logging.info(packets)

        self.__persist(packets=packets)
