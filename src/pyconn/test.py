from core import ApiConnection
from exceptions import RpcException

api = ApiConnection('http://localhost:1986/api').create_api('ICalculator')
print(api.add(1, 2))
print(api.parse_int('1986'))
print(api.PI)
try:
    api.parse_int('invalid')
except RpcException as ex:
    print(ex)
