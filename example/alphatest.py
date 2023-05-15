import csv
import json
import time
import threading
import queue

import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import datetime
import random

from config import username,key,settingslist

class WorldQuantBrain:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_url = "https://api.worldquantbrain.com/authentication"
        self.job_sim_url = "https://api.worldquantbrain.com/simulations"
        self.sim_url = "https://api.worldquantbrain.com/simulations/{}"
        self.self_correlation_check_url = 'https://api.worldquantbrain.com/alphas/{}/correlations/self'
        self.prod_correlation_check_url = 'https://api.worldquantbrain.com/alphas/{}/correlations/prod'
        self.check_url = 'https://api.worldquantbrain.com/alphas/{}/check'
        self.myalpha_url = "https://api.worldquantbrain.com/users/self/alphas"
        self.alpha_url = "https://api.worldquantbrain.com/alphas/{}"
        self.year_url = "https://api.worldquantbrain.com/alphas/{}/recordsets/yearly-stats"
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
            ]
        self.headers = {
            'content-type': 'application/json',
            'User-Agent': random.choice(self.user_agent_list),
            'referer': 'https://platform.worldquantbrain.com/'
        }

        self.session = requests.session()
        self.login()

#login
    def login(self):
        response = self.session.post(
            self.login_url, headers=self.headers,
            auth=HTTPBasicAuth(self.username, self.password)
        )
        time.sleep(1)
        if response.status_code == 201:
            print('{} 登陆成功'.format(self.username))
        else:
            print('{} 登陆失败'.format(self.username))

#simulate

    def simulate(self, settings, regular):
        global writer
        payload = {"type": "REGULAR", "settings": settings['settings'], "regular": regular}

        alphaid = ''
        while True:
            try:
                job_response = self.session.post(self.job_sim_url, data=json.dumps(payload), headers=self.headers,timeout=(5,20))
            except Exception as e:
                print('用户【{}】获取alphaid失败！,原因为{}'.format(self.username,e))
                time.sleep(10)
                return
            try:
                alphaid = job_response.headers['Location'][44:]
                print('用户【{}】获取alphaid:【{}】成功！ '.format(self.username, alphaid))
                time.sleep(60)
                break
            except:
                continue
        fetchdata = False
        alphaurl = self.sim_url.format(alphaid)
        fetchtime = 0
        while fetchdata == False:
            fetchtime += 1
            t3 = time.time()
            try:
                response = self.session.get(alphaurl, headers=self.headers,timeout=(5,10))
                if len(response.content) > 30:
                    if 'MSIE' not in str(response.content):
                        fetchdata = True
                    else:
                        print('请求失败出现服务器错误')
            except:
                return
            time.sleep(5)
        content2 = json.loads(response.content)
        try:
            if content2['status'] == "FAIL" or content2['status'] == "ERROR":
                print('用户【{}】获取alphaid2失败！,原因为{},参数为{},{}'.format(self.username,content2['status'],settings['name'],regular))
                return
            else:
                alphaid2 = content2['alpha']
                print('用户【{}】获取alphaid2:【{}】成功！ 获取次数为{}次'.format(self.username, alphaid2,fetchtime))
                isresult = self.get_alpha_simulation(alphaid2)
                isresult['settings'] = settings['name']
                isresult['REGULAR'] = regular
                yearly_sharpe = self.get_yearly_sharpe(alphaid2)
                isresult['2015'] = yearly_sharpe[0]
                isresult['2016'] = yearly_sharpe[1]                
                isresult['2017'] = yearly_sharpe[2]
                isresult['2018'] = yearly_sharpe[3]
                isresult['2019'] = yearly_sharpe[4]
                isresult['2020'] = yearly_sharpe[5]              
                print(isresult)
                print(yearly_sharpe)
                writer.writerow(isresult.values.tolist())
                print('-' * 50)
        except Exception as e:
            print('----------------------------------------------------------------')
            print('获取alphaid2:【{}】失败！,原因为{},参数为{}，{}'.format(regular,e,settings['name'],regular))
            print('----------------------------------------------------------------')


    def get_alpha_simulation(self, alpha_id):
        simu_response = self.session.get(self.alpha_url.format(alpha_id), headers=self.headers,timeout=(5,15))
        ischeck = json.loads(simu_response.content)['is']['checks']
        ischeckresult = self.solve_is_check(ischeck)
        return ischeckresult
    
    def get_yearly_sharpe(self,alpha_id):
        time.sleep(5)
        fetchdata = False
        while fetchdata == False:
            response = self.session.get(self.year_url.format(alpha_id), headers=self.headers,timeout=(5,10))
            if len(response.content) > 30:
                if 'MSIE' not in str(response.content):
                    fetchdata = True
                else:
                    print('延迟请求')
                    time.sleep(5)
        print(response.content)
        yearly_sharpe = [i[6] for i in json.loads(response.content)['records']]
        print('0000000000000000')
        return yearly_sharpe    


    @staticmethod
    def solve_is_check(x):
        x1 = pd.DataFrame(x)[['name', 'value']].set_index('name')['value'].dropna()
        return x1
    
        
#multiprocess 
    def main(self, tasks, t_id):
        while True:
            if tasks.empty():
                print('队列为空----线程：{}__{} 停止！'.format(self.username, t_id))
                break
            else:
                info = tasks.get()
                self.simulate(settings=info[0], regular=info[1])
                print('用户{} 正在爬取-------队列还剩：{} 个！'.format(self.username, tasks.qsize()))
                
#export 
def create_file():
    global writer
    curr_time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S').replace(' ','').replace('-','').replace(':','')
    filename = time_str+'.csv'
    writer = csv.writer(open(filename, 'a', encoding='utf8', newline=''))
    writer.writerow(['LOW_SHARPE', 'LOW_FITNESS', 'LOW_TURNOVER', 'HIGH_TURNOVER', 'LOW_SUB_UNIVERSE_SHARPE', 'settings','REGULAR','2015','2016','2017','2018','2019','2020'])

#main
def main():
    start_time = time.time()
    create_file()   
    tasks = get_alphalist()
    user = WorldQuantBrain(username, key)
    t_lst = []
    for i in range(3):
        t = threading.Thread(target=user.main, args=(tasks, i))
        t_lst.append(t)
        time.sleep(5)
        t.start()

    for t in t_lst:
        t.join()
    print('采集耗时：{}'.format(time.time() - start_time))

def get_alphalist():
    q = queue.Queue()
    df = pd.read_csv('alpha_generator/alphapool.csv')
    factorset = df.iloc[:,1].tolist()
    for j in factorset:                         
        for i in settingslist:
            q.put([i,j])            
    return q

if __name__ == '__main__':
    main()



