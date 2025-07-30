## Bloom cascade

To install, run:
```
pip install bloom_cascade
```
To use it, first import it like this:
```
from bloom_cascade import Cascade
```
  
### Creating a cascade
Example of building a cascade:
```
cascade = Cascade()
R = set()
S = set()

for i in range(100):
    R.add(str(i))

for i in range(100,400):
    S.add(str(i))
  
cascade.build_cascade_blob(R, S) 
```

### Recreate a cascade from BLOB data
An example retriving a bloom cascade from a blob transaction on Holesky testnet, using the ```blobscan``` API:
```
import requests
import json
import hexbytes
from cascade import Cascade

clean_tx = '0x8fd37f5db4ab0e4c0b8dad166842d0ac7c3aeb86303a3bce3d5b19656dd65c2c'

tx_url = f"https://api.holesky.blobscan.com/transactions/{clean_tx}"
        
print(f" Requesting: {tx_url}")

# Get transaction details
response = requests.get(tx_url)

if response.status_code != 200:
    print(f" Transaction not found: HTTP {response.status_code}")
    print(f"Response: {response.text}")

tx_data = response.json()

print(f" Transaction found: {tx_data.get('hash', 'Unknown')}")
print(f" Block: {tx_data.get('blockNumber', 'Unknown')}")

if not tx_data.get('blobs'):
    print(" No blob versioned hashes found in transaction")


blob_hash = tx_data['blobs'][0]['versionedHash']
print(f" Found {len(blob_hash)} blob hash(es): {blob_hash}")

blobs_url = f"https://api.holesky.blobscan.com/blobs/{blob_hash}/data"
blobs_response = requests.get(blobs_url)

if blobs_response.status_code != 200:
    print(f" Could not retrieve blobs: HTTP {blobs_response.status_code}")


blobs_data = blobs_response.json()
blobs_data_bytes = bytes.fromhex(blobs_data[2:])



csd = Cascade()
# USE THE DEDICATED FUNCTION FOR PROCCESING BLOBS
csd.deserialize_cascade_blob(blobs_data_bytes)

for i in range(100):
    if csd.is_revoked(str(i)):
        print('d'+ str(i))

for i in range(100,200):
    if not csd.is_revoked(str(i)):
        print('R' + str(i))
```