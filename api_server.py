from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from verifier import has_nft

load_dotenv()

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:5001",
    "http://localhost:3000",
    "http://127.0.0.1:5001",
    "http://127.0.0.1:3000",
    "https://*.netlify.app",  # Allow Netlify domains
    "https://*.vercel.app",   # Allow Vercel domains
    "https://*.railway.app"   # Allow Railway domains
])

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://localhost:5000/verify_callback")  # Your bot's webhook URL

@app.route('/verify.html')
def verify_page():
    return send_from_directory('.', 'website_example.html')

@app.route('/api/config')
def get_config():
    """Return configuration data including API keys"""
    return jsonify({
        "helius_api_key": os.getenv("HELIUS_API_KEY", "")
    })

@app.route('/api/verify-nft', methods=['POST'])
def verify_nft():
    try:
        data = request.json
        wallet_address = data.get('wallet_address')
        tg_id = data.get('tg_id')
        
        if not wallet_address or not tg_id:
            return jsonify({"error": "Missing wallet_address or tg_id"}), 400
        
        # Check NFT ownership using your verifier
        has_required_nft = has_nft(wallet_address)
        
        # Send result to bot's webhook
        webhook_data = {
            "tg_id": tg_id,
            "has_nft": has_required_nft,
            "username": f"user_{tg_id}"  # You might want to get actual username from bot
        }
        
        try:
            webhook_response = requests.post(WEBHOOK_URL, json=webhook_data, timeout=10)
            if webhook_response.status_code == 200:
                print(f"Webhook sent successfully for user {tg_id}")
            else:
                print(f"Webhook failed for user {tg_id}: {webhook_response.status_code}")
        except Exception as e:
            print(f"Error sending webhook: {e}")
        
        return jsonify({
            "has_nft": has_required_nft,
            "wallet_address": wallet_address,
            "message": "NFT verification completed"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=False) 