""" Write a function that will create the following output from test_times below

User Joe completed in 4801s
User James completed in 5013s
User Cathy completed in 4760s
[{'user': 'James', 'seconds': 5013}, {'user': 'Joe', 'seconds': 4801}, {'user': 'Cathy', 'seconds': 4760}]

"""

test_times = [
    {
        "user": "Joe",
        "duration": "01:20:01"
    },
    {
        "user": "James",
        "duration": "01:23:33"
    },
    {
        "user": "Cathy",
        "duration": "01:19:20"
    }
]

for i in test_times:
    print("User " + i['user'] + " has completed in " + i['duration'])
