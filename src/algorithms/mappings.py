import pandas as pd

class Mappings:

    def __init__(self, reference: pd.DataFrame, preference: pd.DataFrame, arguments: dict):

        self.__reference = reference
        self.__preference = preference
        self.__arguments = arguments

    def __grains(self, grain: str):

        return self.__reference.loc[self.__reference['parent'].isin(grain), :]

    def exc(self):

        # Linear
        coarse = self.__grains(grain='coarse')
        linear = coarse[['code', 'parent']].merge(
            self.__preference[['identifier', 'name']], left_on='parent', right_on='name')
        linear.drop(columns='parent', inplace=True)


        # Intricate
        fine = self.__grains(grain='fine')
        intricate = fine[['code', 'name']].merge(
            self.__preference[['identifier', 'name']], how='left', on='name')
        intricate['identifier'] = intricate['identifier'].fillna(value=0).astype(int).values

        mappings = pd.concat([intricate, linear], ignore_index=True)
