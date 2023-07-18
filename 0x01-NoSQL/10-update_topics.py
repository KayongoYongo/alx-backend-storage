#!/usr/bin/env python3
"""Changes all topics of a document ased on name"""


import pymongo


def update_topics(mongo_collection, name, topics):
    """Returns the modified object"""

    # Update the document(s) matching the name
    result = mongo_collection.update_many({"name": name},
                                          {"$set": {"topics": topics}})

    # Return the number of modified documents
    return result.modified_count
