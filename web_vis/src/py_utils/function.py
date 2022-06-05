import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import sys, os
import random

def calculate_shop_similarity(target_shop_embedding, wish_embedding):
    target_shop_embedding, wish_embedding = get_only_embedding(target_shop_embedding, wish_embedding)
    scores = np.squeeze(cosine_similarity(target_shop_embedding, wish_embedding))
    scores = (np.array(scores) + 1) * 50
    index = np.argsort(scores)[::-1]

    #print(scores, index)
    return scores, index

def get_only_embedding(target_shop_embedding, wish_embedding):
    wish_embedding = wish_embedding.drop(columns=['index', 'name', 'email'])
    cols = set(wish_embedding.columns) & set(target_shop_embedding)
    cols = list(cols)
    #print(cols)
    target_shop_embedding = target_shop_embedding[cols]
    wish_embedding = wish_embedding[cols]

    return target_shop_embedding.astype('float'), wish_embedding.astype('float')

def calculate_shop_embedding(path, args):
  filepath = os.path.join(path, 'shops', 'embedding_statics.csv')
  shop_stat = pd.read_csv(filepath)
  shop_stat = shop_stat.set_index('feature_name')
  ## load region info
  ## human age is second district but we don't know the second district
  #cols = ['0-14歲人口數', '15-24歲人口數', '25-39歲人口數', '40-64歲人口數', '65歲以上人口數',
  cols = ['DAY_WORK(7:00~13:00)', 'DAY_WORK(13:00~19:00)', 'NIGHT_WORK',
          'DAY_WEEKEND(7:00~13:00)', 'DAY_WEEKEND(13:00~19:00)', 'NIGHT_WEEKEND']

  filepath = os.path.join(path, 'final_output', 'district_features.csv')
  region_data = pd.read_csv(filepath).set_index('TOWN')
  region_data = region_data.loc[args['town'], cols]
  args.update(region_data.to_dict())
  ## shop item
  shop_item = {'town': args['town'], 'lonlat': 0}

  ## calculate embedding
  for key in args:
    if key in shop_stat.index:
      args[key] = (float(args[key]) - shop_stat.loc[key, 'min']) / (shop_stat.loc[key, 'max'] - shop_stat.loc[key, 'min'])

  ## categorical
  ## type
  type_cols = ['apartment', '透天厝', 'store', 'mansion']
  for col in type_cols:
    if args['house_type'] == 'villa':
      args['house_type'] = '透天厝'

    if col == args['house_type']:
      args[col] = 1
    else:
      args[col] = 0

  del args['house_type']
  del args['town']
  args = dict([(key, [args[key]]) for key in args])
  args = pd.DataFrame(args)
  
  return args, shop_item

def filter_shops_by_smart(path, data, dicts):
    """
    data: shops dataframe from shops-datadb.csv
    dicts['smart']
        values:
            bt_ss1 -> 小資首選金店面
            bt_ss2 -> 台北不夜城
            bt_ss3 -> 老屋新生潛力空間
            bt_ss4 -> 政府合作特色物件
    """
    ## Need implementation
    filepath = os.path.join(path, 'shops', dicts['smart']+'.csv')
    house_index = pd.read_csv(filepath).set_index('house_index')
    #print(house_index.iloc[[1, 2]])
    data = slc2(data, list(house_index.index))
    ## house_index.loc[[0, 1, 2]]
    scores = None
    return data, scores

def slc2(df,dx):
  """
  dictfilter = {
      'bt_ss1':list1,
      'bt_ss2':list2,
      'bt_ss3':list3,
  }
  """
  listA=[]
  a= random.sample(range(0,len(dx)),30)
  for i in a :
    listA.append(dx[i])

  out = df.iloc[listA]
  #print(out)
  return out


def filter_shops_by_options(data, dicts):
    """
    data: shops dataframe from shops-datadb.csv
    dicts (shop_feature_mapping.yaml)
        keys:
            county(only taipei)
            town
            house_type
            rental_price
            size
            MRT_distance
            human_age
            road/alley
            house_age
            special(?) -> might delete
    """
    ## Need implementation
    data = slc(dicts, data)
    return data

def slc(d1,df):
  listA=[]
  #type轉換
  dicttype ={'apartment':'公寓',
      'villa': '透天厝',
      'mansion': '電梯大樓',
      'store': '店面',
      '':''
      }
  #price轉換
  dictprice={
  'price_20down':20000,
  'price_20_40':40000,
  'price_40_60':60000,
  'price_60_80':80000,
  'price_80_100':100000,
  'price_100up':1000000
  }
  x=0
  y=0
  if d1['rental_price'] == '':
    pass
  else:
    if d1['rental_price'] == 'price_100up':
      x=dictprice[d1['rental_price']]
      y=1000000
    else :
      x=0
      y=dictprice[d1['rental_price']]

  #size轉換
  dictsize={
    'area_10down': 10,
    'area_11_20': 20,
    'area_21_30': 30,
    'area_31_40': 40,
    'area_40up': 40,
    }
  w=0
  z=0
  if d1['size'] == '':
    pass
  else:
    if d1['size'] == 'area_40up':
      w=dictsize[d1['size']]
      z=1000
    else :
      w=0
      z=dictsize[d1['size']]

  #Mrtdis
  dictdis={
  '': 1500,
  'trans_500': 500,
  'trans_1000': 1000,
  'trans_1500': 1500,
  }
  #RA
  dictroad={
  '':2,
  'road': 1,
  'alley': 0
  }
  #houseage
  dicthouse={
  'house_age_10down': 10,
  'house_age_10_20': 20,
  'house_age_20_30': 30,
  'house_age_30up': 30,
  }
  a=0
  b=0
  if d1['house_age'] == '':
    pass
  else:
    if d1['house_age'] == 'house_age_30up':
      a=dicthouse[d1['house_age']]
      b=100
    else :
      a=0
      b=dicthouse[d1['house_age']]


  for i in range(len(df['town'])) :
      if df['town'][i] == d1['town'] or d1['town'] == '':
        #print(i)
        if df['type'][i] == dicttype[d1['house_type']] or d1['house_type'] == '':
          #print(i)
          if df['rental_price'][i] >= x and df['rental_price'][i] <= y or d1['rental_price'] =='':
          #print(df['size'][i])
            if df['size'][i] >= w and df['size'][i] <= z or d1['size'] == '': 
              #print(i)
              if df['MRT_distance'][i] <= dictdis[d1['MRT_distance']]:
                #print(df['小巷0/大路1'][i])
                if df['小巷0/大路1'][i] == dictroad[d1['road/alley']] or d1['road/alley'] =='':
                  #print(df['house_age'][i])
                  if df['house_age'][i] >= a and df['house_age'][i] <= b or d1['house_age'] == '':
                    #print(i)
                    listA.append(i)
  out = df.iloc[listA]         
  return out


if __name__ == '__main__':
    filefolder = '/home/jasonluo/Documents/competition/2022_interior_hackathon/data/'
    from get_data import get_shop_data
    data = get_shop_data(filefolder)
    d1 = {
        'county': 'taipei',
        'town': '',
        'house_type': '',
        'rental_price': '',
        'size': '',
        'MRT_distance': '',
        'human_age': '',###
        'road/alley': '',
        'house_age': '',
    }
    dicts = {
        'county': 'taipei',
        'town': '松山區',
        'house_type': 'apartment',
        'rental_price': 'price_20down',
        'size': 'area_10down',
        'MRT_distance': 'trans_500',
        'human_age': 'house_age_10down',
        'road/alley': 'road',
        'house_age': 'house_age_10down',
    }
    
    #calculate_shop_embedding(filefolder, {'town': '松山區', 'house_type': 'apartment'})
    data, scores = filter_shops_by_smart(filefolder, data, {"smart": "bt_ss2"})
    print(len(data))
