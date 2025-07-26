import requests, os
from dotenv import load_dotenv

load_dotenv()
COLLECTION_ID = os.getenv("COLLECTION_ID")
RPC_ENDPOINT = os.getenv("RPC_ENDPOINT")
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")

def has_nft(wallet_address):
    print(f"🔍 Checking NFT for wallet: {wallet_address}")
    print(f"📋 Collection ID: {COLLECTION_ID}")
    print(f"🔑 Helius API Key: {HELIUS_API_KEY[:10]}..." if HELIUS_API_KEY else "❌ No API Key")
    
    url = f"https://api.helius.xyz/v0/addresses/{wallet_address}/nft-assets?api-key={HELIUS_API_KEY}"
    print(f"🌐 API URL: {url}")
    
    try:
        response = requests.get(url)
        print(f"📡 API Response Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ API Error: {response.text}")
            return False

        nfts = response.json()
        print(f"🎨 Total NFTs found: {len(nfts)}")
        
        for i, nft in enumerate(nfts):
            if nft.get("grouping"):
                print(f"🔍 NFT {i+1} groupings: {nft['grouping']}")
                if COLLECTION_ID in str(nft["grouping"]):
                    print(f"✅ Required NFT found!")
                    return True
            else:
                print(f"🔍 NFT {i+1}: No grouping data")
        
        print(f"❌ No required NFT found in wallet")
        return False
        
    except Exception as e:
        print(f"❌ Error checking NFTs: {e}")
        return False 