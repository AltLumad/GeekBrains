import numpy as np
from scipy.sparse import csr_matrix


class IdMapper:
    def __init__(self, user_item_matrix):

        self.userids = user_item_matrix.index.values
        self.itemids = user_item_matrix.columns.values

        matrix_userids = np.arange(len(self.userids))
        matrix_itemids = np.arange(len(self.itemids))

        self.id_to_itemid = dict(zip(matrix_itemids, self.itemids))
        self.id_to_userid = dict(zip(matrix_userids, self.userids))

        self.itemid_to_id = dict(zip(self.itemids, matrix_itemids))
        self.userid_to_id = dict(zip(self.userids, matrix_userids))



    def ItemidToId(*items):

        pass





def prefilter_items(data_train, cut_length=3, sales_range=(10,100)):
    # Оставим только 5000 самых популярных товаров
    popularity = data_train.groupby('item_id')['quantity'].sum().reset_index()
    popularity.rename(columns={'quantity': 'n_sold'}, inplace=True)
    top_5000 = popularity.sort_values('n_sold', ascending=False).head(5000).item_id.tolist()
   
    #добавим, чтобы не потерять юзеров
    data_train.loc[~data_train['item_id'].isin(top_5000), 'item_id'] = 999999 

    # Уберем самые популярные 
    # Уберем самые непопулряные 
    top_5000_cut = top_5000[cut_length:-cut_length]
    data_train.loc[~data_train['item_id'].isin(top_5000_cut), 'item_id'] = 999999 
    #data_train = data_train.loc[data_train['item_id'] != 999999]


    # Уберем товары, которые не продавались за последние 12 месяцев
    data_train = data_train[data_train['week_no'] > data_train['week_no'].max() - 52]
    
    # Уберем не интересные для рекоммендаций категории (department)
    to_del = ['GROCERY', 'MISC. TRANS.', 'PASTRY', 
              'DRUG GM', 'MEAT-PCKGD',
               'SEAFOOD-PCKGD', 'PRODUCE', 
              'NUTRITION', 'DELI', 'COSMETICS']
    data_train = data_train[~(data_train['department'].isin(to_del))]
    
    
    # Уберем слишком дешевые товары (на них не заработаем). 1 покупка из рассылок стоит 60 руб. 
    data_train = data_train[~(data_train['sales_value'] < sales_range[0])]
    
    # Уберем слишком дорогие товарыs
    data = data_train[~(data_train['sales_value'] > sales_range[1])]

    return data_train

def postfilter_items(data_train):
    return data_train.loc[data_train['item_id'] != 999999]





def get_recommendations(user, model, sparse_user_item, id_mapper, filter_, N=5):
    """Рекомендуем топ-N товаров"""

    res = [id_mapper.id_to_itemid[rec[0]] for rec in 
                    model.recommend(userid=user, 
                                    user_items=sparse_user_item,   # на вход user-item matrix
                                    N=N, 
                                    filter_already_liked_items=False, 
                                    filter_items=filter_,  # !!! 
                                    recalculate_user=True)]

    return res





def get_similar_items_recommendation(user_id, model, user_item_matrix, id_mapper,N=5):
    """Рекомендуем товары, похожие на топ-N купленных юзером товаров""" 
    user = id_mapper.userid_to_id[user_id]

    top_items = user_item_matrix.toarray()[user, :]
    top_items = np.argsort(-top_items)
    top_items = top_items[:N]

    res = []
    for item in top_items:
        similar_item = [val[0] for val in model.similar_items(itemid=item, N=2) if val[0] != item]
        res.append(id_mapper.id_to_itemid[similar_item[0]])

    assert len(similar_items) == N, 'Количество рекомендаций != {}'.format(N)
    return res


def get_similar_users_recommendation(user, model, user_item_matrix, id_mapper,  N=5):
    """Рекомендуем топ-N товаров, среди купленных похожими юзерами"""
    sparse_user_item=csr_matrix(user_item_matrix).T.tocsr()
    res = []
    similar_users = model.similar_users(user, N=N+1)
    filter_ = [id_mapper.itemid_to_id[999999]]
    for u in similar_users:
        if u[0] == user: continue
        recs = get_recommendations(user, model, sparse_user_item, id_mapper, filter_, 1)
        res.append(recs[0])
        filter_.append(id_mapper.itemid_to_id[recs[0]])
    return res
