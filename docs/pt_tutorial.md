                                         My First Origo private Transaction

This document will guide you through executing your first private transaction on the Origo Blockchain. Before you follow the steps to execute your first transaction, we recommend that you read the following documents to familiarize yourself with the[ JSON-RPC Origo interface](private_transaction.md).

**Steps to Submit a Transaction**

In this example,  you need to download the Origo blockchain binary and execute the origo private transaction between two users: A and B.

Perform the following steps to submit a private transaction to the full node on the Origo network.



1. **Setup the Origo blockchain network**
2. **Create the public address for user A**
3. **Create the private address for user A and user B**
4. **Submit shield transaction from A’s public address to A’s private address**
5. **Submit private transaction from A’s private address to B’s private address**

**Setup Origo Blockchain network**

**Step 1: Download the Origo blockchain binary**

Download the Origo Blockchain Binary from [releases](https://github.com/origolab/origo-binary/releases), please choose right version for your operating system.

**Step 2: Connecting to Medietas mainnet**

To start the mainnet,  change to the binary directory and run the command as below:


```
./origo  --jsonrpc-apis=all
```


**Create the public address for user A**

We use the following command to create a public address for user A and set a password:

```
curl --data '{"method":"personal_newAccount","params":["password"],"id":1,"jsonrpc":"2.0"}' -H "Content-Type: application/json" -X POST localhost:6622
```

It should return an address like this:


```
{"jsonrpc":"2.0","result":"0x00a329c0648769a73afac7f9381e08fb43dbea72","id":1}
```


**Create private address for user A and User B**

**Step 1: Create A’s private Address**

To create A’s private address, using the origo_getNewAddress shown in [JSON-RPC Origo interface](https://github.com/origolab/origo-binary/blob/master/docs/private_transaction.md). The command:


```
curl --data '{"jsonrpc":"2.0","method":"origo_getNewAddress","params":["password"],"id":1}' -H "Content-Type: application/json" -X POST localhost:6622
```


Sample output on success:


```
{"jsonrpc":"2.0","result":"ogo1rcgj5almqeg22zuneqjd7eqfnsw6hntlwkn5udrxsygc0r244nk0g776akc96qv4z547y5k8hx2","id":1}
```


Then the private address for A is:` ogo1rcgj5almqeg22zuneqjd7eqfnsw6hntlwkn5udrxsygc0r244nk0g776akc96qv4z547y5k8hx2`

**Step 2: Create B’s private Address**

To create B’s private address, repeat the command:


```
curl --data '{"jsonrpc":"2.0","method":"origo_getNewAddress","params":["password"],"id":1}' -H "Content-Type: application/json" -X POST localhost:6622
```


 Sample output on success:


```
{"jsonrpc":"2.0","result":"ogo175j7xj6jgn3w0trmxzmssydmdq5rd9vxydwdqmd9t6qkykrr0y24w6xfp44knukqjweuxxa9mel","id":1}
```


Then the private address for B is:` ogo175j7xj6jgn3w0trmxzmssydmdq5rd9vxydwdqmd9t6qkykrr0y24w6xfp44knukqjweuxxa9mel`

**Step 3: List All the private Addresses**

To list all the private addresses you have created, enter this command:


```
curl --data '{"jsonrpc":"2.0","method":"origo_listAddresses","id":1}' -H "Content-Type: application/json" -X POST localhost:6622
```


 Sample output on success:


```
{"jsonrpc":"2.0","result":["ogo180m058urhazk8j98zvz9fsq5zd0vd9dpsc8c6ednwd2xkc3l8z9thmxsezepzx4aascp6nrlkd6","ogo175j7xj6jgn3w0trmxzmssydmdq5rd9vxydwdqmd9t6qkykrr0y24w6xfp44knukqjweuxxa9mel","ogo1rcgj5almqeg22zuneqjd7eqfnsw6hntlwkn5udrxsygc0r244nk0g776akc96qv4z547y5k8hx2"],"id":1}
```


**Submit shield transaction from A’s public address to A’s private address**

**Step 1: Submit the shield transaction**

To send balance from A’s public address to A’s private address, the command as below:

_Note: Please **replace the address 0x00a329c0648769a73afac7f9381e08fb43dbea72 to A's public address, and replace the address ogo180m058urhazk8j98zvz9fsq5zd0vd9dpsc8c6ednwd2xkc3l8z9thmxsezepzx4aascp6nrlkd6** to A’s private address.

```
curl --data '{"method":"personal_sendShieldTransaction","params":[{ "from":"0x00a329c0648769a73afac7f9381e08fb43dbea72","gas": "0x76c00", "gasPrice": "0x9184e72a000", "value": "0x174876e800", "shieldAmounts": [{"address":"ogo180m058urhazk8j98zvz9fsq5zd0vd9dpsc8c6ednwd2xkc3l8z9thmxsezepzx4aascp6nrlkd6","amount": "0x174876e800", "memo":"test" }] }, ""] ,"id":1,"jsonrpc":"2.0"}' -H "Content-Type: application/json" -X POST localhost:6622
```


 Sample output on success:


```
{"jsonrpc":"2.0","result":"0x6cbdaf0c766c3cafe3553c4687a0c1bb3579d40cbe016806d5225e7ed6c6bcfd","id":1}
```


**Step 2: List the Unspent Transaction for A’s private Address**

To show the unspent transaction for A’s address, the command:


```
curl --data '{"jsonrpc":"2.0","method":"origo_listUnspent","params":["ogo180m058urhazk8j98zvz9fsq5zd0vd9dpsc8c6ednwd2xkc3l8z9thmxsezepzx4aascp6nrlkd6"],"id":1}' -H "Content-Type: application/json" -X POST localhost:6622
```


 Sample output on success:


```
{"jsonrpc":"2.0","result":[{"address":"ogo180m058urhazk8j98zvz9fsq5zd0vd9dpsc8c6ednwd2xkc3l8z9thmxsezepzx4aascp6nrlkd6","amount":"0x174876e800","change":false,"confirmations":"0x0","jsindex":"0x0","jsoutindex":"0x0","memo":"","outindex":"0x0","spendable":true,"txid":"0x5dfe…c967"}],"id":1}
```


**Step 3: List the Balance for A’s private Address**

To show the balance for A’s private address, the command:


```
curl --data '{"jsonrpc":"2.0","method":"origo_getBalance","params":["ogo180m058urhazk8j98zvz9fsq5zd0vd9dpsc8c6ednwd2xkc3l8z9thmxsezepzx4aascp6nrlkd6"],"id":1}' -H "Content-Type: application/json" -X POST localhost:6622
```


Sample output on success:


```
{"jsonrpc":"2.0","result":"0x174876e800","id":1}
```


The result balance is same with the shield transaction submitted.

**Submit private transaction from A’s private address to B’s private address**

**Step 1: Submit the private transaction**

To submit the private transaction from A’s private address to B’s private address, the command as below:


```
curl --data '{"jsonrpc":"2.0","method":"origo_sendMany", "params":["ogo180m058urhazk8j98zvz9fsq5zd0vd9dpsc8c6ednwd2xkc3l8z9thmxsezepzx4aascp6nrlkd6", [{"address":"ogo175j7xj6jgn3w0trmxzmssydmdq5rd9vxydwdqmd9t6qkykrr0y24w6xfp44knukqjweuxxa9mel", "amount":"0xba43b7400", "memo":"test" }],"password"],"id":1}' -H "Content-Type: application/json" -X POST localhost:6622
```


 Sample output on success:


```
{"id":1,"jsonrpc":"2.0","result":"0x62e05075829655752e146a129a044ad72e95ce33e48ff48118b697e15e7b41e4"}
```


**Step 2: List the Unspent Transaction for B’s private Address**

To show the unspent transaction for B’s address, the command:


```
curl --data '{"jsonrpc":"2.0","method":"origo_listUnspent","params":["ogo175j7xj6jgn3w0trmxzmssydmdq5rd9vxydwdqmd9t6qkykrr0y24w6xfp44knukqjweuxxa9mel"],"id":1}' -H "Content-Type: application/json" -X POST localhost:6622
```


 Sample output on success:


```
{"jsonrpc":"2.0","result":[{"address":"ogo175j7xj6jgn3w0trmxzmssydmdq5rd9vxydwdqmd9t6qkykrr0y24w6xfp44knukqjweuxxa9mel","amount":"0xba43b7400","change":false,"confirmations":"0x0","jsindex":"0x0","jsoutindex":"0x0","memo":"","outindex":"0x0","spendable":true,"txid":"0x5dfe…c967"}],"id":1}
```


**Step 3: List the Balance for B’s private Address**

To show the balance for B’s private address, the command:


```
curl --data '{"jsonrpc":"2.0","method":"origo_getBalance","params":["ogo175j7xj6jgn3w0trmxzmssydmdq5rd9vxydwdqmd9t6qkykrr0y24w6xfp44knukqjweuxxa9mel"],"id":1}' -H "Content-Type: application/json" -X POST localhost:6622
```


Sample output on success:


```
{"jsonrpc":"2.0","result":"0xba43b7400","id":1}
```


The result balance is same with the private transaction submitted.


### **Congratulations!**

You have successfully executed your private transaction on the Origo testnet and submit the shield transaction from A’s public address to private address and private transaction from A’s private address to B’s private address.


<!-- Docs to Markdown version 1.0β17 -->
