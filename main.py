import asyncio
import datetime
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

# 允许跨域，方便前端开发
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 数据模型 ---
class SpiderConfig(BaseModel):
    api_type: str
    page_count: int
    start_date: str

# --- 全局状态 (模拟数据库/Redis) ---
is_running = False
logs = []

def add_log(message: str, type: str = "info"):
    """添加日志，带时间戳"""
    time_str = datetime.datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{time_str}] {message}"
    logs.append(log_entry)
    # 保持日志列表不过大，只保留最后1000条
    if len(logs) > 1000:
        logs.pop(0)

async def scan_task(config: SpiderConfig):
    """
    模拟核心扫描逻辑 (替代原作者的私有代码)
    这里展示的是逻辑框架，你可以填入真实的 request/socket 扫描代码
    """
    global is_running
    add_log(f"后台采集任务启动: 类型={config.api_type}, 页数={config.page_count}, 日期: {config.start_date}")
    
    current_page = 1
    while is_running and current_page <= config.page_count:
        add_log(f"正在采集第 {current_page} 页...")
        await asyncio.sleep(1.5) # 模拟网络延迟
        
        # 模拟发现IP
        found_ips = random.randint(5, 20)
        add_log(f"采集到 {found_ips} 个IP，开始处理...")
        
        for _ in range(found_ips):
            if not is_running: break
            # 生成随机IP模拟
            ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}:8080"
            
            # 模拟检测逻辑
            check_time = random.uniform(0.1, 0.5)
            await asyncio.sleep(check_time)
            
            if random.choice([True, False]):
                add_log(f"{ip} ✓ (可用)", "success")
            else:
                add_log(f"{ip} ✗ (无效)", "error")
        
        current_page += 1
    
    if is_running:
        add_log("采集任务完成。", "success")
        is_running = False
    else:
        add_log("用户手动停止采集。", "warning")

# --- API 接口 ---

@app.post("/api/start")
async def start_spider(config: SpiderConfig, background_tasks: BackgroundTasks):
    global is_running, logs
    if is_running:
        return {"status": "error", "message": "任务已经在运行中"}
    
    is_running = True
    logs = [] # 每次启动清空旧日志
    background_tasks.add_task(scan_task, config)
    return {"status": "success", "message": "任务已启动"}

@app.post("/api/stop")
async def stop_spider():
    global is_running
    is_running = False
    return {"status": "success", "message": "正在停止..."}

@app.get("/api/logs")
async def get_logs():
    """前端轮询此接口获取最新日志"""
    return {"running": is_running, "logs": logs}