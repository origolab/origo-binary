import logging
import argparse

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config

from stratum.client import ConnectionPool
from stratum.client import Connection
from equihash.pow import Pow

import time

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger("stratum-server")

def ok(**kwargs):
    kwargs["status"] = "ok"
    return dict(kwargs)

def call(connection_pool, method, params):
    with connection_pool.get() as conn:
        response = conn.call(method, *params)
    return response["result"]


@view_config(route_name="execute", renderer="json", request_method="POST")
def execute(request):
    method = request.POST.get("method")
    params = request.POST.get("params", [])
    result = call(request.connection_pool, method, params)
    return ok(result=result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, default=96,
                        help='length of the strings to be XORed')
    parser.add_argument('-k', type=int, default=5,
                        help='number of strings needed for a solution')
    parser.add_argument('-v', '--verbosity', action='count',
                        help='show debug output (use -vv for verbose output)')
    args = parser.parse_args()

    try:
        conn = Connection(1)
    except:
        print("failed to connect node ")
        exit()
    
    pow = Pow(args.n, args.k, args.verbosity)
   
    while True:
         result = conn.call("mining.subscribe")["result"]

         if len(result[1]) != (32*2+2) or len(result[2]) != (32*2+2): 
             print("wrong response")
             time.sleep(5)
             continue

         pow_hash = result[1]
         data = pow_hash
         nonce, soln = pow.mine_with_data(data, result[2])

         workId = 1
         jobId = result[3]
         
         result = conn.call("mining.submit", workId, jobId, result[1], str(nonce), soln)["result"]

         time.sleep(1)



