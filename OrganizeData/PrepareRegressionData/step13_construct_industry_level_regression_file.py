#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step13_construct_industry_level_regression_file
# @Date: 2021/6/13
# @Author: Mark Wang
# @Email: markwang@connect.hku.hk

"""
python -m OrganizeData.PrepareRegressionData.step11_construct_pension_cost_information
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    unido_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20210613_unido_panel_data.pkl'))
    unido_p5_linkage_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20210613_unido_p5_linkage_file.pkl'))
    unido_df.loc[:, 'country_code'] = unido_df['country_code'].astype(int)
    unido_p5_linkage_df.loc[:, 'country_code'] = unido_p5_linkage_df['country_code'].astype(int)
    unido_with_p5: DataFrame = unido_df.merge(unido_p5_linkage_df, on=['country_code'])
