
def is_data_in_collection(data, collection):
   return collection.find_one(data) is not None

def count_duplicate_data(data, collection):
    query = data.copy()
    query.pop('_id', None)  # _id 필드 제거
    return collection.count_documents(query)

def remove_duplicates_except_nth(data, collection, n=-1):
   query = data.copy()
   query.pop('_id', None)
   
   if collection.count_documents(query) > 1:
       matching_docs = list(collection.find(query))
       deleted_count = 0
       if abs(n) <= len(matching_docs):
           for doc in matching_docs:
               if doc != matching_docs[n]:
                   result = collection.delete_one({'_id': doc['_id']})
                   deleted_count += result.deleted_count
       return deleted_count
   return 0

def delete_data_in_collection(data, collection, single=False):
    query = data.copy()
    query.pop('_id', None)
    if single:
        result = collection.delete_one(query)
    else:
        result = collection.delete_many(query)
    return result.deleted_count

def update_data_in_collection(data, updated_data, collection, single=False):
   query = data.copy()
   query.pop('_id', None)
   
   if single:
       result = collection.update_one(query, {'$set': updated_data})
   else:
       result = collection.update_many(query, {'$set': updated_data})
   
   return result.modified_count

def insert_data_in_collection(data, collection):
   try:
       result = collection.insert_one(data)
       return result.inserted_id
   except Exception as e:
       print(f"Error inserting data: {e}")
       return False

def insert_many_data_in_collection(data_list, collection):
    try:
        result = collection.insert_many(data_list, ordered=False)
        return result.inserted_ids
    except Exception as e:
        print(f"Error inserting data: {e}")
        return False

def insert_if_not_duplicate(data, collection):
    query = data.copy()
    query.pop('_id', None)
    
    if collection.count_documents(query) == 0:
        result = insert_data_in_collection(data, collection)
        return {'inserted': True, 'id': result}
    return {'inserted': False, 'id': None}

def create_unique_index(collection, fields):
   try:
       index_fields = [(field, 1) for field in fields]
       result = collection.create_index(index_fields, unique=True)
       return {"success": True, "index_name": result}
   except Exception as e:
       return {"success": False, "error": str(e)}

def create_collection(db, collection_name):
   try:
       collection = db.create_collection(collection_name)
       return {"success": True, "collection": collection}
   except Exception as e:
       return {"success": False, "error": str(e)}

def get_all_collections(db):
   return db.list_collection_names()

def get_all_collections_with_info(db):
    return db.list_collections()

def find_data_by_date_range(collection, date_field, start_date, end_date, additional_query=None):
    query = {
        date_field: {
            '$gte': start_date,
            '$lte': end_date
        }
    }
    
    if additional_query:
        query.update(additional_query)
    
    return list(collection.find(query))

def count_data_by_date_range(collection, date_field, start_date, end_date, additional_query=None):
    query = {
        date_field: {
            '$gte': start_date,
            '$lte': end_date
        }
    }
    
    if additional_query:
        query.update(additional_query)
    
    return collection.count_documents(query)