#!/usr/bin/env python2
import argparse
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from datetime import datetime
from operator import itemgetter
from pyblake2 import blake2b
import struct
import binascii
import progressbar

from convert import (
    compress_array,
    expand_array,
    get_minimal_from_indices,
)

DEBUG = False
VERBOSE = False
#progressbar = None

class Pow(object):
    def __init__(self, n, k, v):
        self.n = n
        self.k = k
              
        self.DEBUG = v > 0
        self.VERBOSE = v > 1

    def mine_with_data(self, data, target):
        
        n = self.n
        k = self.k

        validate_params(n, k)
        if DEBUG:
            print ('- n: %d' % n)
            print ('- k: %d' % k)

        prev_hash = bytearray.fromhex(data[2:])

        #change difficult to little endian       
        d = bytearray.fromhex(target[2:])[::-1]
        #d = bytearray.fromhex(target[2:])

        start = datetime.today()
        # H(I||...
        size = (512/n)*n/8
        digest = blake2b(digest_size=size, person=blake_person(n, k))
        digest.update(prev_hash)
        nonce = 0
        x = None
        while (nonce >> 161 == 0):
            print
            print ('Nonce: %d' % nonce)
            # H(I||V||...
            curr_digest = digest.copy()
            hash_nonce(curr_digest, nonce)
            # (x_1, x_2, ...) = A(I, V, n, k)
            if DEBUG:
                gbp_start = datetime.today()
            solns = gbp_basic(curr_digest, n, k)
            if DEBUG:
                print ('GBP took %s' % str(datetime.today() - gbp_start))
                print ('Number of solutions: %d' % len(solns))
            for soln in solns:
                hn = nonce_to_hex(nonce)
                hs = solution_to_hex(soln)
                if difficulty_filter(prev_hash, hn, hs, d):
                    print 'hash less than difficult'
                    x = soln
                    break
            if x:
                break
            nonce += 1
        duration = datetime.today() - start

        if not x:
            raise RuntimeError('Could not find any valid nonce. Wow.')

        hn = nonce_to_hex(nonce)
        hs = solution_to_hex(x)
        curr_hash = block_hash(prev_hash, hn, hs)
        str_nonce = print_hash(hn)
        str_sol = print_hash(hs)

        print ('-----------------')
        print ('Mined block!')
        print ('Pow hash: %s' % print_hash(prev_hash))
        print ('Proof hash:  %s' % print_hash(curr_hash))
        print ('Nonce:         %s' % str_nonce)
        print ('Solution:      ')
        #for soln in solns:
        print('           ', x)
        print('           ', str_sol)
        print ('Time to find:  %s' % str(duration))
        print ('-----------------')
        
        return str_nonce, str_sol;


def hash_nonce(digest, nonce):
    for i in range(8):
        digest.update(struct.pack('<I', nonce >> (32*i)))

def nonce_to_hex(nonce):
    hex_nonce = bytearray.fromhex('')
    for i in range(8):
        hex_nonce += struct.pack('<I', nonce >> (32 * i))
    if DEBUG: print('hex_nonce ', print_hash(hex_nonce))
    return hex_nonce
        
def hash_xi(digest, xi):
    digest.update(struct.pack('<I', xi))
    return digest # For chaining

def solution_to_hex(soln):
    bit_len = 17
    hex_sol = get_minimal_from_indices(soln,  bit_len)
    if DEBUG: print('hex sol ', print_hash(hex_sol))
    return hex_sol

def count_zeroes(h):
    # Convert to binary string
    if type(h) == bytearray:
        h = ''.join('{0:08b}'.format(x, 'b') for x in h)
    else:
        h = ''.join('{0:08b}'.format(ord(x), 'b') for x in h)
    # Count leading zeroes
    return (h+'1').index('1')

def has_collision(ha, hb, i, l):
    res = [ha[j] == hb[j] for j in range((i-1)*l/8, i*l/8)]
    return reduce(lambda x, y: x and y, res)

def distinct_indices(a, b):
    for i in a:
        for j in b:
            if i == j:
                return False
    return True

def xor(ha, hb):
    return bytearray(a^b for a,b in zip(ha,hb))

def gbp_basic(digest, n, k):
    '''Implementation of Basic Wagner's algorithm for the GBP.'''
    collision_length = n/(k+1)
    if DEBUG: print ('collision_length ', collision_length)
    hash_length = (k+1)*((collision_length+7)//8)
    indices_per_hash_output = 512/n
    if DEBUG: print ('indices_per_hash_output ', indices_per_hash_output)

    # 1) Generate first list
    if DEBUG: print 'Generating first list'
    X = []
    tmp_hash = ''
    if DEBUG and progressbar: bar = progressbar.ProgressBar()
    else: bar = lambda x: x
    for i in bar(range(0, 2**(collision_length+1))):
        r = i % indices_per_hash_output
        if r == 0:
            # X_i = H(I||V||x_i)
            curr_digest = digest.copy()
            hash_xi(curr_digest, i/indices_per_hash_output)
            tmp_hash = curr_digest.digest()
        X.append((
            expand_array(bytearray(tmp_hash[r*n/8:(r+1)*n/8]),
                         hash_length, collision_length),
            (i,)
        ))

    # 3) Repeat step 2 until 2n/(k+1) bits remain
    for i in range(1, k):
        if DEBUG: print 'Round %d:' % i

        # 2a) Sort the list
        if DEBUG: print '- Sorting list'
        X.sort(key=itemgetter(0))
        if DEBUG and VERBOSE:
            for Xi in X[-32:]:
                print '%s %s' % (print_hash(Xi[0]), Xi[1])

        if DEBUG: print '- Finding collisions'
        Xc = []
        if DEBUG and progressbar:
            orig_size = len(X)
            pbar = progressbar.ProgressBar(max_value=orig_size)
        while len(X) > 0:
            # 2b) Find next set of unordered pairs with collisions on first n/(k+1) bits
            j = 1
            while j < len(X):
                if not has_collision(X[-1][0], X[-1-j][0], i, collision_length):
                    break
                j += 1

            # 2c) Store tuples (X_i ^ X_j, (i, j)) on the table
            for l in range(0, j-1):
                for m in range(l+1, j):
                    # Check that there are no duplicate indices in tuples i and j
                    if distinct_indices(X[-1-l][1], X[-1-m][1]):
                        if X[-1-l][1][0] < X[-1-m][1][0]:
                            concat = X[-1-l][1] + X[-1-m][1]
                        else:
                            concat = X[-1-m][1] + X[-1-l][1]
                        Xc.append((xor(X[-1-l][0], X[-1-m][0]), concat))

            # 2d) Drop this set
            while j > 0:
                X.pop(-1)
                j -= 1
            if DEBUG and progressbar: pbar.update(orig_size - len(X))
        if DEBUG and progressbar: pbar.finish()
        # 2e) Replace previous list with new list
        X = Xc

    # k+1) Find a collision on last 2n(k+1) bits
    if DEBUG:
        print 'Final round:'
        print '- Sorting list'
    X.sort(key=itemgetter(0))
    if DEBUG and VERBOSE:
        for Xi in X[-32:]:
            print '%s %s' % (print_hash(Xi[0]), Xi[1])
    if DEBUG: print '- Finding collisions'
    solns = []
    if DEBUG and progressbar:
        orig_size = len(X)
        pbar = progressbar.ProgressBar(max_value=orig_size, redirect_stdout=True)
    while len(X) > 0:
        j = 1
        while j < len(X):
            if not (has_collision(X[-1][0], X[-1-j][0], k, collision_length) and
                    has_collision(X[-1][0], X[-1-j][0], k+1, collision_length)):
                break
            j += 1

        for l in range(0, j-1):
            for m in range(l+1, j):
                res = xor(X[-1-l][0], X[-1-m][0])
                if count_zeroes(res) == 8*hash_length and distinct_indices(X[-1-l][1], X[-1-m][1]):
                    if DEBUG and VERBOSE:
                        print 'Found solution:'
                        print '- %s %s' % (print_hash(X[-1-l][0]), X[-1-l][1])
                        print '- %s %s' % (print_hash(X[-1-m][0]), X[-1-m][1])
                    if X[-1-l][1][0] < X[-1-m][1][0]:
                        solns.append(list(X[-1-l][1] + X[-1-m][1]))
                    else:
                        solns.append(list(X[-1-m][1] + X[-1-l][1]))

        # 2d) Drop this set
        while j > 0:
            X.pop(-1)
            j -= 1
        if DEBUG and progressbar: pbar.update(orig_size - len(X))
    if DEBUG and progressbar: pbar.finish()
    return solns

def block_hash(prev_hash, nonce, soln):
    # H(I||V||x_1||x_2||...|x_2^k)
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(prev_hash)
    digest.update(nonce)
    # for xi in soln:
    #     hash_xi(digest, xi)
    #prefix = bytearray.fromhex('fd4005')
    prefix = bytearray.fromhex('44')
    digest.update(prefix)
    digest.update(soln)

    if DEBUG: print("input ", print_hash(prev_hash + nonce + prefix + soln))
    
    h = digest.finalize()
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(h)
    return digest.finalize()


def bare_hash(prev_hash):
    # H(I||V||x_1||x_2||...|x_2^k)
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(prev_hash)
    h = digest.finalize()
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(h)
    return digest.finalize()

def difficulty_filter(prev_hash, nonce, soln, d):
    h = block_hash(prev_hash, nonce, soln)
    if DEBUG: print("h ", print_hash(h))
    if DEBUG: print("d ", print_hash(d))

    cur = bytearray(h)
    for i in range(len(cur) - 1, 0, -1):
        if d[i] != cur[i]:
            return d[i] > cur[i]
    return 1
    
def blake_person(n, k):
    return b'OrigoPoW' + struct.pack('<II', n, k)

def print_hash(h):
    if type(h) == bytearray:
        return ''.join('{0:02x}'.format(x, 'x') for x in h)
    else:
        return ''.join('{0:02x}'.format(ord(x), 'x') for x in h)

def validate_params(n, k):
    if (k >= n):
        raise ValueError('n must be larger than k')
    if (((n/(k+1))+1) >= 32):
        raise ValueError('Parameters must satisfy n/(k+1)+1 < 32')

def str_to_hexStr(string):
    str_bin = string.encode('utf-8')
    return binascii.hexlify(str_bin)
