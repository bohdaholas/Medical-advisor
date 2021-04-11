import json

with open('SymptomsOutput.json') as file:
    data = json.load(file)

for question in data:
    if "choices" in question:
        print(question["laytext"])
        for choice in question["choices"]:
            print(f">>> {choice['laytext']}")
        print()
