import pandas as pd
import numpy as np

def read_signal_data(city=None):
    """
    only 109 is available
    read_signal_data.
    :returns: signal_data
    """
    signal_data = pd.read_csv('../data/signal/109年11月行政區電信信令人口統計資料_鄉鎮市區.csv', encoding="big5", skiprows=[1])
    if city is not None:
        signal_data = signal_data[signal_data['COUNTY'] == city]

    ## drop certain column
    signal_data = signal_data.drop(columns=['COUNTY_ID', 'COUNTY', 'TOWN', 'DAY_WORK', 'INFO_TIME', 'DAY_WEEKEND'])

    return signal_data

def read_internal_data(year='109'):
    """
    read_internal_data.

    :year: TODO
    :returns: internal data

    """
    internal_data = pd.read_csv(f'../data/internal_data/Taipei_data/{year}_Taipei_basic_area.csv')
    mapping_tbl = read_mapping_tbl()
    internal_data = internal_data.merge(mapping_tbl, left_on='最小統計區代碼', right_index=True)

    internal_data.drop(columns=['資料時間'])

    return internal_data

def extract_cols(data, year='109'):
    if year == '109':
        with open('../tbl/colname_109.txt', 'r') as f:
            colnames = [i.rstrip('\n') for i in f.readlines()]
    else:
        with open('../tbl/colname_104-108.txt', 'r') as f:
            colnames = [i.rstrip('\n') for i in f.readlines()]

    data = data[colnames]

    return data

def read_mapping_tbl():
    """
    This data includes bus stops and MRT stations
    And other TOWN, or region information
    """
    mapping_tbl = pd.read_csv("../tbl/Taipei_mapping.csv")
    mapping_tbl = mapping_tbl.set_index('CODEBASE')
    mapping_tbl = mapping_tbl[['TOWN_ID', 'TOWN', 'X', 'Y', 'lon', 'lat', 'AREA', 'bus_stops', 'MRT_stops']]

    return mapping_tbl


