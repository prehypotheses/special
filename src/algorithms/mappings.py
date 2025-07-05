"""Module mappings.py"""
import logging

import pandas as pd


class Mappings:
    """
    Extracting a mix of fine & coarse labels
    """

    def __init__(self, reference: pd.DataFrame, preference: pd.DataFrame):
        """

        :param reference:
        :param preference:
        """

        self.__reference = reference
        self.__preference = preference

    def __grains(self, grain: str):
        """

        :param grain:
        :return:
        """

        return self.__reference.loc[self.__reference['parent'].isin(grain), :]

    def __coarse(self):
        """

        :return:
        """

        grains = self.__grains(grain='coarse')

        # Focusing on the coarse labels of interest
        instances = grains[['code', 'parent']].merge(
            self.__preference[['identifier', 'name']], left_on='parent', right_on='name')

        # The fields of interest are `code`, `identifier`, `name`
        instances.drop(columns='parent', inplace=True)
        logging.info('COARSE:\n%s', instances)

        return instances

    def __fine(self):
        """

        :return:
        """

        grains = self.__grains(grain='fine')

        # Focusing on the coarse labels of interest
        instances = grains[['code', 'name']].merge(
            self.__preference[['identifier', 'name']], how='left', on='name')
        instances['identifier'] = instances['identifier'].fillna(value=0).astype(int).values
        logging.info('FINE:\n%s', instances)

        return instances

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        mappings = pd.concat([self.__fine(), self.__coarse()], ignore_index=True)

        return mappings
