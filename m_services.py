from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256
import datetime
import flask_login
import m_dal

# Users
def users_get_all(db):
    return m_dal.collection_get(db.users)

def users_get_one(db, user_id):
    return m_dal.document_get(db.users, user_id)

def users_create(db, data):
    new_record = {
            'username': data.get('username'),
            'email': data.get('email'),
            'gender': None if data.get('gender')=="null" else data.get('gender'),
            'password': pbkdf2_sha256.hash(data.get('password')),
            'terms_and_conditions': False if data.get('terms_and_conditions')==None else True,
            'marketing': False if data.get('marketing')==None else True
        }
    return m_dal.users_create(db.users, new_record)

def users_update(db, data, user_id):
    updated_record = {
            'username': data.get('username'),
            'email': data.get('email'),
            'gender': None if data.get('gender')=="null" else data.get('gender'),
            'password': pbkdf2_sha256.hash(data.get('password')),
            'terms_and_conditions': False if data.get('terms_and_conditions')==None else True,
            'marketing': False if data.get('marketing')==None else True
        }
    return m_dal.users_update(db.users, updated_record, user_id)

def users_delete(db, user_id):
    return m_dal.users_delete(db.users, user_id)

# Categories
def categories_get_all(db):
    return m_dal.collection_get(db.categories)

def categories_create_0(db, data):
    category_value = data.get('category')
    return m_dal.categories_create_0(db.categories, category_value)

def categories_create_1(db, data, parent_id):
    category_value = data.get('category')
    return m_dal.categories_create_1(db.categories, category_value, parent_id)

def categories_update_0(db, data, category_id):
    category_value = data.get('category')
    return m_dal.categories_update_0(db.categories, category_value, category_id)

def categories_update_1(db, data, category_id):
    category_value = data.get('category')
    return m_dal.categories_update_1(db.categories, category_value, category_id)

def categories_delete_0(db, category_id):
    return m_dal.categories_delete_0(db.categories, category_id)

def categories_delete_1(db, category_id):
    return m_dal.categories_delete_1(db.categories, category_id)

def sub_categories_get(db, parent_id):
    return m_dal.sub_categories_get(db.categories, parent_id)

# Threads
def threads_get_all(db):
    return m_dal.collection_get(db.threads)

def threads_get_one(db, thread_id):
    return m_dal.document_get(db.threads, thread_id)

def threads_search(db, data):
    user_input = {
        'category_id': data.get('categories'),
        'sub_category_id': data.get('sub_categories'),
        'search_box': data.get('search-box')
    }
    return m_dal.threads_search(db.threads, user_input)

def threads_create(db, data):
    category_id = data.get('categories')
    category_name = m_dal.category_name_get(db.categories, category_id)
    if data.get('sub_categories'):
        sub_category_id = ObjectId(data.get('sub_categories'))
        sub_category_name = m_dal.sub_category_name_get(db.categories, data.get('sub_categories'))
    else:
        sub_category_id = ""
        sub_category_name = ""
    new_record = {
        'datetime': datetime.datetime.utcnow(),
        'user': {
            'user_id': ObjectId(flask_login.current_user._id),
            'username': flask_login.current_user.username
        },
        'category': {
            'category_id': ObjectId(category_id),
            'category_name': category_name,
            'sub_category_id': sub_category_id,
            'sub_category_name': sub_category_name
        },
        'product_name': data.get('product_name'),
        'price': float(data.get('price')),
        'image': data.get('image'),
        'affiliate': data.get('affiliate'),
        'description': data.get('description'),
        'votes': {
            'up_votes': [],
            'down_votes': []
        },
        'sub_posts': []
    }
    # print(new_record)
    return m_dal.threads_create(db.threads, new_record)

def threads_update(db, data, thread_id):
    category_id = data.get('categories')
    category_name = m_dal.category_name_get(db.categories, category_id)
    if data.get('sub_categories'):
        sub_category_id = ObjectId(data.get('sub_categories'))
        sub_category_name = m_dal.sub_category_name_get(db.categories, data.get('sub_categories'))
    else:
        sub_category_id = ""
        sub_category_name = ""
    # sub_category_id = ObjectId(data.get('sub_categories')) if data.get('sub_categories') else ""
    updated_record = {
        'datetime': datetime.datetime.utcnow(),
        'user': {
            # 'user_id': data.get('user_id').strip(),
            # 'username': data.get('username')
            'user_id': ObjectId(flask_login.current_user._id),
            'username': flask_login.current_user.username
        },
        'category': {
            'category_id': ObjectId(data.get('categories')),
            'category_name': category_name,
            'sub_category_id': sub_category_id,
            'sub_category_name': sub_category_name
        },
        'product_name': data.get('product_name'),
        'price': float(data.get('price')),
        'image': data.get('image'),
        'affiliate': data.get('affiliate'),
        'description': data.get('description'),
        'votes': {
            'up_votes': [],
            'down_votes': []
        },
        'sub_posts': []
    }
    # print(updated_record)
    return m_dal.threads_update(db.threads, updated_record, thread_id)

def threads_delete(db, thread_id):
    return m_dal.threads_delete(db.threads, thread_id)

# Thread comments
def comments_create(db, data, thread_id):
    new_record = {
        'datetime': datetime.datetime.utcnow(),
        'user': {
            'user_id': ObjectId(flask_login.current_user._id),
            'username': flask_login.current_user.username
        },
        'comment': data.get('comment'),
        'quote': None
    }
    return m_dal.comments_create(db.threads, new_record, thread_id)

def comments_update(db, data, thread_id, comment_id):
    updated_record = {
        'datetime': datetime.datetime.utcnow(),
        'user': {
            'user_id': ObjectId(flask_login.current_user._id),
            'username': flask_login.current_user.username
        },
        'comment': data.get('comment'),
        'quote': None
    }
    return m_dal.comments_update(db.threads, updated_record, thread_id, comment_id)

def comments_delete(db, comment_id):
    return m_dal.comments_delete(db.threads, comment_id)

def comments_count(db, thread_id):
    return m_dal.comments_count(db.threads, thread_id)

# Voting
def vote_up(db, thread_id):
    return m_dal.vote_up(db.threads, thread_id)

def vote_down(db, thread_id):
    return m_dal.vote_down(db.threads, thread_id)

def vote_up_check(db, thread_id):
    return m_dal.vote_up_check(db.threads, thread_id)

def vote_down_check(db, thread_id):
    return m_dal.vote_down_check(db.threads, thread_id)

def vote_up_remove(db, thread_id):
    return m_dal.vote_up_remove(db.threads, thread_id)

def vote_down_remove(db, thread_id):
    return m_dal.vote_down_remove(db.threads, thread_id)

def vote_count(db, thread_id, up_or_down):
    return m_dal.vote_count(db.threads, thread_id, up_or_down)
