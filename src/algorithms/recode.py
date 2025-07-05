"""Module recode.py"""
import pandas as pd
import datasets


class Recode:
    """
    This class recodes the fine entity tags; the old tags that are not of interest are set
    to zero, i.e., miscellaneous/other.  Whilst the tags of interest are assigned new codes.
    """

    def __init__(self, mappings: pd.DataFrame, features: datasets.Features):
        """

        :param mappings:
        :param features:
        """

        self.__recode = mappings.set_index(keys='code')['identifier'].to_dict()
        self.__features = features

    def __call__(self, feed: datasets.arrow_dataset.Dataset) -> datasets.arrow_dataset.Dataset:
        """

        :param feed:
        :return:
        """

        frame = feed.to_pandas()
        frame.drop(columns='ner_tags', inplace=True)
        frame['fine_ner_tags'] = frame['fine_ner_tags'].apply(lambda x: list(map(self.__recode.get, x)))

        return datasets.Dataset.from_pandas(frame, self.__features)
