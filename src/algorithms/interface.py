import datasets
import pandas as pd

import src.elements.master as mr

import src.algorithms.reference as rf
import src.algorithms.preference as pf
import src.algorithms.mappings
import src.algorithms.recode


class Interface:

    def __init__(self, master: mr.Master, arguments: dict):

        self.__data: datasets.DatasetDict = master.data
        self.__arguments: dict = arguments

    @staticmethod
    def __get_features(preference: pd.DataFrame) -> datasets.Features:

        classes = preference['label'].tolist()

        features = datasets.Features(
            {'id': datasets.Value('string', id=None),
             'tokens': datasets.Sequence(feature=datasets.Value(dtype='string', id=None), length=-1, id=None),
             'fine_ner_tags': datasets.Sequence(feature=datasets.ClassLabel(names=classes), length=-1, id=None)
             })

        return features

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

        datasets.DatasetDict({
            'train': recode(feed=self.__data['train']),
            'validation': recode(feed=self.__data['validation']),
            'test': recode(feed=self.__data['test'])
        })


