# coding: utf-8
# python 版本2.7
import sys
import json
import urllib2
import base64
import requests

reload(sys)
sys.setdefaultencoding("utf-8")

def get_access_token():
	url = "https://openapi.baidu.com/oauth/2.0/token"
	body = {
	"grant_type":"client_credentials",
	"client_id" :"此处填写自己的client_id",
	"client_secret":"此处填写自己的client_secret",
	}

	r = requests.post(url,data=body,verify=True)
	respond = json.loads(r.text)
	return respond["access_token"]
def yuyinshibie_api(audio_data,token):
	speech_data = base64.b64encode(audio_data).decode("utf-8")
	speech_length = len(audio_data)
	post_data = {
	"format" : "wav",
	"rate" : 16000,
	"channel" : 1,
	"cuid" : "B8-27-EB-BA-24-14",
	"token" : token,
	"speech" : speech_data,
	"len" : speech_length
	}

	url = "http://vop.baidu.com/server_api"
	json_data = json.dumps(post_data).encode("utf-8")
	json_length = len(json_data)
	#print(json_data)


	req = urllib2.Request(url, data=json_data)
	req.add_header("Content-Type", "application/json")
	req.add_header("Content-Length", json_length)

	#print("asr start request\n")
	resp = urllib2.urlopen(req)
	#print("asr finish request\n")
	resp = resp.read()
	resp_data = json.loads(resp.decode("utf-8"))
	if resp_data["err_no"] == 0:
	   return resp_data["result"]
	else:
	    print(resp_data)
	    return None
def asr_main(filename,tok):
	try:
		f = open("fliename", "rb")
		audio_data = f.read()
		f.close()
		resp = yuyinshibie_api(audio_data,tok)
		return resp[0]
	except Exception,e:
		print "e:",e
		return "识别失败".encode("utf-8")