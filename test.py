import collections

Person = collections.namedtuple("Person", "first_name last_name age")

# initialize a user as a Person Tuple
user = Person("John", "Doe", 21)

print(user)
