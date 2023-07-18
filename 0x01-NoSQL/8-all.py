#!/usr/bin/env python3
"""The script retrieves all documents in a collection"""


import pymongo


def list_all(mongo_collection):
    """Returns documents from a collection"""
    documents = []
    
    # Retrieve all documents from the collection
    cursor = mongo_collection.find()
    
    # Iterate over the cursor and append documents to the list
    for document in cursor:
        documents.append(document)
    
    return documents
