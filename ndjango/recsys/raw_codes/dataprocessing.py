# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import pprint
import json


url = "https://openapi.foodsafetykorea.go.kr/api/af124064dfda4b78a2d7/COOKRCP01/json/1000/2000"
response = requests.get(url)
contents = response.text

pp = pprint.PrettyPrinter(indent=4)
print(pp.pprint(contents))


json_ob = json.loads(contents)
print(json_ob)
print(type(json_ob))

body = json_ob["COOKRCP01"]["row"]


dataframe = json_normalize(body)
print(dataframe)

dataframe.to_csv('recipe2.csv' ,encoding='utf-8-sig')

import pandas as pd
from pandas.io.json import json_normalize
korecipe=pd.read_csv('recipe2.csv',encoding='utf-8-sig')

enrecipe=pd.read_csv('F:\\Ndjango\\branch_test\\archive\\recipeenglish.csv')
enrecipe.columns
#enrecipe=enrecipe.drop(columns='Ingredients',axis=1)
Instructions=enrecipe['Instructions'].astype(str)
Instructionslist=Instructions.apply(lambda x: x.split('\n'))
list_lengths = Instructionslist.apply(lambda x: len(x))
enrecipe = pd.concat([enrecipe, list_lengths.rename('Instructions_length')], axis=1)
ingredient=enrecipe[['Ingredients','Cleaned_Ingredients']]
print(ingredient)
min(list_lengths)
enrecipe.columns
enrecipe=enrecipe.drop('Unnamed: 0',axis=1)


from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# 데이터프레임에서 식재료 추출
ingredients = enrecipe['Cleaned_Ingredients']

# TF-IDF 벡터화
tfidf_vectorizer = TfidfVectorizer(max_features=len(set(ingredients)))
tfidf_matrix = tfidf_vectorizer.fit_transform(ingredients)

# 벡터화된 식재료 딕셔너리 생성
ingredient_dict = {}
terms = tfidf_vectorizer.get_feature_names()
for i, term in enumerate(terms):
    ingredient_dict[term] = tfidf_matrix.getcol(i).sum()

# 딕셔너리를 데이터프레임으로 변환
df_ingredients = pd.DataFrame.from_dict(ingredient_dict, orient='index', columns=['tfidf'])
df_ingredients = df_ingredients.sort_values(by=['tfidf'], ascending=False)

import re

def clean_text(text):
    # remove digits
    text = re.sub(r'\d', '', text)
    # remove brackets and parentheses
    text = re.sub(r'[()\[\]]', '', text)
    # remove commas, dots and hyphens
    text = re.sub(r'[,.\\/-]', ' ', text)
    # remove adjectives and units
    text = re.sub(r'\b\w+\b', lambda x: '' if x.group(0) in ['cup', 'tsp', 'tbsp', 'lb', 'oz'] else x.group(0), text)
    # remove extra whitespaces
    text = re.sub(r'\s+', ' ', text)
    # remove leading and trailing whitespaces
    text = text.strip()
    return text
ingredients=pd.DataFrame(ingredients)
ingredients['Cleaned_Ingredients'] = ingredients['Cleaned_Ingredients'].apply(clean_text)

print(enrecipe['Cleaned_Ingredients'][0])
enr2=enrecipe['Cleaned_Ingredients'][0].split(',')
enr2
import ast
all_ingredients = []
for ingredients in enrecipe['Cleaned_Ingredients']:
    list_ingredients = ast.literal_eval(ingredients)
    all_ingredients.append(list_ingredients)


ingredients_list2 = [item for sublist in all_ingredients for item in sublist]
merged_ingre_list = list(set(ingredients_list2))


ingredients2 = []
for i in range(len(merged_ingre_list)):
    for item in merged_ingre_list[i].split(','):
        ingredient12 = re.sub(r'\([^)]*\)', '', item) # 괄호 안의 내용 제거
        ingredient12 = re.sub('[^a-zA-Z ]+', '', ingredient12) # 숫자, 기호, 영어 알파벳 제거
        ingredient12 = ingredient12.strip() # 양쪽 공백 제거
        ingredients2.append(ingredient12)

print(ingredients2)
pattern = r"(\d+\/\d+|\d+)\s*(cup|tablespoon|teaspoon|pound|ounce|quart|gallon|pint|inch|cm|mm|')?\s*(minced|chopped|diced|sliced)?\s*([\w\s\-]+)"

ingredients3 = []
for ingredient in ingredients_list2:
    ingredient = ingredient.strip()
    match = re.findall(pattern, ingredient)
    if match:
        ingredient_name = match[0][-1]
        ingredient_name = re.sub(r'\b(Tbsp|1|2|3|4|5|6|7|8|9|to|tbsp|tsp|oz|lb|s|plus|¾|½|¼|fl|-15|qt|-inch|-pound|-ounce|-|4½|2½|g|ml|⅓|cups|or|large|small|dry|)\b', '', ingredient_name).strip()
        ingredients3.append(ingredient_name)
ingredients3 = list(filter(lambda x: len(x) > 0, ingredients3))


def clean_ingredients_list(ingredients_list):
    cleaned_list = []
    for ingredient in ingredients_list:
        # Remove any remaining unit measurements
        ingredient = re.sub(r'\b(oz|ounce|fl oz|size|a|10|1¾|xx|xcm|diameter|cubes|cubed|cube|dash|dashes|drop|diced|drops|finequality|freshly|strained|tightly|very|qt|½|¾|¼|x|in|0|lager|light lager|pot|x|14ounces|14x9|but|c|canned|15ounces|16|15x15|17|18|container|jar|loaf|loaves|package|16x3|box|of|by||bottles|18long|stick|cup|can|cans|strips|3½|fluid ounce|ounces|⅔|cup|pounds|teaspoons|15|inch|pound|ripe|lb|pound|g|gram|kg|kilogram|tsp|teaspoon|tbsp|tablespoon)\b', '', ingredient, flags=re.IGNORECASE)
        # Remove any hyphenated words
        ingredient = re.sub(r'\b\w+-\w+\b', '', ingredient)
        # Remove any numbers with two or more digits
        ingredient = re.sub(r'\d{1}', '', ingredient)
        # Remove any numbers with two or more digits
        ingredient = re.sub(r'\d{2,}', '', ingredient)
        # Remove numbers with x in between
        ingredient = re.sub(r'\d+x|\d+x\d+|\dx', '', ingredient)
        # Remove any extra whitespace and hyphens
        ingredient = ' '.join(ingredient.split()).replace('-', '')
        # Remove any extra whitespace
        ingredient = ' '.join(ingredient.split())
        # Remove any remaining unit measurements
        ingredient = re.sub(r'\b(oz|ounce|fl oz|size|a|purchased|frozen|t|chopped|containers|jars|inchwide|inchthick|inchstrips|inchtall|inchsquare|inchlong|inches|inchdiameter|highquality|grated|lightly|xx|more|packages|packaged|tsps|L|SALT|St|U|bestquality|tbsps|fresh|bottled|bowls|boxes|bunch|bunches|firm|storebought|sticks|sprig|sprigs|tablespoons|to|packed|fresh|finely|cold|coarsely|10|1¾|qt|½|¾|¼|x|in|0|lager|light lager|pot|x|14ounces|14x9|15ounces|16|15x15|17|18|container|jar|loaf|loaves|package|16x3|box|of|by||bottles|18long|stick|cup|can|cans|strips|3½|fluid ounce|ounces|⅔|cup|pounds|teaspoons|15|inch|pound|ripe|lb|pound|g|gram|kg|kilogram|tsp|teaspoon|tbsp|tablespoon)\b', '', ingredient, flags=re.IGNORECASE)
        # Remove any hyphenated words
        ingredient = re.sub(r'\b\w+-\w+\b', '', ingredient)
        # Remove any numbers with two or more digits
        ingredient = re.sub(r'\d{1}', '', ingredient)
        # Remove any numbers with two or more digits
        ingredient = re.sub(r'\d{2,}', '', ingredient)
        # Remove numbers with x in between
        ingredient = re.sub(r'\d+x|\d+x\d+|\dx', '', ingredient)
        # Remove any extra whitespace and hyphens
        ingredient = ' '.join(ingredient.split()).replace('-', '')
        # Remove any extra whitespace
        ingredient = ' '.join(ingredient.split())
        cleaned_list.append(ingredient)
    return cleaned_list
ingredients4=clean_ingredients_list(ingredients3)
print(ingredients4)

ingredients4 = list(filter(lambda x: len(x) > 0, ingredients4))

ingredients5 =  [s.replace(' ', '_') for s in ingredients4]

ingredients7 = [ingredient.lower() for ingredient in ingredients4]
unique_ingredients=list(set(ingredients7))
ingredients6 =  [s.replace(' ', '_') for s in list(unique_ingredients)]
uniqueingre=pd.DataFrame(list(unique_ingredients))

uniqueingre.to_csv('uniqingred.csv',header=None,index=None)

ingredients_list2 = [ingredient.lower() for ingredient in ingredients_list2]
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from gensim.models import Word2Vec
from keras.preprocessing.text import Tokenizer

tokenizer = Tokenizer()
tokenizer.fit_on_texts(unique_ingredients)

# 각 식재료를 토큰화하여 숫자 시퀀스로 변환
sequences = tokenizer.texts_to_sequences(unique_ingredients)

# 토큰과 해당하는 숫자를 딕셔너리 형태로 출력
word_index = tokenizer.word_index

# TF-IDF 벡터화
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(unique_ingredients)

# K-means 클러스터링(2500개의 클러스터)
kmeans = KMeans(n_clusters=2500).fit(X)
kmeans2 = KMeans(n_clusters=2000).fit(X)
kmeans3 = KMeans(n_clusters=1500).fit(X)
kmeans4 = KMeans(n_clusters=1000).fit(X)
kmeans5 = KMeans(n_clusters=500).fit(X)
# 카테고리 생성 2500
categories = {}
for i, ingredient in enumerate(unique_ingredients):
    category = kmeans.labels_[i]
    if category not in categories:
        categories[category] = []
    categories[category].append(ingredient)


# 카테고리 생성 2000
categories2 = {}
for i, ingredient in enumerate(unique_ingredients):
    category = kmeans2.labels_[i]
    if category not in categories2:
        categories2[category] = []
    categories2[category].append(ingredient)

#print(categories2)

# 카테고리 생성 1500
categories3 = {}
for i, ingredient in enumerate(unique_ingredients):
    category = kmeans3.labels_[i]
    if category not in categories3:
        categories3[category] = []
    categories3[category].append(ingredient)
#print(categories3)
# 카테고리 생성 1000
categories4 = {}
for i, ingredient in enumerate(unique_ingredients):
    category = kmeans4.labels_[i]
    if category not in categories4:
        categories4[category] = []
    categories4[category].append(ingredient)
#print(categories4)
# 카테고리 생성 500
categories5 = {}
for i, ingredient in enumerate(unique_ingredients):
    category = kmeans5.labels_[i]
    if category not in categories5:
        categories5[category] = []
    categories5[category].append(ingredient)
#print(categories5)
import pickle
with open('categories4.pickle','wb')as fw:
    pickle.dump(categories4,fw)
with open('categories5.pickle','wb')as fw:
    pickle.dump(categories5,fw)
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# 토큰화된 데이터를 이용해 K-means clustering 모델 학습
model = KMeans(n_clusters=10)
model.fit(X)

# 클러스터 개수별 inertia 값을 구함 >굳이 구해야할까? 일단 오랜시간이 걸리는 작업
inertias = []
for k in range(500,600):
    model = KMeans(n_clusters=k)
    model.fit(X)
    inertias.append(model.inertia_)
    print(k)


# inertia 값 그래프를 그리고 elbow point를 찾음
plt.plot(range(500, 600), inertias)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.show()

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# 데이터를 불러온 후 전처리 작업을 수행합니다.

# KMeans 알고리즘을 사용하여 클러스터링을 수행합니다.
kmeans = KMeans(n_clusters=100)
kmeans.fit(X)

# 클러스터링 결과의 Silhouette coefficient를 계산합니다.
silhouette_avg = silhouette_score(X, kmeans.labels_)
print("The average silhouette_score is :", silhouette_avg)
# 클러스터링 결과의 Silhouette coefficient를 계산합니다.
silhouette_avg = silhouette_score(X, kmeans2.labels_)
print("The average silhouette_score is :", silhouette_avg)
'''
그럼 이제 뭘 해야할까
1. 클러스터들에 이름붙이기(카테고리 만들기)
2. 이름을 호출하면 해당 클러스터에 해당하는 내용물이 있는 레시피를 호출하게 만들기
3. 요리법도 비슷한것끼리, 혹은 난이도가 비슷한것끼리 묶을까?
- 난이도로 한다면 기준은? 
    -요리법의 길이로 했을때는 정규화해서 0~0.2는 1성, 0.2~0.4는 2성... 0.8~1.0은 5성
    -요리 재료의 수로 한다면?
        
- 식재료 카테고리 수는 약 500개
     -클러스터 수도 거기에 맞출까?
'''     
import torch
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import re


tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")

ner_model = AutoModelForTokenClassification.from_pretrained("bert-base-multilingual-casedZZ")

ner_pipeline = pipeline('ner', model=ner_model, tokenizer=tokenizer)


def get_ingredient(text):
    # 정규표현식 패턴으로 재료명을 찾습니다.
    pattern = r'\b(?:[A-Z][a-z]*\s+)*(?:[A-Z][a-z]*)\b(?:(?:\s+or\s+)|(?:\s*\,\s*)|(?:\s*\-\s*)|$)'
    match = re.search(pattern, text)
    if match:
        return match.group().strip()
    else:
        return None


def extract_ingredients(data):
    # 입력된 데이터의 각 문장을 추출합니다.
    sentences = [sent for sent in data if sent.endswith('.') or sent.endswith('?') or sent.endswith('!')]

    # 각 문장에서 재료명을 추출합니다.
    ingredients = []
    for sent in sentences:
        inputs = tokenizer(sent, return_tensors="pt", padding=True, truncation=True)
        outputs = ner_model(**inputs)
        predicted_labels = outputs.logits.argmax(dim=-1)
        predicted_labels = predicted_labels.detach().cpu().numpy().tolist()
        label = [ner_model.config.id2label[label_id] for label_id in predicted_labels[0] if ner_model.config.label2id.get(ner_model.config.id2label[label_id], -1) != -1][1:-1]
        indices = [i for i, x in enumerate(label) if x != "I-INGR"]
        if len(indices) > 1:
            start = indices[0]
            end = indices[-1]
            ingredient = get_ingredient(sent[start:end])
            if ingredient:
                ingredients.append(ingredient)
    return ingredients

# Example usage
data = ['1 (3½–4-lb.) whole chicken',
'2¾ tsp. kosher salt, divided, plus more',
'2 small acorn squash (about 3 lb. total)',
'2 Tbsp. finely chopped sage',
'1 Tbsp. finely chopped rosemary',
'6 Tbsp. unsalted butter, melted, plus 3 Tbsp. room temperature']
extract_ingredients(data)
