import pandas as pd
import os
import random


class Processor:
    def __init__(self, csv_filename: str, number_of_group: int, group_names: list = None) -> None:
        self.__original_name = csv_filename.removesuffix('.csv')
        if not csv_filename.endswith('.csv'):
            raise KeyError("The filename must end with .csv and be in csv format")
        self.__df = pd.read_csv(csv_filename)
        if group_names is None or len(group_names) == 0:
            self.group_names = {i: str(i) for i in range(1, int(number_of_group) + 1)}
        elif len(group_names) == number_of_group:
            self.group_names = {i + 1: group_names[i] for i in range(number_of_group)}
        else:
            if len(group_names) != number_of_group:
                raise ValueError("Number of groups must be equal to the number of group names")
            else:
                raise ValueError("Unexpected Error")

    def get_group_names(self, group_num: int) -> list:
        return self.group_names[group_num]

    def make_a_group(self, prefix: str):
        """ Make a group and write to separate file with prefix"""

        i = 0

        if prefix.isspace() or len(prefix) == 0:
            file_name = f'{self.__original_name}'
            while os.path.exists(file_name + '.csv'):
                i += 1
                file_name = f'{self.__original_name}({i})'
        else:
            file_name = f'{prefix}_' + self.__original_name
            while os.path.exists(file_name + '.csv'):
                i += 1
                file_name = f'{prefix}_{self.__original_name}({i})'

        # calculate data for group quota
        total_num = len(self.__df)
        base = total_num // len(self.group_names)
        quota = {i: base for i in self.group_names.keys()}
        remains = total_num % len(self.group_names)
        if remains != 0:
            for i in range(1, remains + 1):
                group = i % len(self.group_names)
                if group == 0:
                    group = len(self.group_names)
                quota[group] += 1

        new_df = self.__df.copy()
        new_df['Group'] = new_df.apply(lambda _: self.group_names[self.__add_to_group(quota)], axis=1)
        new_df.to_csv(f'{file_name}.csv', index=False)

    def __add_to_group(self, group_quota: dict) -> int:
        group_choice = [i for i in self.group_names.keys() if group_quota[i] > 0]
        if len(group_choice) == 0:
            raise ValueError("Something went wrong! during grouping process")
        group = random.choice(group_choice)
        group_quota[group] -= 1
        return group
