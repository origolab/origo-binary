## CPU Mining Tutorial

### Miner Client

We choose [EquiHash](https://en.wikipedia.org/wiki/Equihash) as our PoW algorithm, we build a miner client which can do equihash mining with cpu. because the cpu is weak on the pow race. so it is only suite for test and study Origo.

### Stratum

Miner client connects to Origo node by [Stratum Protocol](https://en.bitcoinwiki.org/wiki/Stratum_mining_protocol).  Default ip:port binding is `0.0.0.0:8008`. There are two major messages `subscribe` and `submit` for client to mine with node.

#### Subscribe

Requesting message from `Miner` to `Full Node` to get current mining block:

Request Format:
```
{"params": [], "id":"id", "method": "mining.subscribe"}
```
Sample Request
```
{"params": [], "id":"1", "method": "mining.subscribe"}
```

Response Format
```
{"result":["job_id","pow_hash","target","block_number"], "id":"id"}
```
Sample Response
```
{"result":["0x","0xd2fe47ed1d9c3f0b17991f02825f750383b83ffd6fffee0a2f5102becf092321","0x4000000000000000000000000000000000000000000000000000000000000000","0x2"],"id":1}
```

Fields Specification
* `job_id`: mining job id
* `pow_hash`: 32 Bytes - the hash of block header (without pow solution).
* `target`: 32 Bytes - difficulty target for current block.
* `block_number`: 32 Bytes - current mining block number


#### Submit

Submitting message from miner to node to submit a solution.

Message Format
```
{"params": [1, "job_id", "pow_hash", "nonce", "solution"], "id": "id, "method": "mining.submit"}
```
Sample Message
```
{"params": [1, "0x3", "0xded589e98f675dfd7c885d20ab45295b1db7d17488639869ff944ec16d58c243", "0800000000000000000000000000000000000000000000000000000000000000", "12c0b3a6de9f75e762a07631b644ad6c8051ca4d265d8711913631ecbeb3a783da6442be3c5552f1d70a64b764f04a2e7b8b07456caa9fee49ffb5f8f50dcae2772fb919"], "id": 3, "method": "mining.submit"}
```

Fields Specification
* `job_id`: mining job id
* `pow_hash`: 32 Bytes - the hash of block header (without pow solution).
* `nonce`: 32 Bytes - equihash nonce.
* `solution`: 68 Bytes - equihash solution.

### Tutorial

**Step 1: Download the Origo blockchain binary**

Download the Origo Blockchain Binary from [releases](https://github.com/origolab/origo-binary/releases), please choose right version for your operating system.

**Step 2: Start Origo testnet**

To start the testnet, save below content as `config_miner.toml`:

```
[mining]
# Change this address to your own mining wallet address
author = "0x7a93b005d71d402ff5b88f812e0e04db7e2fb2f4"
force_sealing = true
reseal_on_txs = "all"
reseal_min_period = 4000
reseal_max_period = 60000
tx_queue_size = 8192

[stratum]
# Enable stratum
disable = false

```

Then start full node via this command:
```
./origo --config=config_miner.toml
```

**Step 3: Start Mining Client**

First, `cd` to the miner directory:
```
cd tools/miner/cpuminer-py
```

Then, install required pip packages in your local Python environment. If you have not install Python, please install Python 2.7 first, miner client can only run on Python 2.7.
```
pip install -r requirements.txt
```

Lastly, run mining server script:
```
python server.py
```

If everything is correctly configured, you will see these logs:
```
DEBUG:stratum-client:connecting to 127.0.0.1:8008...
INFO:stratum-client:connected to 127.0.0.1:8008
DEBUG:stratum-client:mining.subscribe(()) took 0.572919845581ms
Miner starting
Nonce: 0
hash less than difficulty
-----------------
Mined block!
Pow hash: 37d716c808c1c3cbcaa656ade3f12ce2320f7419e24ed1b591ae97c8c1b35bf4
Proof hash:  ebce7cae82721b5e52ca813e918a5f1df112a27a906c0cc1bae7c26ed0a3da19
Nonce:         0000000000000000000000000000000000000000000000000000000000000000
Solution:
('           ', [7616, 22826, 26651, 80025, 33022, 68809, 33872, 49565, 40734, 91951, 99926, 131056, 78638, 127239, 95966, 114577, 19602, 30561, 91412, 127840, 74302, 74624, 87161, 116253, 22405, 73391, 54733, 125143, 30302, 62898, 57917, 91079])
('           ', '0ee0164a8d0373899407f4332508a0c19d4f8f59cbf0cadfff099977c41eedbdbf9126491dd86ca29f360911f48e02a8f3c61d2bc2c7abdab9be8d73b2f3d6c9c47b63c7')
Time to find:  0:00:07.328608
-----------------

```