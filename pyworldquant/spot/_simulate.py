from requests.auth import HTTPBasicAuth
import time
import json
import pandas as pd

def login(self):
    """login Information (USER_DATA)

    login current user account

    Post /authentication

    Keyword Args:
        username
        password
    """

    url_path = "/authentication"
    url = self.base_url + url_path
    response = self.session.post(url,timeout= self.timeout ,auth=HTTPBasicAuth(self.username, self.password))
    print(111111)
    if response.status_code == 201:
        print('{} login success'.format(self.username))
    else:
        print('{} login fail'.format(self.username))

    return

def simulate(self,regular,setting):
    """Simulate Information ()

    simulate

    Post /authentication

    Keyword Args:
        regular
        settings
    """
    payload = self.simulate1(regular,setting)
    a = self.simulate2(payload)
    b = self.brief_performance(a)
    return b


def simulate1(self,regular,setting):
    url_path = "/simulations"
    url = self.base_url + url_path
    payload = {"type": "REGULAR", "settings": setting['settings'], "regular": regular}
    while True:
        try:
            response = self.session.post(url, data=json.dumps(payload),timeout= self.timeout)
        except Exception as e:
            print('Fetch alphaid failed！,{}'.format(e))
            time.sleep(10)
            payload['alphaid1'] = ''
            return payload

        if response.status_code != 201:
            print('Fetch alphaid failed！,REASON IS {}'.format(json.loads(response.content)))
            return
        else:
            try:
                alphaid = response.headers['Location'][44:]
                print('用户【{}】获取alphaid:【{}】成功！ '.format(self.username, alphaid))
                payload['alphaid1'] = alphaid
                return payload
            except:
                continue

def simulate2(self,payload):
    if payload is None:
        return
    url_path = "/simulations/{}".format(payload['alphaid1'])
    url = self.base_url + url_path
    fetchdata = False
    fetchtime = 0
    while fetchdata == False:
        fetchtime += 1
        try:
            response = self.session.get(url, timeout= self.timeout)
            if len(response.content) > 30:
                if 'MSIE' not in str(response.content):
                    fetchdata = True
                else:
                    print('Request Failed! Server Error')
        except:
            return
        time.sleep(5)
    content2 = json.loads(response.content)
    try:
        if content2['status'] == "FAIL" or content2['status'] == "ERROR":
            print('fetch alphaid2 failed！ Reason is {},{}'.format(content2['status'],content2['message']))
            return
        else:
            alphaid2 = content2['alpha']
            return alphaid2
    except Exception as e:
        print('Fetch alphaid2:【{}】Fail！,Reason is {}'.format(e))

def brief_performance(self,alphaid2):
    url_path = "/alphas/{}".format(alphaid2)
    url = self.base_url + url_path
    try:
        simu_response = self.session.get(url, timeout= self.timeout)
        ischeck = json.loads(simu_response.content)['is']['checks']
        ischeckresult = solve_is_check(ischeck)
        return ischeckresult
    except Exception as e:
        print('Fetch performance Fail！,Reason is {}'.format(e))

def solve_is_check(x):
    x1 = pd.DataFrame(x)[['name', 'value']].set_index('name')['value'].dropna()
    return x1




