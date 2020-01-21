# Origo Mining Guide

Welcome, this guide is intended to get you mining "ogo" with the Origo mainnet, we've chosen [EquiHash](https://en.wikipedia.org/wiki/Equihash) as our PoW algorithm, which is a memory-hard Proof-of-Work algorithm and is based on a generalization of the Birthday problem to finds colliding hash values. The unit for mining is **Sol/s** (solution per second).

## GPU Mining
Because the CPU has limitd performance on the PoW race, and too inefficient to hold any value, we suggest you mine with GPU card. 
Please Follow this guide, which will help you mine with GPU card with the our gpu miner.

### Requirement

We only verified the miner in the below environment:
* Ubuntu 18.04 LTS / Ubuntu 16.04 LTS
* GTX 1070 / GTX 1070 Ti / GTX 1080 / GTX 1080 Ti

#### intall Nvidia Driver

Install NVIDIA driver on your system:
```
ubuntu-drivers autoinstall
```
#### Python 3

Install Python3 and OpenCL headers:

```
sudo apt update
sudo apt install -y nvidia-opencl-dev python3
```

### Tutorial

#### Step 1: Download the Origo blockchain binary

Download the Origo Blockchain Binary from [releases](https://github.com/origolab/origo-binary/releases), please choose right version for your operating system.

#### Step 2: Connecting to Origo mainnet 

Create a `config.toml` file as below, **be careful to config your own mining wallet address**:

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

Starting full node as below:

```
./origo --config config.toml
```

#### Step 3: Start mining

Download [GPU Miner](../tools/miner/gpuminer) to your machine, then run miner. Here is an example:

```
./ogominer --use 0,1,2
```
the parameter of `--use` chooses the GPU card for mining, `0,1,2` is an example that chooses the GPU card index of 0 and 1 and 2 for mining, you can use `nvidia-smi` to get the list of GPU card of your system.

## Detail of mining
If you want to mining "ogo" with your own miner, you can get the detail here, We assume that you are professional with Equihash algorithm. 
### Equihash parameter
```
 Equihash (n, k) :          (192, 7) 
 Blake2b personal string :  "OrigoPow"
 nonce length :             32 bytes
```
### PoW
The input of Equihash is 64 bytes hash of block header, `keccak512` is the hash algorithm, so the input is 
```
 pow_hash = keccak512(block_header)
```
when the miner finds a `solution` of Equihash, the proof of work will be checked as follow
```
sha256 ( sha256 ( pow_hash + nonce + solution_prefix + solution ) ) <= target
```
the solution_prefix is the compact size of solution, for (192, 7) the solution size is `400`, so the solution_prefix is `0xfd9001`, the target is calculate from current difficulty. if the check have been passed that the solution meet the difficulty requirement and the block have been mined.
### interface of mining
The miner can get work from Origo node by stratum protocol，follow is describe of the protocol
#### stratum
##### authorize
register miner
```
{"id": x, "method": "mining.authorize", "params": ["user_name", "user_secret"]}
```
##### notify 
new mining work notify
```
{"id": x, "method": "mining.notify", "params": ["task_id", "pow_hash", "target", "job_id"] }
```
##### subscribe 
get work from node
```
request
{"params": [], "id":"x", "method": "mining.subscribe"}

response
{"result": ["task_id", "pow_hash", "target", "job_id"], "id":"x"}
```
##### submit 
submit solution to the node
```
submit: 
{"params":  ["task_id", "job_id", "pow_hash", "nonce", "solution"], "id": "y", "method":"mining.submit"}

response of success
 {"result":true,"id":y}  
```

If you have any question about the mining of Origo, you can contact with us.
