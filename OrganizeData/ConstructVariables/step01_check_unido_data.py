#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step01_check_unido_data
# @Date: 2021/6/12
# @Author: Mark Wang
# @Email: markwang@connect.hku.hk

"""
python -m OrganizeData.ConstructVariables.step01_check_unido_data
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    unido_df: DataFrame = pd.read_csv(os.path.join(const.DATABASE_PATH, 'UNIDO', 'data.csv'), header=0,
                                      names=['table_no', 'country_code', const.YEAR, 'ISIC', 'ISIC_combination',
                                             'value', 'table_definition_code', 'source_code', 'unit'])
    table_def_dict = {1: 'NumEstablishments', 2: 'NumEnterprises', 3: 'NumPersonEngaged', 4: 'NumEmployee',
                      5: 'Wages', 11: 'OutputBasicPrices', 12: 'OutputFactorValues', 13: 'OutputProducerPrices',
                      14: 'Output', 17: 'VABasicPrices', 18: 'VAFactorValues', 19: 'VAProducerPrices',
                      20: 'VA', 21: 'FixedCapital', 31: 'NumFemaleEmployee', 51: 'IndProductIndex'}

    union_df2: DataFrame = unido_df.loc[:,
                           ['country_code', const.YEAR, 'ISIC', 'value', 'table_definition_code']].copy()
    result_df = DataFrame()

    for key in table_def_dict:
        tmp_df: DataFrame = union_df2.loc[union_df2['table_definition_code'] == key].rename(
            columns={'value': table_def_dict[key]}).drop(['table_definition_code'], axis=1)
        if result_df.empty:
            result_df: DataFrame = tmp_df.copy()
        else:
            result_df: DataFrame = result_df.merge(tmp_df, on=['country_code', const.YEAR, 'ISIC'], how='outer')

    result_df2: DataFrame = result_df.replace(['...'], np.nan)
    for key in table_def_dict:
        result_df2.loc[:, table_def_dict[key]] = result_df2[table_def_dict[key]].astype(float)

    result_df3: DataFrame = result_df2.dropna(subset=table_def_dict.values(), how='all')
    result_df3.to_pickle(os.path.join(const.TEMP_PATH, '20210613_unido_panel_data.pkl'))
