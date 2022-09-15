#!/usr/bin/env python
# coding=utf-8

#Import the flask module
from wrapt_timeout_decorator import *
from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
from playwright_stealth import stealth_sync
import asyncio
import base64
import os,sys
import datetime,time,random
import httpx,requests
import traceback

app = Flask(__name__)

result = 'hello world'

@app.route('/')
def hello_world():
    statement = 'Hello World!'
    return statement


"""
param = {
        run:"result='test'"; # base64 or normal diy code,             
        browser:"chromium";  # browser name,
        device:"iPhone X";   # device for webkit
        stealth:true;        # if stealth mode
        async:true;          # if async/await mode
        }
"""

@timeout(60*10) # 10 minutes
@app.route('/post', methods=['POST'])
def playwright():
    status_code = 200
    try:
        if browser_name:=request.form.get('browser', default=False):
            device_name=request.form.get('device', default='')
            with sync_playwright() as playwright:
                global result
                if  browser_name.lower() == "chromium":
                    browser = playwright.chromium.launch(headless=True)
                    context = browser.new_context()
                elif browser_name.lower() == "firefox":
                    browser = playwright.firefox.launch(headless=True)
                    context = browser.new_context()
                else:
                    browser = playwright.webkit.launch(headless=True)

                    if device_name.lower() == "random":
                       device_name = random.choice(list(playwright.devices.keys()))
                    else:
                        for d in playwright.devices.keys():
                            if device_name.lower() == d.lower():
                                device_name = d
                                break
                        if device_name not in playwright.devices.keys():
                            device_name = "Desktop Firefox"  # use default
                    print(f"webkit using [{device_name}]")
                    device      = playwright.devices[device_name]
                    context     = browser.new_context(**device,)
                context.clear_cookies()
                page = context.new_page()
                if stealth:=request.form.get('stealth', default=False):
                    print(stealth)
                    print("page is stealth!")
                    stealth_sync(page)

            run="global result;"
            if command:=request.form.get('run', default=False):
                try:
                    run+=base64.b64decode(command).decode('utf-8')
                except:
                    run+=command
            print(run)
            exec(run)
    except Exception as e:
        #result=str(e)
        result=traceback.format_exc()
        traceback.print_exc()
        status_code = 500

    try:browser.close()
    except:pass

    return jsonify({
                    'code': status_code,
                    'result': result,
                  })

if __name__ == "__main__":
    # Create the main driver function
    app.run(host    = os.getenv('IP', '0.0.0.0'), 
            port    = int(os.getenv('PORT', 9000)),
            debug   = True,
           )
