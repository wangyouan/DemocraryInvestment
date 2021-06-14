#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step14_append_other_country_control_variables
# @Date: 2021/6/14
# @Author: Mark Wang
# @Email: markwang@connect.hku.hk

"""
python -m OrganizeData.PrepareRegressionData.step14_append_other_country_control_variables
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    reg_df: DataFrame = pd.read_stata(os.path.join(const.RESULT_PATH, '20210614_unido_p5_regression_data.dta'))

    # construct regime change dummy
    reg_p5_df: DataFrame = reg_df.loc[:, ['country_iso3', 'DEMOC_POLITY_IV']].dropna(how='any').drop_duplicates()
    regime_change_df: DataFrame = reg_p5_df.groupby('country_iso3')['DEMOC_POLITY_IV'].count().reset_index(drop=False)
    regime_change_df.loc[:, 'REGIME_CHANGE'] = (regime_change_df['DEMOC_POLITY_IV'] > 1).astype(int)
    reg_df_regime_change: DataFrame = reg_df.merge(regime_change_df.loc[:, ['country_iso3', 'REGIME_CHANGE']],
                                                   on=['country_iso3'], how='left')

    # append some country level control variables
    # Load Data (CNTS) -- Unrest
    cnts_df = pd.read_excel(os.path.join(const.DATA_PATH, '2020 Special Student Edition (data thu 2016).xlsx'),
                            usecols=['World Bank Code', 'Year', 'Riots'])[1:].rename(
        columns={'World Bank Code': 'country_iso3', 'Year': const.YEAR, 'Riots': 'DOMESTIC_UNREST'})
    cnts_df.loc[:, 'country_iso3'] = cnts_df.loc[:, 'country_iso3'].replace({'SIN': 'SGP', 'ROM': 'ROU', 'SER': 'SRB'})
    cnts_df.loc[:, 'year'] = cnts_df['year'].astype(int)
    cnts_df.loc[:, 'DOMESTIC_UNREST'] = cnts_df['DOMESTIC_UNREST'].astype(int)
    cnts_df.loc[:, 'DOMESTIC_UNREST_DUMMY'] = (cnts_df.loc[:, 'DOMESTIC_UNREST'] > 0).astype(int)
    cnts_df.to_pickle(os.path.join(const.TEMP_PATH, '20210614_domestic_unrest_data.pkl'))

    reg_df_cnts: DataFrame = reg_df_regime_change.merge(cnts_df, on=['country_iso3', const.YEAR], how='left')

    # Load country level control variables
    country_control_df = pd.read_pickle(os.path.join(const.DATA_PATH, 'country_control.pkl')).rename(
        columns={'loc': 'country_iso3'})

    reg_df_control: DataFrame = reg_df_cnts.merge(country_control_df, on=[const.YEAR, 'country_iso3'], how='left')
    reg_df_control.to_stata(os.path.join(const.RESULT_PATH, '20210614_unido_p5_with_ctrl.dta'), write_index=False)
