Dependency
```
python = "^3.10"
granian = "1.7.6"
fastapi = "0.115.8"
```
Default port is 8080, if you want change service port, modify file: site-packages/code_exec/controller/api.py

Running service command:
```
code-exec
```

Example of API interface:
```
curl -XPOST '127.0.0.1:8080/api/exec' \
-H 'Content-Type: application/json' \
-d '{
    "language": "python",
    "inputs":
    {
        "arg1": "参数1"
    },
    "code": "import json\ndata = {\"name\": arg1, \"age\": 18}\njson_str = json.dumps(data, ensure_ascii=False)\nresult = {\"data\": json_str}\n"
}'
```
