# -*- coding: utf-8 -*-

import requests
import re
import pandas as pd
url = 'https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000720.1.6ff830ffiy8OY5&cat=50067917&brand=3223' \
      '459&q=%B5%E7%B6%AF%C2%DD%CB%BF%B5%B6&sort=s&style=g&from=sn_1_brand-qp#J_crumbs'
ret = requests.get(url).text
print(ret)
product_list = re.findall('<a href=".*" class="productImg"?', ret)
print(product_list)


pattern0 = re.compile('\?id=\d+')
pattern1 = re.compile('user_id=\d+')
# pattern = re.compile()
pattern2 = re.compile('\d+')
product = []
for sent in product_list:
    product_id = pattern0.findall(sent)[0]
    seller_id = pattern1.findall(sent)[0]
    product.append((pattern2.findall(product_id)[0], pattern2.findall(seller_id)[0]))


data = pd.DataFrame(product, columns=['itemid', 'sellerid'])


data.to_csv('./tmall_product_for_spyder//tmall_prduct_id.csv', encoding='utf-8')
