
import pandas as pd


class Reference:

    def __init__(self, id2label: dict):

        self.__id2label = id2label


    def __get_frame(self):

        frame = pd.DataFrame.from_dict(self.__id2label, orient='index')
        frame.reset_index(drop=False, inplace=True)
        frame.rename(columns={'index': 'code', 0: 'name'}, inplace=True)

        return frame

    def __call__(self):
        """

        :return:
        """
        
        frame = self.__get_frame()

        splits = frame['name'].str.split(pat='-', n=1, expand=True)
        splits.rename(columns={0: 'parent', 1: 'branch'}, inplace=True)


        reference = frame.copy().join(splits, how='left')
