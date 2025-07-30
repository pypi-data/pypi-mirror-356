def remove_duplicates_keep_latest(collection):
   try:
       initial_count = collection.count_documents({})
       pipeline = [
           {"$sort": {"_id": 1}},
           {"$group": {
               "_id": {"영업일": "$영업일", "종목코드": "$종목코드"},
               "latest_id": {"$last": "$_id"}
           }}
       ]
       
       unique_docs = list(collection.aggregate(pipeline))
       result = collection.delete_many({
           "_id": {"$nin": [doc["latest_id"] for doc in unique_docs]}
       })
       
       return {
           "success": True,
           "initial_count": initial_count,
           "final_count": collection.count_documents({}),
           "deleted_count": result.deleted_count
       }
   except Exception as e:
       return {
           "success": False,
           "error": str(e)
       }