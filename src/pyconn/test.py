from core import ApiConnection
from exceptions import RpcException

api = next(ApiConnection('http://localhost:1986/api').create_api({
    'ICalculator': {
        'methods': {
            'AddAsync': {
                'alias': 'add'
            },
            'ParseInt': {
                'alias': 'parse_int'
            }
        },
        'properties': {
            'PI': {
                'alias': 'pi',
                'hasgetter': True,
                'hassetter': False
            }
        }
    }
}))
print(api.add(1, 2))
print(api.parse_int('1986'))
print(api.pi)
try:
    api.parse_int('invalid')
except RpcException as ex:
    print(ex)
