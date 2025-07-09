import json

# Python对象
data = {
    "name": "John",
    "age": 30,
    "is_student": False,
    "hobbies": ["reading", "swimming"],
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "zip": "10001"
    }
}

# 将Python对象转换为JSON字符串并保存到文件
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)

# 从JSON文件中读取数据
with open('data.json', 'r') as f:
    loaded_data = json.load(f)

print(loaded_data)
for i,j in dict(loaded_data).items():
    print(i,j)