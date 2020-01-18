                                             Origo Private Transaction JSON-RPC APIs



**origo_getNewAddress**

Return a new private address for sending and receiving payments. The address will be added to the node’s wallet.


#### **Parameters**

1. password: String – The passord is used to encrypt the private address in the node's wallet.


**Returns**

1. address: String – The new private address.


**Example**

**Request**


```
curl --data '{"jsonrpc":"2.0","method":"origo_getNewAddress","params":["password"],"id":1}' -H "Content-Type: application/json" -X POST localhost:6622
```


**Response**


```
{"jsonrpc":"2.0","result":"ogo1dj3lwla9h4axf8wpqkuazyuzv3m0j3pdxuvm0x36q3wgm2y0qskkkzp7anznjtpemggswkmuwe0","id":1}
```



---


**origo_listAddresses**

Return all private addresses in the node's wallet.


#### **Parameters**

None

**Returns**



1. Array - A list of private addresses

**Example**

**Request**


```
curl --data '{"jsonrpc":"2.0","method":"origo_listAddresses","id":1}' -H "Content-Type: application/json" -X POST localhost:6622
```


**Response**


```
{"jsonrpc":"2.0","result":["ogo1dj3lwla9h4axf8wpqkuazyuzv3m0j3pdxuvm0x36q3wgm2y0qskkkzp7anznjtpemggswkmuwe0","ogo127hk2tmx3pktg0pvdskrtjal5yt9en5zn67vm3tuxau5v5vvvl8p34phy0n4znfq7h4f5n6l2yw"],"id":1}
```




---

**personal_sendShieldTransaction**

Send transaction from public address to private address and signs it in a single call. The account does not need to be unlocked to make this call, and will not be left unlocked after.


#### **Parameters**

1.     Object – The Shield Transaction Object



*   from: Address - 20 Bytes - The address the transaction is send from.
*   to: Address - 20 Bytes - (optional) The address the transaction is directed to.
*   gas: Quantity - Integer of the gas provided for the transaction execution.
*   gasPrice: Quantity - Integer of the gas price used for each paid gas.
*   value: Quantity - Integer of the value sent with this transaction, the value should be the multiple of 10^9.
*   data: Data - (optional) 4 byte hash of the method signature followed by encoded parameters. For details see Ethereum Contract ABI.
*   nonce: Quantity - (optional) Integer of a nonce. This allows to overwrite your own pending transactions that use the same nonce.
*   condition: Object - (optional) Conditional submission of the transaction. Can be either an integer block number or UTC timestamp (in seconds) or null.
*   shield_amouts: List – private amount info in shield transaction
    *   address: String – private address the transaction is directed to
    *   amount: Quantity – the numeric amount to the address
    *   memo: String – (optional) raw data represented in hexadecimal string

2.     String - Passphrase to unlock the from account




```
Params: [
{
    "from":"0x00a329c0648769a73afac7f9381e08fb43dbea72",
    "gas": "0x76c00", 
    "gasPrice": "0x9184e72a000", 
    "value": "0x174876e800", 
    "shieldAmounts": [
        {
        "address":"ogo180m058urhazk8j98zvz9fsq5zd0vd9dpsc8c6ednwd2xkc3l8z9thmxsezepzx4aascp6nrlkd6",
        "amount": "0x174876e800",
        "memo":"test"
        }
    ]
 },
"password123"
]
```

**Returns**



1. Data - 32 Bytes - the transaction hash, or the zero hash if the transaction is not yet available

**Example**

**Request**


```
curl --data '{"method":"personal_sendShieldTransaction","params":[{ "from":"0x00a329c0648769a73afac7f9381e08fb43dbea72","gas": "0x76c00", "gasPrice": "0x9184e72a000", "value": "0x174876e800", "shieldAmounts": [{"address":"ogo180m058urhazk8j98zvz9fsq5zd0vd9dpsc8c6ednwd2xkc3l8z9thmxsezepzx4aascp6nrlkd6","amount": "0x174876e800", "memo":"test" }] }, ""] ,"id":1,"jsonrpc":"2.0"}' -H "Content-Type: application/json" -X POST localhost:6622
```


**Response**


```
{
  "id": 1,
  "jsonrpc": "2.0",
  "result": "0x62e05075829655752e146a129a044ad72e95ce33e48ff48118b697e15e7b41e4"
}
```




---


**origo_getBalance**

Returns the balance of a private address belonging to the node’s wallet.


#### **Parameters**



1. address: String - The selected address. It may be a transparent or private address.
2. miniconf: Quantity - (optional) default = 1, Only include transactions confirmed at least this many times

**Returns**



1. Quantity - The total amount balance received for this address

**Example**

**Request**


```
curl --data '{"jsonrpc":"2.0","method":"origo_getBalance","params":["ogo127hk2tmx3pktg0pvdskrtjal5yt9en5zn67vm3tuxau5v5vvvl8p34phy0n4znfq7h4f5n6l2yw"],"id":1}' -H "Content-Type: application/json" -X POST localhost:6622
```


**Response**


```
{"jsonrpc":"2.0","result":"0x174876e800","id":1}
```




---


**origo_listUnspent**

Returns array of unspent shielded notes with between minconf and maxconf (inclusive) confirmations. Optionally filter to only include notes sent to specified addresses.


#### **Parameters**



1. address: - The private address to filter on.
2. miniconf: Quantity - (optional) default = 1, The minimum confirmations to filter
3. maxconf: Quantity -  (optional) default = 9999999, The maximum confirmations to filter
4. include_watch_only: bool -  (optional)  default = false, whether include watchonly addresses

**Returns**


1.     Object – The unspent note for the private address.



*   address: String - The private address to filter on.
*   amout: Quantity - amount of value in the note, it is multiple of 10^9.
*   change: Bool - true if the address received the note is also in the sending addresses.
*   confirmations: Quantity - number of confirmations, default is 0.
*   jsindex: Quantity - joinsplit index.
*   jsoutindex: Quantity - output index of the joinsplit.
*   memo: String – raw data represented in hexadecimal string for this note.
*   outindex: Quantity - output index of the transaction for this note.
*   spendable: Bool - True if note can be spent by wallet.
*   txid: 32 Bytes - the transaction hash include this note.

**Example**

**Request**


```
curl --data '{"jsonrpc":"2.0","method":"origo_listUnspent","params":["ogo1td987xe2lmhez8juecmnlk4mxfwe6m4jft8g20czh9kp5p4mfhqn8uf7cua3zh454p6uzc4z8td"],"id":1}' -H "Content-Type: application/json" -X POST localhost:6622
```


**Response**


```
{"jsonrpc":"2.0","result":[{"address":"ogo1td987xe2lmhez8juecmnlk4mxfwe6m4jft8g20czh9kp5p4mfhqn8uf7cua3zh454p6uzc4z8td","amount":"0x174876e800","change":false,"confirmations":"0x0","jsindex":"0x0","jsoutindex":"0x0","memo":"test","outindex":"0x0","spendable":true,"txid":"0x348c…89cf"}],"id":1}
```




---


**origo_sendMany**

Transfer value from private address to private address. while change generated from private address returns to itself.


#### **Parameters**



1. from: String - the from private address to transfer balance.
2. Amounts: Array - An array of json objects representing the amounts to send.
    *   address: String - the private address to send.
    *   Amount: Quantity - The value to send to the address，it should be multiple of 10^9.
    *   Memo: String - raw data represented in hexadecimal string format.
3. password: String - The passord is used to decrypt the from private address in the node's wallet.
4. miniconf: Quantity - (optional) default = 0, Only use funds confirmed at least this many times.
5. gas: Quantity - (optional), default=21000, The gas limit of the transaction.
6. gasPrice: Quantity - (optional), default=1, The gas price of the transaction.

**Returns**


1. Data - 32 Bytes - the transaction hash, or the zero hash if the transaction is not yet available

**Example**

**Request**


```
 curl --data '{"jsonrpc":"2.0","method":"origo_sendMany", "params":["ogo1mj73lnwek33kppywv520yfnt58thshan8rfacfpum6hcr2ftwt4kn50kdmlm5r3js3pcvcmtxp8", [{"address":"ogo1fklhxyhg0c20yaqkfkwyf2khtn7e3nme97y28nhlvdexcvzqytzhtuz46admr44vas99wpqjfqt", "amount":"0xba43b7400", "memo":"test" }], "password"],"id":1}' -H "Content-Type: application/json" -X POST localhost:6622
```


**Response**


```
{"jsonrpc":"2.0","result":"0x01458993fd9414eaad5b4bee990d5117aa0080f35c51906837fe1c0365d5af84","id":1}
```




---



<!-- Docs to Markdown version 1.0β17 -->
