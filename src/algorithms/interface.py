import datasets
import pandas as pd

import src.elements.master as mr

import src.algorithms.reference as rf
import src.algorithms.preference as pf
import src.algorithms.mappings

class Interface:

    def __init__(self, master: mr.Master, arguments: dict):

        self.__master = master
        self.__arguments = arguments

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

        preference = pf.Preference(
            arguments=self.__arguments).__call__()

        reference = rf.Reference(
            id2label=self.__arguments.get('id2label')).__call__()

        mappings = src.algorithms.mappings.Mappings(
            reference=reference, preference=preference).exc()
