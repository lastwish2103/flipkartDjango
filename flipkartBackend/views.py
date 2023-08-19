from django.http import JsonResponse
import pandas as pd
import numpy as np
from flipkartBackend.settings import BASE_DIR
from pymongo import MongoClient
# from dotenv import load_dotenv
import os
# load_dotenv()

db=MongoClient(os.environ.get("CONNECTION_URI")).get_database("flipkart")

productRatingDf=pd.read_csv(f"{BASE_DIR}/Public/productRating.csv")

def TopRatedProduct(request,limit=20):
    try:
        topProducts=productRatingDf.iloc[:limit,:1]
        products=[]
        collection=db.get_collection("products")
        query={
            "id": {"$in": topProducts["ProductId"].to_list()}
        }
        data=collection.find(query)
        for value in data:
            if(value):
                value["_id"]=str(value["_id"])
                value["_id"]=str(value["_id"])
                products.append(value)
        return JsonResponse({"status":True,"data":products},status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"status":False,"data":[]},status=500)
    
def TopSimilaryProduct(request,product_id,limit=20):
    try:
        row=pd.read_csv(f"{BASE_DIR}/Public/{product_id}.csv")
        row=row.sort_values(by=product_id,ascending=False)
        productIds=row["Unnamed: 0.1"][:limit]
        if(len(row)==0):
            raise Exception("Invalid Id")
        products=[]
        collection=db.get_collection("products")
        query={
            "id": {"$in": productIds.to_list()}
        }
        data=collection.find(query)
        for value in data:
            if(value):
                value["_id"]=str(value["_id"])
                value["_id"]=str(value["_id"])
                products.append(value)
        return JsonResponse({"status":True,"data":products},status=200)
    except Exception as e:
        print(e)
        return JsonResponse({"status":False,"data":[]},status=500)
    

def findRecentProduct(request,user_id,limit=20):
    try:
        collection=db.get_collection("user_logs")
        data=collection.find_one({"username":user_id},sort=[('timestamp', -1)])
        if(data):
            return TopSimilaryProduct(request,data['product_id'],limit)
        else:
            return TopRatedProduct(request,limit)
    except Exception as e:
        print(e)
        return JsonResponse({"status":False,"data":[]},status=500)