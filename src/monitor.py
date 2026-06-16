import asyncio
import httpx
import json
import os
from datetime import datetime
from alerts import send_telegram_alert

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, 'config', 'targets.json')

target_states = {}

async def check_target(target: dict):
    """Infinite monitoring loop with state tracking for a specific target"""
    name = target['name']
    url = target['url']
    interval = target['interval']
    expected_status = target['expected_status']

    target_states[url] = False

    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
        while True:
            try:
                response = await client.get(url)
                
                if response.status_code != expected_status:
                    if not target_states[url]:
                        msg = (f"🚨 <b>ALERT: {name}</b>\n"
                               f"URL: {url}\n"
                               f"Status: {response.status_code} (Expected: {expected_status})")
                        print(msg.replace('<b>', '').replace('</b>', ''))
                        await send_telegram_alert(msg)
                        target_states[url] = True 
                else:
                    if target_states[url]: 
                        msg = f"✅ <b>RECOVERED: {name}</b>\nURL: {url}\nService is back online!"
                        print(msg.replace('<b>', '').replace('</b>', ''))
                        await send_telegram_alert(msg)
                        target_states[url] = False 
                        
                    time_now = datetime.now().strftime('%H:%M:%S')
                    print(f"[{time_now}] ✅ {name} is UP ({response.status_code})")
                    
            except httpx.TimeoutException:
                if not target_states[url]:
                    msg = f"🐢 <b>TIMEOUT: {name}</b>\nURL: {url}\nService is taking too long to respond (>10s)!"
                    print(msg.replace('<b>', '').replace('</b>', ''))
                    await send_telegram_alert(msg)
                    target_states[url] = True
                
            except Exception as e:
                if not target_states[url]:
                    msg = f"🔥 <b>CRITICAL DOWN: {name}</b>\nURL: {url}\nError: {type(e).__name__}"
                    print(msg.replace('<b>', '').replace('</b>', ''))
                    await send_telegram_alert(msg)
                    target_states[url] = True

            await asyncio.sleep(interval)

async def main():
    print("🚀 Starting OpsPulse Asynchronous Monitor...")
    
    if not os.path.exists(CONFIG_PATH):
        print(f"❌ Error: Config file not found at {CONFIG_PATH}")
        return
        
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        targets = json.load(f)
        
    print(f"📊 Loaded {len(targets)} targets for monitoring.\n")

    tasks = [check_target(target) for target in targets]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Monitor stopped by user.")