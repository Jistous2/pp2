import json

with open("sample-data.json", "r") as file: #открывает файл
    data = json.load(file) #превращает в словарь

print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<8} {'MTU':<6}") #заголовки
print("-" * 80)

interfaces = data["imdata"]

for item in interfaces:
    attributes = item["l1PhysIf"]["attributes"]
    dn = attributes.get("dn", "")
    descr = attributes.get("descr", "")
    speed = attributes.get("speed", "")
    mtu = attributes.get("mtu", "")
    #.get читает поля

    print(f"{dn:<50} {descr:<20} {speed:<8} {mtu:<6}")