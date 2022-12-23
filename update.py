import requests

main = requests.get("https://raw.githubusercontent.com/bonaktan/AutoBM/main/AutoBM/main.py")
update = requests.get("https://raw.githubusercontent.com/bonaktan/AutoBM/main/update.py")

print(
    """WARNING: You WILL Overwrite the main.py and update.py files, any changes WILL
be lost, do you wish to continue? (y/N)  """, end="")
response = str(input())
if response.lower() != "y": print("Aborting"); quit()

with open("AutoBM/main.py", "w") as m: m.write(main.text)
with open("update.py", "w") as u: u.write(update.text)
