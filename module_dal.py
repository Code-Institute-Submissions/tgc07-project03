from bson.objectid import ObjectId

def dal_collection_get(collection):
    return collection.find()

def dal_category_create_0(collection, category_value):
    new_record = {
        'category': category_value,
        'sub_categories': []
    }
    return collection.insert_one(new_record)

def dal_category_create_1(collection, category_value, parent_id):
    return collection.update_one({
        '_id': ObjectId(parent_id)
    }, {
        '$push': {
            'sub_categories': {
                '_id': ObjectId(),
                'category': category_value,
                'sub_categories': []
            }
        }
    })

def dal_category_update_0(collection, category_value, category_id):
    return collection.update_one({
        '_id': ObjectId(category_id)
    }, {
        '$set': {
            'category': category_value
            }
    })

def dal_category_update_1(collection, category_value, category_id):
    return collection.update_one({
            'sub_categories._id': ObjectId(category_id)
        }, {
            '$set': {
                'sub_categories.$.category': category_value
            }
        })

def dal_category_delete_0(collection, category_id):
    return collection.remove({
        '_id': ObjectId(category_id)
        })

def dal_category_delete_1(collection, category_id):
    return collection.update_one({
        'sub_categories._id': ObjectId(category_id)
        }, {
            '$pull': {
                'sub_categories': {
                    '_id': ObjectId(category_id)
                }
            }
        })


