from flask import Flask, request
from telegram import Bot
import os
import json
import time

app = Flask(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
bot = Bot(token=BOT_TOKEN)

ANALYTICS_FILE = "analytics.json"

def log_analytics(user_id, username, status):
    data = {
        "user_id": user_id,
        "username": username,
        "status": status,
        "timestamp": time.time()
    }
    with open(ANALYTICS_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

@app.route('/verify_callback', methods=['POST'])
def verify_callback():
    try:
        data = request.json
        user_id = data.get('tg_id')
        has_nft = data.get('has_nft')
        username = data.get('username', f'user_{user_id}')

        if not user_id:
            return {"error": "No user id"}, 400

        print(f"Processing verification for user {user_id} (has_nft: {has_nft})")

        if has_nft:
            # User has NFT - grant access
            try:
                bot.send_message(
                    chat_id=GROUP_ID, 
                    text=f"✅ <b>Verification Successful!</b>\n\n👤 @{username} has been verified and granted access to the group.\n\n🎉 Welcome to Meta Betties Private Key!",
                    parse_mode='HTML'
                )
                print(f"User {user_id} verified successfully")
                log_analytics(user_id, username, "verified")
            except Exception as e:
                print(f"Error sending verification message: {e}")
            return {"status": "verified"}, 200
        else:
            # User doesn't have NFT - remove from group
            try:
                bot.ban_chat_member(chat_id=GROUP_ID, user_id=user_id)
                bot.unban_chat_member(chat_id=GROUP_ID, user_id=user_id)  # So they can rejoin if they verify later
                bot.send_message(
                    chat_id=GROUP_ID, 
                    text=f"❌ <b>Access Denied</b>\n\n👤 @{username} was removed for not holding the required NFT.\n\n💡 To rejoin, please acquire the required NFT and verify again.",
                    parse_mode='HTML'
                )
                print(f"User {user_id} removed for not having NFT")
                log_analytics(user_id, username, "removed")
            except Exception as e:
                print(f"Error removing user {user_id}: {e}")
            return {"status": "removed"}, 200

    except Exception as e:
        print(f"Error in verify_callback: {e}")
        return {"error": str(e)}, 500

@app.route('/health', methods=['GET'])
def health_check():
    return {"status": "healthy"}

if __name__ == '__main__':
    print("🔗 Webhook server starting on port 5000...")
    app.run(port=5000, debug=True) 