# zluri_assignment

Prerequisites - Docker, Python 3.X

Steps to run - 
1) clone repo https://github.com/MayankSharma-MS/zluri_assignment
2) run ./init.sh
Note: If docker container spin up takes time and python script fails to get connection, retry using this command **python start.py**

# Table Schema and sample data
 
![alt text](https://github.com/MayankSharma-MS/zluri_assignment/blob/2d15fad96dbdf5e00c975cd40b93b3f9ba12f90c/schema.png "Schema")

![alt text](https://github.com/MayankSharma-MS/zluri_assignment/blob/2d15fad96dbdf5e00c975cd40b93b3f9ba12f90c/sample_data.png "Sample Data")

# Points achieved

All 1 to 5. However, there's always some scope for improvement.

# If had more time to invest in this

1) Manage variables in a config, currently credentials and queries are all over the place
2) Divide csv into smaler chunks and process in parrallel. However, the largest file given in assignment gets processed under 65 secs with single process.

# Assumptions taken into account for the task
1) **sku** being primary key, every conflicting record is to be replaced with the latest one.
2) **name** column is the product name, which is used for aggregated view.
3) Aggregated view is to be updated less frequently, hence created MATERIALIZED VIEW.
