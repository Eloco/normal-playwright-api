#!/usr/bin/env python
# coding=utf-8

#Import the flask module
from flask import Flask, request, jsonify
from wrapt_timeout_decorator import *
import asyncio
import base64
import os,sys,json
import traceback
import tempfile
import copy

app = Flask(__name__)

@app.route('/')
async def hello_world():
    statement = 'Hello Flask GET!'
    return statement

"""
param = {
        run      : "result='hello Flask POST'" ; # base64 or normal run code
        browser  : "webkit"                    ; # browser name
        device   : "iPhone X"                  ; # device for webkit
        stealth  : false                       ; # if stealth mode
        reindent : true                        ; # if reindent run code
        }
"""


@timeout(60*10) # 10 minutes
@app.route('/post', methods=['POST'])
async def playwright():
    try:
        status_code = 200
        result="Hello Flask POST!"

        if_stealth   = bool(request.form.get('stealth'  , default  = False))
        if_reindent  = bool(request.form.get('reindent' , default  = True))
        browser_name = str(request.form.get('browser'   , default  = 'webkit')).strip().lower()
        device_name  = str(request.form.get('device'    , default  = '')).strip().lower()

        run_code     = str(request.form.get('run', default =f'result="{result}"')).strip()

        template_file="async_template.py"

        try:
            run_code=base64.b64decode(run_code).decode('utf-8')
        except:pass
        run_code     = run_code.replace('\r','\n').replace('\n','\n'+" "*4*2)

        with tempfile.TemporaryDirectory() as tmpdirname:
            #print('created temporary directory', tmpdirname)
            os.chdir(sys.path[0])
            template=open(template_file).read()
            template=template.replace('<run_code>',run_code)
            sys.path = list(filter(lambda x:os.path.exists(x) and \
                    "/var/folders/" not in x[:13],sys.path)) ##clean sys.path
            sys.path.insert(1, tmpdirname)
            file_path=os.path.join(tmpdirname,"template.py")
            with open(file_path,"w") as f:f.write(template)
            if if_reindent:os.system(f"reindent {file_path} &> /dev/null;autopep8 {file_path} --select=E121,E101,E11 --in-place &> /dev/null;cat {file_path}")
            import template
            result=await template.main(browser_name=browser_name,if_stealth=if_stealth,device_name=device_name)

    except Exception as e:
        #result=str(e)
        result=traceback.format_exc()
        traceback.print_exc()
        status_code = 500

    return jsonify({
                    'code'   : status_code ,
                    'result' : result      ,
                  })

if __name__ == "__main__":
    # Create the main driver function
    app.run(host    = os.getenv('IP', '0.0.0.0'), 
            port    = int(os.getenv('PORT', 9000)),
            debug   = True,
           )
