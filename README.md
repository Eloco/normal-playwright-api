# normal-playwright-api
a playwright ASYNC API inside docker
> upgrade to async api!

note: it can run on local docker or container like heroku
```
podman pull                       public.ecr.aws/w3s2d0z8/normal-playwright-api:master
podman pull                       ghcr.io/eloco/normal-playwright-api:latest
pdoman run --rm=True -p 8080:8080 ghcr.io/eloco/normal-playwright-api:latest
```
```
bs64=`echo "await page.goto('http://whatsmyuseragent.org/',wait_until='commit'); result=await page.content()" | base64 -w 0`
http -f POST http://127.0.0.1:8080/post  run=${bs64} browser="webkit" device="iphone 6" stealth="True" | jq .result | html2text | sed -r "s/\\\n//g"  | grep -v '^\s*$' | grep -v '^"'

What's my User Agent?
Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38
(KHTML, like Gecko) Version/16.0 Mobile/15A372 Safari/604.1
My IP Address: xx.xx.xx.xx
Copyright © What's my User Agent 2015
```

```
param = {
        run      : "result='hello Flask POST'" ; # base64 or normal run code
        browser  : "webkit"                    ; # browser name
        device   : "iPhone X"                  ; # device for webkit
        stealth  : false                       ; # if stealth mode
        reindent : true                        ; # if reindent run code
        }
```

BTW: if u need to set proxy, marksure add the code into your post['run']:
>https://playwright.dev/python/docs/network

>You can configure pages to load over the HTTP(S) proxy or SOCKSv5. Proxy can be either set globally for the entire browser, or for each browser context individually.
You can optionally specify username and password for HTTP(S) proxy, you can also specify hosts to bypass proxy for.
```
browser = await chromium.launch(proxy={
  "server": "http://myproxy.com:3128",
  "username": "usr",
  "password": "pwd"
})
```
