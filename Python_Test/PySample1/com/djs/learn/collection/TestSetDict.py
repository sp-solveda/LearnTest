'''
Created on Mar 1, 2016

@author: dj
'''

# set and dict(key) saved order will be random.

print("-------------------- Set --------------------")

blank_set_wrong = {}
blank_set = set()

print("blank_set Wrong {} =", blank_set_wrong)
print("blank_set set() =", blank_set)

print("-" * 40)

fruits = set(['avacados', 'bananas', 'oranges', 'grapes', 'managos'])
print("fruits{} set() =", fruits)
fruits2 = {'avacados', 'bananas', 'oranges', 'grapes', 'managos'}
print("fruits2{} {} =", fruits2)

vegetables = set(['carrots', 'oranges', 'onions', 'managos', 'celery'])
print("vegetables{} =", vegetables)

print("-" * 40)

print("fruits - vegetables =", fruits - vegetables)
print("vegetables - fruits =", vegetables - fruits)

print("fruits | vegetables =", fruits | vegetables)
print("vegetables | fruits =", vegetables | fruits)

print("fruits & vegetables =", fruits & vegetables)
print("vegetables & fruits =", vegetables & fruits)

print("-" * 40)

words = "Hello, Kitty!"
print("words =", words)

letters1 = {letter for letter in words}
print("letters1 =", letters1)

letters2 = set(words)
print("letters2 =", letters2)

letters2.remove('y')
print("letters2 =", letters2)

letters2.add('Y')
print("letters2 =", letters2)

print("-" * 40)

a_list_of_list = [[1, 2, 3], [1, 2, 3], [2, 3, 4], [2, 3, 4]]
print("a_list_of_list =", a_list_of_list)
# List cannot be hashed. Thus cannot be item of set.
a_set_of_tuple = {tuple(item) for item in a_list_of_list}
print("a_set_of_tuple =", a_set_of_tuple)
an_unique_list_of_list = [list(item) for item in a_set_of_tuple]
print("an_unique_list_of_list =", an_unique_list_of_list)

print("-------------------- Dict --------------------")

blank_dict1 = {}
blank_dict2 = dict()

print("blankDict 1 {} =", blank_dict1)
print("blankDict 2 dict() =", blank_dict2)

print("-" * 40)

animals = {'Cat': 1, 'Dog': 2, 'Chicken': 3}
animals2 = dict(Cat = 1, Dog = 2, Chicken = 3)
print("animals {} =", animals)
print("animals2 dict() =", animals2)

print("-" * 40)

animal_unique = animals.copy()
animal_unique.update(animals2)
print("animal_unique {} =", animal_unique)

print("-" * 40)

animals.update({'Duck': 4})
print("animals {} =", animals)

one_animal = {}
one_animal["Tiger"] = 5
animals.update(one_animal)
print("animals {} =", animals)

animals_copy = animals
animals_copy.update({"Lion": 6})
print("animals {} =", animals)

print("-" * 40)

print("animals.keys() =", animals.keys())
print("animals.values() =", animals.values())
print("animals.values() as list =", list(animals.values()))
print("animals.items() =", animals.items())

print("max(animals) =", max(animals))
print("min(animals) =", min(animals))
print("len(animals) =", len(animals))

print("sorted(animals) =", sorted(animals))
print("sorted(animals.items()) =", sorted(animals.items()))

print("-" * 40)

print("animals['Dog'] = ", animals['Dog'])
print("animals.get('Tiger') = ", animals.get('Tiger'))
print("animals.get('Tiger', 'Not exist') = ",
      animals.get('Tiger', 'Not exist'))

print("-" * 40)

for key in animals:
    print(key, "=", animals.get(key))

print("-" * 40)

for key, value in animals.items():
    print(key, "=", value)

print("-" * 40)

animals3 = animals.fromkeys(animals)
print("animals3 .fromkeys(animals) =", animals3)

print("-" * 40)

animals4 = animals.fromkeys(animals, 0)
print("animals4 .fromkeys(animals, 0) =", animals4)

print("-" * 40)

animals.popitem()
print("animals.popitem() =", animals)

del animals2['Chicken']
print("del animals2['Chicken'] =", animals2)

animals2.pop('Dog')
print("animals2.pop('Dog') =", animals2)

animals2.clear()
print("animals2.clear() =", animals2)

print("-" * 40)

sentence = "This is a good day to work!"
print("sentence =", sentence)
characters = {}
print("characters{} =", characters)
for character in sentence:
    characters[character] = characters.get(character, 0) + 1
print("characters{} =", characters)
print("sorted(characters.items() =", sorted(characters.items()))

print("-" * 40)

# Better, as set(sentence) reduces the loop counter.
letter_count = {letter: sentence.count(letter) for letter in set(sentence)}
# letter_count = {letter: sentence.count(letter) for letter in sentence}
print("letter_count =", letter_count)

if __name__ == '__main__':
    pass
