import subprocess
import sys
import time
import threading
import os
import signal
import psutil

def kill_existing_processes():
    """Kill any existing Python processes running our services"""
    print("🔍 Checking for existing processes...")
    killed = 0
    current_pid = os.getpid()
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Skip the current process (start_bot.py)
            if proc.info['pid'] == current_pid:
                continue
                
            cmdline = proc.info['cmdline']
            if cmdline and any('bot.py' in str(arg) or 'webhook.py' in str(arg) or 'api_server.py' in str(arg) for arg in cmdline):
                print(f"🛑 Killing existing process: {proc.info['name']} (PID: {proc.info['pid']})")
                proc.terminate()
                proc.wait(timeout=5)
                killed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            pass
    
    if killed > 0:
        print(f"✅ Killed {killed} existing processes")
        time.sleep(2)  # Wait for processes to fully terminate
    else:
        print("✅ No existing processes found")

def run_service(service_name, command):
    """Run a service in a subprocess"""
    print(f"🚀 Starting {service_name}...")
    try:
        # Use subprocess.Popen with proper shell=False for better control
        if sys.platform == "win32":
            process = subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            process = subprocess.Popen(command, shell=True)
        
        print(f"✅ {service_name} started with PID: {process.pid}")
        return process
    except Exception as e:
        print(f"❌ Failed to start {service_name}: {e}")
        return None

def main():
    print("🤖 Starting NFT-Gated Telegram Bot...")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found! Please create it with your configuration.")
        print("Required variables: BOT_TOKEN, GROUP_ID, COLLECTION_ID, RPC_ENDPOINT, HELIUS_API_KEY")
        return
    
    # Kill existing processes first
    kill_existing_processes()
    
    # Start services in order
    services = [
        ("Webhook Server", "python webhook.py"),
        ("API Server", "python api_server.py"),
        ("Telegram Bot", "python bot.py")
    ]
    
    processes = []
    
    try:
        # Start all services
        for service_name, command in services:
            process = run_service(service_name, command)
            if process:
                processes.append((service_name, process))
            time.sleep(3)  # Longer delay between starts
        
        print("\n🎉 All services started successfully!")
        print("📱 Bot is now running and ready to verify users.")
        print("🌐 Verification page: http://localhost:3000")
        print("🔗 Webhook: http://localhost:5000")
        print("🔗 API Server: http://localhost:5001")
        print("\nPress Ctrl+C to stop all services...")
        
        # Keep running until interrupted
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping all services...")
        for service_name, process in processes:
            try:
                process.terminate()
                print(f"✅ {service_name} stopped")
            except:
                pass
        print("👋 All services stopped. Goodbye!")

if __name__ == "__main__":
    main() 