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
    p5_country_df: DataFrame = p5_df[['ccode', 'country']].drop_duplicates()
    unido_p5_linkage_df: DataFrame = country_code.merge(p5_country_df, on=['country'], how='left')
    index_dict = {52: 812, 72: 775, 95: 732, 98: 365, 134: 818, 129: 2, 128: 510, 126: 696, 117: 652, 96: 359}
    for i in index_dict:
        unido_p5_linkage_df.loc[i, 'ccode'] = index_dict[i]

    unido_p5_linkage_df.to_pickle(os.path.join(const.TEMP_PATH, '20210613_unido_p5_linkage_file.pkl'))
