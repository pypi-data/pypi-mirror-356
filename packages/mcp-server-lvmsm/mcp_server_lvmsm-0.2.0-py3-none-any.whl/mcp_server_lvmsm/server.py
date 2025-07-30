# -*- coding: utf-8 -*-
import base64
import io
from PIL import Image
import requests
import execjs
import time
import json
from datetime import datetime
import ddddocr
import os
from enum import Enum
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    ErrorData,
    Tool,
    TextContent,
    INVALID_PARAMS,
    INTERNAL_ERROR,
)

class LvmsmTools(str, Enum):
    ADD_SMRW = "add_smrw"

def lmwlaqldsm_login(username, password):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    js_file_path = os.path.join(current_dir, "1_lmwlaqldsm.js")
    
    with open(js_file_path, "r", encoding="UTF-8") as file:
        js_code = file.read()

    # 执行 JavaScript 代码
    ctx = execjs.compile(js_code)
    pwd = ctx.call("encryptByAES", password)

    i = 1
    while True:
        if i > 10:
            return None
        # 获取验证码
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN',
            'Connection': 'keep-alive',
            'Cookie': 'sessionid=lcnmxjrq12gqkx6e4i3xpxtzegifbaqg',
            'Host': '10.138.188.65',
            'Referer': 'https://10.138.188.65/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows'
        }
        url = "https://10.138.188.65/interface/myauth/captcha/"
        main_url_html = requests.get(url=url, headers=headers, verify=False)
        response = main_url_html.text
        datas = json.loads(response)
        base64_str = datas.get('data').get('mg_str')['image']
        identifier = datas.get('data').get('identifier')
        # 处理base64
        image_data = base64.b64decode(base64_str)
        image = Image.open(io.BytesIO(image_data))
        ocr = ddddocr.DdddOcr(show_ad=False)
        captcha_code = ocr.classification(image)

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'zh-CN',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Cookie': 'sessionid=lcnmxjrq12gqkx6e4i3xpxtzegifbaqg',
            'Content-Length': '146',
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'https://10.138.188.65/',
            'Origin': 'https://10.138.188.65',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'Host': '10.138.188.65'
        }
        params = {"username": username, "password": pwd, "captcha_code": captcha_code, "identifier": identifier}
        url = "https://10.138.188.65/interface/myauth/login"
        main_url_html = requests.post(url=url, headers=headers, json=params, verify=False)
        response = main_url_html.text
        datas = json.loads(response)
        message = datas.get('message')
        if message == "验证码错误！":
            i = i + 1
            print("验证码错误！")
            time.sleep(1)
            continue
        token = datas.get('data')['token']
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN',
            'Connection': 'keep-alive',
            'Cookie': 'sessionid=lcnmxjrq12gqkx6e4i3xpxtzegifbaqg',
            'Host': '10.138.188.65',
            'Referer': 'https://10.138.188.65/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'token': token
        }
        return headers

class LvmsmServer:
    # 任务列表
    def add_smrw(self, ip: str, exec_timing_date: str)->str:
        headers = lmwlaqldsm_login('admin', 'khxxb2421!@')
        params = {
            "task_type":1,
            "bvs_task":"no",
            "strategy":{"policy":1,"configType":"strategy"},
            "target":"ip",
            "input_type":"input",
            "domainList":"",
            "name":"扫描【"+ip+"】",
            "exec":"immediate",
            "tpl":"36",
            "exp_verify":"no",
            "use_agent":"no",
            "login_ifuse":"yes",
            "pwdguess":"no",
            "exec_range":"",
            "scan_pri":"2",
            "port_strategy":"standard",
            "port_speed":"3",
            "port_tcp":"T",
            "port_udp":"no",
            "live":"yes",
            "live_icmp":"yes",
            "live_udp":"no",
            "hasIpv6":False,
            "live_tcp_allports":"no",
            "live_tcp":"yes",
            "live_tcp_ports":"21,22,23,25,80,443,445,139,3389,6000",
            "live_arp":"no",
            "sping_delay":"1",
            "scan_level":"3",
            "timeout_plugins":40,
            "timeout_read":5,
            "enable_unsafe_plugins":"no",
            "scan_alert":"no",
            "check_addtional":"no",
            "srv_vul_detect":"no",
            "srv_ntp_detect":"no",
            "scan_oracle":"no",
            "ifdebug":"no",
            "encoding":"GBK",
            "report_tpl_sum":1,
            "report_tpl_host":101,
            "report_ifcreate":"no",
            "send_ftp":"no",
            "report_ifsent":"no",
            "loginarray":[{"ip_range":ip,"protocol":"","port":"","os":"","ssh_auth":"","user_name":"","user_pwd":"","user_ssh_key":"","ostpls":[],"apptpls":[],"dbtpls":[],"virttpls":[],"bdstpls":[],"devtpls":[],"statustpls":"","jhosts":[],"tpltype":"","jump_ifuse":"","host_ifsave":"","protect":"","protect_level":"","oracle_ifuse":"","ora_port":"","ora_username":"","ora_userpwd":"","ora_usersid":"","weblogic_ifuse":"","weblogic_system":"","weblogic_version":"","weblogic_user":"","weblogic_path":"","web_login_wblgc_ifuse":"","web_login_wblgc_user":"","web_login_wblgc_pwd":"","web_login_wblgc_path":"","tpllist":[],"tpllistlen":0,"tpl_industry":"nsfocus:绿盟科技","web_login_url":"","web_login_cookie":""}],
            "login_check_type":"login_check_type_vul",
            "bvs_check_type":"bvs_check_type_standard",
            "ipList":ip,
            "exec_timing_date":exec_timing_date,
            "exec_everyday_time":"00:00",
            "exec_everyweek_day":"1",
            "exec_everyweek_time":"00:00",
            "exec_emonthdate_day":"1",
            "exec_emonthdate_time":"00:00",
            "exec_emonthweek_pre":"1",
            "exec_emonthweek_day":"1",
            "exec_emonthweek_time":"00:00",
            "seniorstr":"",
            "report_type_html":"html",
            "report_content_sum":"sum",
            "report_content_host":"host",
            "pwd_interval":"0",
            "pwd_num":"0",
            "pwd_threadnum":"5",
            "pwd_timeout":"5",
            "pwd_smb":"yes",
            "port_smb":"139,445",
            "pwd_type_smb":"c",
            "pwd_user_smb":"smb_user.default",
            "pwd_pass_smb":"smb_pass.default",
            "pwd_telnet":"yes",
            "port_telnet":"23",
            "pwd_type_telnet":"c",
            "pwd_user_telnet":"telnet_user.default",
            "pwd_pass_telnet":"telnet_pass.default",
            "pwd_ssh":"yes",
            "port_ssh":"22",
            "pwd_type_ssh":"c",
            "pwd_user_ssh":"ssh_user.default",
            "pwd_pass_ssh":"ssh_pass.default"
        }
        url = 'https://10.138.188.65/interface/task/system_scan/'
        main_url_html = requests.post(url=url, json=params, headers=headers, verify=False)
        response = main_url_html.text
        json_result = json.loads(response)
        code = json_result.get('code')
        message = json_result.get('message')
        if code == 200 and message.__contains__("新建成功"):
            return message
        else:
            return "任务新建失败！"

async def serve() -> None:
    server = Server("mcp-lvmsm")
    lvmsm_server = LvmsmServer()

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=LvmsmTools.ADD_SMRW.value,
                description="Initiate scanning task",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "ip": {
                            "type": "string",
                            "format": "ipv4",
                            "description": "IPv4 address to be blocked at the port level, e.g., '192.168.1.1'",
                        },
                    },
                    "required": ["ip"]
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        try:
            match name:
                case LvmsmTools.ADD_SMRW.value:
                    ip = arguments.get("ip")
                    if not ip:
                        raise ValueError("Missing required argument: ip")
                    now_time = datetime.today().strftime('%Y-%m-%d %H:%M') + ":00"
                    result = lvmsm_server.add_smrw(ip,now_time)

                case _:
                    raise ValueError(f"Unknown tool: {name}")
            return [TextContent(type="text", text=result)]

        except Exception as e:
            raise ValueError(f"Error processing mcp-server-lvmsm query: {str(e)}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)

