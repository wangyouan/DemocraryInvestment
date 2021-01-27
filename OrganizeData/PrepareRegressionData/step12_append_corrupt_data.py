#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step12_append_corrupt_data
# @Date: 2021/1/26
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
ti_cpi: Corruption Perceptions Index. Scale of 0-100 where a 0 equals the highest level of perceived corruption
and 100 equals the lowest level of perceived corruption.

ti_cpi_om: Corruption Perceptions Index (Old methodology). Scale of 0-10 where a 0 equals the highest level of
perceived corruption and 10 equals the lowest level of perceived corruption.

vdem_corr: Political corruption. Question: How pervasive is political corruption?
Clarification: The directionality of the V-Dem corruption index runs from less corrupt to more corrupt
(unlike the other V-Dem variables that generally run from less democratic to more democratic
situation). The corruption index includes measures of six distinct types of corruption that cover
both different areas and levels of the polity realm, distinguishing between executive, legislative and
judicial corruption. Within the executive realm, the measures also distinguish between corruption
mostly pertaining to bribery and corruption due to embezzlement. Finally, they differentiate between
corruption in the highest echelons of the executive (at the level of the rulers/cabinet) on the one
hand, and in the public sector at large on the other. The measures thus tap into several distinguished
types of corruption: both 'petty' and 'grand'; both bribery and theft; both corruption aimed and
influencing law making and that affecting implementation. Aggregation: The index is arrived at by
taking the average of (a) public sector corruption index; (b) executive corruption index; (c) the indicator
for legislative corruption; and (d) the indicator for judicial corruption. In other words, these
four different government spheres are weighted equally in the resulting index. V-Dem replace missing
values for countries with no legislature by only taking the average of (a), (b) and (d).

bci_bci: The BCI index values lie between 0 and 100, with an increase in the index corresponding to a raise
in the level of corruption. This is a first difference with CPI and WGI where an increase means that
the level of corruption has decreased.
There exists no objective scale on which to measure the perception of corruption and the exact
scaling you use is to a large extent arbitrary. However, we were able to give the index an absolute
scale: zero corresponds to a situation where all surveys say that there is absolutely no corruption. On
the other hand, when the index is one, all surveys say that corruption is as bad as it gets according
to their scale. This is another difference with CPI and WGI, where the scaling is relative. They are
rescaled such that WGI has mean 0 and a standard deviation of 1 in each year, while CPI always lies
between 0 and 100.
In contrast, the actual range of values of the BCI will change in each year, depending how close
countries come to the situation where everyone agrees there is no corruption at all (0), or that corruption
is as bad as it can get (100).
The absolute scale of the BCI index was obtained by rescaling all the individual survey data such that
zero corresponds to the lowest possible level of corruption and 1 to the highest one. We subsequently
rescaled the BCI index such that when all underlying indicators are zero (one), the expected value of
the BCI index is zero (hundred)

bti_acp: To what extent does the government successfully contain corruption? 1-10.
1. The government fails to contain corruption, and there are no integrity mechanisms in place.
4. The government is only partly willing and able to contain corruption, while the few integrity
mechanisms implemented are mostly ineffective.
7. The government is often successful in containing corruption. Most integrity mechanisms are in
place, but some are functioning only with limited effectiveness.
10. The government is successful in containing corruption, and all integrity mechanisms are in place
and effective.

python -m OrganizeData.PrepareRegressionData.step12_append_corrupt_data
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    reg_df: DataFrame = pd.read_stata(os.path.join(const.DM_DATA_PATH, '20201221_democracy_investment_firm_r1.dta'))
    qog_df: DataFrame = pd.read_pickle(os.path.join(const.DATA_PATH, '20210127_qog_useful_dataset.pkl')).rename(
        columns={'ccodealp': 'country_iso3', 'vdem_corr': 'VDEM_CORRUPT_INDEX', 'bci_bci': 'BCI_CORRUPT_INDEX',
                 'bti_acp': 'BTI_CORRUPT_INDEX'})
    qog_df.loc[:, 'TI_CORRUPT_INDEX'] = 1 - qog_df['ti_cpi'].fillna(qog_df['ti_cpi_om'] * 10) / 100
    qog_df.loc[:, 'BCI_CORRUPT_INDEX'] /= 100
    qog_df.loc[:, 'BTI_CORRUPT_INDEX'] = 1 - qog_df['BTI_CORRUPT_INDEX'] / 10
    reg_df_corruption: DataFrame = reg_df.merge(
        qog_df.loc[:, ['country_iso3', const.YEAR, 'TI_CORRUPT_INDEX', 'VDEM_CORRUPT_INDEX', 'BCI_CORRUPT_INDEX',
                       'BTI_CORRUPT_INDEX']],
        on=['country_iso3', const.YEAR], how='left')

    reg_df_corruption.to_stata(os.path.join(const.DM_DATA_PATH, '20210127_democracy_investment_firm_corrupt.dta'),
                               write_index=False)
