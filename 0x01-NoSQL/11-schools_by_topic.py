#!/usr/bin/env python3
"""A script that returns a list of schools having a specific topic"""

import pymongo


def schools_by_topic(mongo_collection, topic):
    """Returns a list of schools"""
    # Find schools matching the specified topic
    schools = mongo_collection.find({"topics": topic})

    # Return the list of schools
    return list(schools)
