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

import numpy as np
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    unido_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20210613_unido_panel_data.pkl'))
    unido_p5_linkage_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20210613_unido_p5_linkage_file.pkl'))
    unido_df.loc[:, 'country_code'] = unido_df['country_code'].astype(int)
    unido_p5_linkage_df.loc[:, 'country_code'] = unido_p5_linkage_df['country_code'].astype(int)
    unido_with_p5: DataFrame = unido_df.merge(unido_p5_linkage_df, on=['country_code'])

    p5_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20201210_p5_v2018.pkl')).drop_duplicates(
        subset=['scode', 'year'], keep='first').rename(
        columns={'scode': 'country_iso3', 'democ': 'DEMOC_POLITY_IV', 'autoc': 'AUTOC_POLITY_IV', 'parcomp': 'COMP_PAR',
                 'xropen': 'OPEN_EXEC_RCT', 'xrcomp': 'COMP_EXEC_RCT', 'xconst': 'CONS_EXEC', 'parreg': 'PART_REG',
                 'polity2': 'POLITY_IV_SCORE', 'xrreg': 'CHIEF_EXEC_REG', 'durable': 'DURABLE', 'exrec': 'EXE_RECRUIT',
                 'exconst': 'EXE_CONSTRAINT', 'polcomp': 'POL_COMPETITION'}).replace(
        [-66, -88, -99], np.nan).replace({-77: 0}).drop(
        ['p5', 'cyear', 'ccode', 'country', 'flag', 'fragment', 'polity', 'prior', 'emonth', 'eday', 'eyear', 'eprec',
         'interim', 'bmonth', 'bday', 'byear', 'bprec', 'post', 'change', 'd5', 'sf', 'regtrans'], axis=1)

    unido_with_p5.loc[:, 'dep_year'] = unido_with_p5[const.YEAR]
    unido_with_p5.loc[:, const.YEAR] -= 1
    unido_with_p5_df: DataFrame = unido_with_p5.merge(p5_df, on=['country_iso3', const.YEAR], how='left')

    # construct dependent variables
    for key in ['NumEstablishments', 'NumEnterprises', 'NumPersonEngaged', 'NumEmployee', 'Wages', 'OutputBasicPrices',
                'OutputFactorValues', 'OutputProducerPrices', 'Output', 'VABasicPrices', 'VAFactorValues',
                'VAProducerPrices', 'VA', 'FixedCapital', 'NumFemaleEmployee']:
        unido_with_p5_df.loc[:, 'ln{}'.format(key)] = unido_with_p5_df[key].apply(lambda x: np.log(x + 1))

    unido_with_p5_df.loc[:, 'FemaleRatio'] = unido_with_p5_df['NumFemaleEmployee'] / unido_with_p5_df['NumEmployee']
    unido_with_p5_df.loc[:, 'OutputPerEstab'] = unido_with_p5_df['Output'] / unido_with_p5_df['NumEstablishments']
    unido_with_p5_df.loc[:, 'OutputPPPerEstab'] = unido_with_p5_df['OutputProducerPrices'] / unido_with_p5_df[
        'NumEstablishments']
    unido_with_p5_df.loc[:, 'OutputFVPerEstab'] = unido_with_p5_df['OutputFactorValues'] / unido_with_p5_df[
        'NumEstablishments']
    unido_with_p5_df.loc[:, 'OutputBPPerEstab'] = unido_with_p5_df['OutputBasicPrices'] / unido_with_p5_df[
        'NumEstablishments']

    unido_with_p5_df.loc[:, 'VAPerEstab'] = unido_with_p5_df['VA'] / unido_with_p5_df['NumEstablishments']
    unido_with_p5_df.loc[:, 'VAPPPerEstab'] = unido_with_p5_df['VAProducerPrices'] / unido_with_p5_df[
        'NumEstablishments']
    unido_with_p5_df.loc[:, 'VAFVPerEstab'] = unido_with_p5_df['VAFactorValues'] / unido_with_p5_df[
        'NumEstablishments']
    unido_with_p5_df.loc[:, 'VABPPerEstab'] = unido_with_p5_df['VABasicPrices'] / unido_with_p5_df[
        'NumEstablishments']

    unido_with_p5_df.loc[:, 'OutputPerEnter'] = unido_with_p5_df['Output'] / unido_with_p5_df['NumEnterprises']
    unido_with_p5_df.loc[:, 'OutputPPPerEnter'] = unido_with_p5_df['OutputProducerPrices'] / unido_with_p5_df[
        'NumEnterprises']
    unido_with_p5_df.loc[:, 'OutputFVPerEnter'] = unido_with_p5_df['OutputFactorValues'] / unido_with_p5_df[
        'NumEnterprises']
    unido_with_p5_df.loc[:, 'OutputBPPerEnter'] = unido_with_p5_df['OutputBasicPrices'] / unido_with_p5_df[
        'NumEnterprises']

    unido_with_p5_df.loc[:, 'VAPerEnter'] = unido_with_p5_df['VA'] / unido_with_p5_df['NumEnterprises']
    unido_with_p5_df.loc[:, 'VAPPPerEnter'] = unido_with_p5_df['VAProducerPrices'] / unido_with_p5_df[
        'NumEnterprises']
    unido_with_p5_df.loc[:, 'VAFVPerEnter'] = unido_with_p5_df['VAFactorValues'] / unido_with_p5_df[
        'NumEnterprises']
    unido_with_p5_df.loc[:, 'VABPPerEnter'] = unido_with_p5_df['VABasicPrices'] / unido_with_p5_df[
        'NumEnterprises']

    unido_with_p5_df.loc[:, 'WagePerEmployee'] = unido_with_p5_df['Wages'] / unido_with_p5_df['NumEmployee']

    unido_with_p5_df.loc[:, 'OutputPerEmployee'] = unido_with_p5_df['Output'] / unido_with_p5_df['NumEmployee']
    unido_with_p5_df.loc[:, 'OutputPPPerEmployee'] = unido_with_p5_df['OutputProducerPrices'] / unido_with_p5_df[
        'NumEmployee']
    unido_with_p5_df.loc[:, 'OutputFVPerEmployee'] = unido_with_p5_df['OutputFactorValues'] / unido_with_p5_df[
        'NumEmployee']
    unido_with_p5_df.loc[:, 'OutputBPPerEmployee'] = unido_with_p5_df['OutputBasicPrices'] / unido_with_p5_df[
        'NumEmployee']

    unido_with_p5_df.loc[:, 'VAPerEmployee'] = unido_with_p5_df['VA'] / unido_with_p5_df['NumEmployee']
    unido_with_p5_df.loc[:, 'VAPPPerEmployee'] = unido_with_p5_df['VAProducerPrices'] / unido_with_p5_df[
        'NumEmployee']
    unido_with_p5_df.loc[:, 'VAFVPerEmployee'] = unido_with_p5_df['VAFactorValues'] / unido_with_p5_df[
        'NumEmployee']
    unido_with_p5_df.loc[:, 'VABPPerEmployee'] = unido_with_p5_df['VABasicPrices'] / unido_with_p5_df[
        'NumEmployee']

    unido_with_p5_df.loc[:, 'OutputPerCapital'] = unido_with_p5_df['Output'] / unido_with_p5_df['FixedCapital']
    unido_with_p5_df.loc[:, 'OutputPPPerCapital'] = unido_with_p5_df['OutputProducerPrices'] / unido_with_p5_df[
        'FixedCapital']
    unido_with_p5_df.loc[:, 'OutputFVPerCapital'] = unido_with_p5_df['OutputFactorValues'] / unido_with_p5_df[
        'FixedCapital']
    unido_with_p5_df.loc[:, 'OutputBPPerCapital'] = unido_with_p5_df['OutputBasicPrices'] / unido_with_p5_df[
        'FixedCapital']

    unido_with_p5_df.loc[:, 'VAPerCapital'] = unido_with_p5_df['VA'] / unido_with_p5_df['FixedCapital']
    unido_with_p5_df.loc[:, 'VAPPPerCapital'] = unido_with_p5_df['VAProducerPrices'] / unido_with_p5_df[
        'FixedCapital']
    unido_with_p5_df.loc[:, 'VAFVPerCapital'] = unido_with_p5_df['VAFactorValues'] / unido_with_p5_df[
        'FixedCapital']
    unido_with_p5_df.loc[:, 'VABPPerCapital'] = unido_with_p5_df['VABasicPrices'] / unido_with_p5_df[
        'FixedCapital']
    unido_with_p5_df2: DataFrame = unido_with_p5_df.replace([np.inf, -np.inf], np.nan)
    unido_with_p5_df.to_stata(os.path.join(const.RESULT_PATH, '20210614_unido_p5_regression_data.dta'),
                              write_index=False)
