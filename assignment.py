import threading
import requests
import json
import numpy as np


class Request_Exceutor(object):
    def __init__(self):
        self.url = "http://surya-interview.appspot.com/message"
        self.headers = {"X-Surya-Email-Id": "asr.rathour@gmail.com"}
        self.get_resp_time = []
        self.post_resp_time = []
        self.facts_dict = {}

    def calculate_facts(self):
        # This method calculates all required facts
        self.facts_dict['tenth_percentile_get'] = np.percentile(
            self.get_resp_time, 10)
        self.facts_dict['tenth_percentile_post'] = np.percentile(
            self.post_resp_time, 10)
        self.facts_dict['fiftyth_percentile_get'] = np.percentile(
            self.get_resp_time, 50)
        self.facts_dict['fiftyth_percentile_post'] = np.percentile(
            self.post_resp_time, 50)
        self.facts_dict['ninetyth_percentile_get'] = np.percentile(
            self.get_resp_time, 90)
        self.facts_dict['ninetyth_percentile_post'] = np.percentile(
            self.post_resp_time, 90)
        self.facts_dict['ninetty_fifth_percentile_get'] = np.percentile(
            self.get_resp_time, 95)
        self.facts_dict['ninetty_fifth_percentile_post'] = np.percentile(
            self.post_resp_time, 95)
        self.facts_dict['ninetty_nineth_percentile_get'] = np.percentile(
            self.get_resp_time, 99)
        self.facts_dict['ninetty_nineth_percentile_post'] = np.percentile(
            self.post_resp_time, 99)
        self.facts_dict['mean_get_resp_time'] = np.mean(self.get_resp_time)
        self.facts_dict['mean_post_resp_time'] = np.mean(self.post_resp_time)
        self.facts_dict['std_dev_get_resp_time'] = np.std(self.get_resp_time)
        self.facts_dict['std_dev_post_resp_time'] = np.std(self.post_resp_time)
        return self.facts_dict

    def request_executer(self):
        # This method executes get and post requests
        resp = requests.get(self.url,
                            headers=self.headers)
        roundtrip_getreq = resp.elapsed.total_seconds()
        self.get_resp_time.append(roundtrip_getreq)
        resp = json.loads(resp.content)
        data = {}
        data['emailId'] = resp['emailId']
        data['uuid'] = resp['uuid']
        rsp = requests.post("http://surya-interview.appspot.com/message",
                            json=data)
        roundtrip_post = rsp.elapsed.total_seconds()
        self.post_resp_time.append(roundtrip_post)

if __name__ == '__main__':
    req_exec = Request_Exceutor()
    for i in range(100):
        print "Executing threads"
        t = threading.Thread(target=req_exec.request_executer)
        t.start()
        t.join()
    facts = req_exec.calculate_facts()
    print facts
