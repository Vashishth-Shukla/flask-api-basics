import requests

response = requests.get(
    "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=stackoverflow"
)

for question in response.json()["items"]:
    if question["answer_count"] < 2:
        print(f'{question["title"]} : {question["answer_count"]}')
        print(question["link"])
    else:
        print("skipped!")
    print()
