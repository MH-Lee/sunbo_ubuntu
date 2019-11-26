from django.shortcuts import render
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view
# from django.http import HttpResponse, JsonResponse
# from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import generics
from recommender.models import Recommender, Result
from recommender.serializer import ResultSerializer
import pandas as pd
from scipy import spatial
from sklearn.preprocessing import minmax_scale
import json
from ast import literal_eval
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from collections import namedtuple
import os
import warnings
warnings.filterwarnings("ignore")

model_name = './recommender/models/Doc2vec1.model'
doc_vectorizer = Doc2Vec.load(model_name)


def recommend(target, doc_vectorizer):
    obj = Recommender.objects.all()
    final_list =  pd.DataFrame(list(obj.values()))
    final_list['token'] = final_list['token'].apply(lambda x:literal_eval(x))
    middle = final_list[(final_list['establish'] <= 6)& (final_list['establish'] >= 4)].reset_index(drop=True)
    prime  = final_list[final_list['establish'] < 4].reset_index(drop=True)
    TaggedDocument = namedtuple('TaggedDocument', 'words tags')
    tagged_docs = [TaggedDocument(d, c) for d, c in final_list[['token', 'lable']].values]
    X = [doc_vectorizer.infer_vector(doc.words) for doc in tagged_docs]
    y = [doc.tags for doc in tagged_docs]
    target_idx = final_list[final_list['company']==target].index[0]
    category1 = middle[middle['company']== target]['predicted_label1'].values[0]
    category2 = middle[middle['company']== target]['predicted_label2'].values[0]
    category  = [category1,category2]
    print('target :',target,' ,categroy :',category)
    ss = prime[(prime['predicted_label1'].isin(category))|(prime['predicted_label2'].isin(category))].reset_index(drop=True)
    similarity = []
    for i in range(len(ss)):
        temp = ss['company'][i]
        temp_idx = final_list[final_list['company']==temp].index[0]
        s_score = 1 - spatial.distance.cosine(X[target_idx], X[temp_idx])
        similarity.append(s_score)
    ss['similarity'] =similarity
    ss['normal_total']   = minmax_scale(ss['total'])
    ss['normal_similarity']   = minmax_scale(ss['similarity'])
    ss['normal_patent']   = minmax_scale(ss['patent'])
    ss['weight'] = ss['normal_total']+ ss['normal_similarity'] + ss['tips'] + ss['normal_patent'] + ss['tips']
    recomend_result = ss.sort_values(["weight"], ascending=[False]).reset_index(drop=True)
    return recomend_result[0:10][['company','weight']], category

# Create your views here.
def introduction(request):
    return render(request, './project/introduction.html')

def network(request):
    json_data=open('./recommender/data/network.json').read()
    json_data = {"data": [json.loads(json_data)]}
    return render(request, './project/networks.html', context=json_data)

def recommender(request):
    return render(request, './project/recommender.html')

class RecommenderAPIView(generics.ListAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = ResultSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            target = serializer.data['target']
            try:
                recomend_result, category = recommend(target, doc_vectorizer)
                result_list = recomend_result.to_dict('records')
                result = {
                    'result':result_list,
                    'category':category
                }
            except IndexError:
                result_list = ["회사이름이 없습니다."]
                result = {
                    'result':result_list,
                    'category': "회사이름이 없습니다."
                }
        return Response(result, status=200)
