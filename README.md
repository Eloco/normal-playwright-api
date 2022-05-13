# normal-playwright-api
a playwright API inside docker

note: it can run on local docker or container like heroku
```
sudo docker pull public.ecr.aws/w3s2d0z8/normal-playwright-api:master
sudo docker pull ghcr.io/eloco/normal-playwright-api:latest
sudo docker run --rm=True -p 8080:8080 ghcr.io/eloco/local-lambda-playwright
```
```
bs64=`echo "page.goto('http://whatsmyuseragent.org/',wait_until='commit'); result=page.content()" | base64 -w 0`
http -f POST http://127.0.0.1:8080/post  run=${bs64} browser="webkit" device="iphone 6" stealth="True" | jq .result | html2text -utf8 | sed -r "s/\\\n//g"  | grep -v '^\s*$' | grep -v '^"'

What's my User Agent?
Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38
(KHTML, like Gecko) Version/15.4 Mobile/15A372 Safari/604.1
My IP Address: xx.xx.xx.xx
Copyright © What's my User Agent 2015
```

```
param = {
        run:"result='test'"; # base64 or normal diy code,
        browser:"chromium";  # browser name,
        device:"iPhone X";   # device for webkit
        stealth:true;        # if stealth mode
        }
```
