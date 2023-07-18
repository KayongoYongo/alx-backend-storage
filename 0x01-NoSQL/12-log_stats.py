#!/usr/bin/env python3
"""A script that provides some stats about Nginx logs stored in MongoDB"""

import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["logs"]
collection = db["nginx"]

# Get the total number of documents in the collection
total_logs = collection.count_documents({})

# Print the total number of logs
print(f"{total_logs} logs")

# Get the count of documents for each HTTP method
http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
method_stats = collection.aggregate([
    {"$group": {"_id": "$method", "count": {"$sum": 1}}}
])

# Print the count of documents for each HTTP method
print("Methods:")
for method in http_methods:
    count = next((method_stat["count"] for method_stat in method_stats
                  if method_stat["_id"] == method), 0)
    print(f"\tmethod {method}: {count}")

# Get the count of documents with specific method and path
specific_logs = collection.count_documents({"method": "GET",
                                            "path": "/status"})

# Print the count of documents with specific method and path
print(f"{specific_logs} status check")
