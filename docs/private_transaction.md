                                             Origo Private Transaction JSON-RPC APIs



**personal_sendShieldTransaction**

Sends transaction and signs it in a single call. The account does not need to be unlocked to make this call, and will not be left unlocked after.


#### **Parameters**

1.     Object – The Shield Transaction Object



*   from: Address - 20 Bytes - The address the transaction is send from.
*   to: Address - (optional) 20 Bytes - The address the transaction is directed to.
*   gas: Quantity - (optional) Integer of the gas provided for the transaction execution.
*   gasPrice: Quantity - (optional) Integer of the gas price used for each paid gas.
*   value: Quantity - (optional) Integer of the value sent with this transaction.
*   data: Data - (optional) 4 byte hash of the method signature followed by encoded parameters. For details see Ethereum Contract ABI.
*   nonce: Quantity - (optional) Integer of a nonce. This allows to overwrite your own pending transactions that use the same nonce.
*   condition: Object - (optional) Conditional submission of the transaction. Can be either an integer block number or UTC timestamp (in seconds) or null.
*   shield_amouts: List – shield amount info in shield transaction
    *   address: ZAddress – shiled address the transaction is directed to
    *   amount: Quantity – the numeric amount to the address
    *   memo: String – (optional) raw data represented in hexadecimal string

2.     String - Passphrase to unlock the from account




```
Params: [
{
    "from":"0x00a329c0648769a73afac7f9381e08fb43dbea72",
    "to": "0xd46e8dd67c5d32be8058bb8eb970870f07244567",
    "gas": "0x76c0",
    "gasPrice": "0x9184e72a000",
    "value": "0x9184e72a",
    "shieldAmounts": [
        {
        "address":"ox0000000000000000000000000000000000000001",
        "amount": 32,
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
curl --data '{"method":"personal_sendShieldTransaction","params":[{ "from":"0x00a329c0648769a73afac7f9381e08fb43dbea72","to": "0xd46e8dd67c5d32be8058bb8eb970870f07244567", "gas": "0x76c0", "gasPrice": "0x9184e72a000", "value": "0x9184e72a", "shieldAmounts": [{"address":"ogo127hk2tmx3pktg0pvdskrtjal5yt9en5zn67vm3tuxau5v5vvvl8p34phy0n4znfq7h4f5n6l2yw", "amount": 32, "memo":"test" }] }, "password123"] ,"id":1,"jsonrpc":"2.0"}' -H "Content-Type: application/json" -X POST localhost:6622
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


**origo_getNewAddress**

Return a new private address for sending and receiving payments. The spending key for this zaddr will be added to the node’s wallet.


#### **Parameters**

None

**Returns**



1. String - The new private address

**Example**

**Request**


```
curl --data '{"jsonrpc":"2.0","method":"origo_getNewAddress","id":1}' -H "Content-Type: application/json" -X POST localhost:6622
```


**Response**


```
{"jsonrpc":"2.0","result":"ogo1dj3lwla9h4axf8wpqkuazyuzv3m0j3pdxuvm0x36q3wgm2y0qskkkzp7anznjtpemggswkmuwe0","id":1}
```




---


**origo_listAddresses**

Return all stored private addresses


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
{"jsonrpc":"2.0","result":"0x0","id":1}
```




---


**origo_listUnspent**

Returns array of unspent shielded notes with between minconf and maxconf (inclusive) confirmations. Optionally filter to only include notes sent to specified addresses.


#### **Parameters**



1. addresses: - A json array of private addresses to filter on. Duplicate addresses not allowed.
2. miniconf: Quantity - (optional) default = 1, The minimum confirmations to filter
3. maxconf: Quantity -  (optional) default = 9999999, The maximum confirmations to filter
4. include_watch_only: bool -  (optional)  default = false, whether include watchonly addresses

**Returns**



1. Data - 32 Bytes - the transaction hash, or the zero hash if the transaction is not yet available

**Example**

**Request**


```
curl --data '{"jsonrpc":"2.0","method":"origo_listUnspent","params":["ogo127hk2tmx3pktg0pvdskrtjal5yt9en5zn67vm3tuxau5v5vvvl8p34phy0n4znfq7h4f5n6l2yw",2, 5, false],"id":1}' -H "Content-Type: application/json" -X POST localhost:6622
```


**Response**


```
{"jsonrpc":"2.0","result":[{"address":"ogo127hk2tmx3pktg0pvdskrtjal5yt9en5zn67vm3tuxau5v5vvvl8p34phy0n4znfq7h4f5n6l2yw","amount":"0x20","change":false,"confirmations":"0x0","jsindex":"0x0","jsoutindex":"0x0","memo":"","outindex":"0x0","spendable":true,"txid":"0xda7d…b29e"}],"id":1}
```




---


**origo_sendMany**

Send multiple private transactions. Amounts are decimal numbers with at most 8 digits of precision.while change generated from private address returns to itself.


#### **Parameters**



1. fromaddress: String - the private address to send the funds from
2. Amounts: Array - An array of json objects representing the amounts to send.
    *   address: String - the private address to send
    *   Amount: Quantity - The value to send to the address
    *   Memo: String - raw data represented in hexadecimal string format
3. miniconf: Quantity - (optional) default = 0, Only use funds confirmed at least this many times.
4. fee: Quantity - (optional), default=0, The fee amount to attach to this transaction

**Returns**



1. Data - 32 Bytes - the transaction hash, or the zero hash if the transaction is not yet available

**Example**

**Request**


```
curl --data '{"jsonrpc":"2.0","method":"origo_sendMany", "params":["ogo127hk2tmx3pktg0pvdskrtjal5yt9en5zn67vm3tuxau5v5vvvl8p34phy0n4znfq7h4f5n6l2yw", [{"address":"ogo1gs2uw342alp7z49xgm2a4hshj53cwnl4ml0ardxqe8ewtl3ynut2dhq6f0n2rzf7rglv7jeksxe", "amount": 32, "memo":"test" }], 5, 12],"id":1}' -H "Content-Type: application/json" -X POST localhost:6622
```


**Response**


```
{"jsonrpc":"2.0","result":"0x01458993fd9414eaad5b4bee990d5117aa0080f35c51906837fe1c0365d5af84","id":1}
```




---



<!-- Docs to Markdown version 1.0β17 -->
