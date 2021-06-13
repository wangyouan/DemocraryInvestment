#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step02_merge_unido_data_with_polity_v
# @Date: 2021/6/13
# @Author: Mark Wang
# @Email: markwang@connect.hku.hk

"""
python -m OrganizeData.ConstructVariables.step02_merge_unido_data_with_polity_v
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    country_code: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20210613_country_code_information.pkl'))
    p5_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20201210_p5_v2018.pkl')).drop_duplicates(
        subset=['scode', 'year'], keep='first').rename(
        columns={'scode': 'country_iso3'})
    p5_country_df: DataFrame = p5_df[['country_iso3', 'country']].drop_duplicates()
    unido_p5_linkage_df: DataFrame = country_code.merge(p5_country_df, on=['country'], how='left')
    index_dict = {'418': 'LAO', '104': 'MMR', '410': 'KOR', '643': 'RUS', '704': 'VNM', '158': 'TWN', '384': 'CIV',
                  '230': 'ETH', '278': 'DDR', '280': 'DEU', '840': 'USA', '834': 'TZA', '784': 'ARE', '760': 'SYR',
                  '498': 'MDA'}

    for i in index_dict:
        unido_p5_linkage_df.loc[unido_p5_linkage_df['country_code'] == i, 'country_iso3'] = index_dict[i]

    unido_p5_linkage_df.to_pickle(os.path.join(const.TEMP_PATH, '20210613_unido_p5_linkage_file.pkl'))
