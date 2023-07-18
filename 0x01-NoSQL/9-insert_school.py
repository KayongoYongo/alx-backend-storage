#!/usr/bin/env python3
"""The script inserts a document into a collection"""


import pymongo


def insert_school(mongo_collection, **kwargs):
    """Returns the document id"""
    # Insert the document into the collection
    result = mongo_collection.insert_one(kwargs)

    # Return the new document's _id
    return result.inserted_id
