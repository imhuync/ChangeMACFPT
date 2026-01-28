import requests
from bs4 import BeautifulSoup

class FPTRegister:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = "http://10.22.119.252:82/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def run(self, clean_mac):
        try:
            resp = self.session.get(self.base_url, timeout=15)
            soup = BeautifulSoup(resp.text, 'html.parser')

            if "Register MAC for Students" not in resp.text:
                form = soup.find('form', id='frmMain')
                if not form: return False, "Không tìm thấy form login."
                
                action = form.get('action')
                if not action.startswith("http"):
                    action = self.base_url + action.lstrip('/')

                payload_login = {
                    '__VIEWSTATE': soup.find(id='__VIEWSTATE')['value'],
                    '__VIEWSTATEGENERATOR': soup.find(id='__VIEWSTATEGENERATOR')['value'],
                    '__EVENTVALIDATION': soup.find(id='__EVENTVALIDATION')['value'],
                    'txtUserName': self.username,
                    'txtPassWord': self.password,
                    'btnLogon.x': '50', 'btnLogon.y': '15'
                }
                
                post_login = self.session.post(action, data=payload_login)
                if "Register MAC for Students" not in post_login.text:
                    return False, "Đăng nhập thất bại."
                
                resp = post_login
                soup = BeautifulSoup(resp.text, 'html.parser')

            payload_mac = {
                '__VIEWSTATE': soup.find(id='__VIEWSTATE')['value'],
                'ctl00_ctpControlPanel_rsm_TSM': ';;System.Web.Extensions, Version=3.5.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:3a0cfa34-00a0-4a4d-a205-9a520ebde97a:ea597d4b:b25378d2;Telerik.Web.UI, Version=2013.1.220.35, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:43979e1a-2fe0-4f32-ae90-cced0bd7b824:16e4e7cd:58366029',
                'ctl00$ctpControlPanel$txtMacAddress': clean_mac,
                'ctl00$ctpControlPanel$bntExec': 'Edit'
            }
            
            gen = soup.find(id='__VIEWSTATEGENERATOR')
            if gen: payload_mac['__VIEWSTATEGENERATOR'] = gen['value']
            
            ev = soup.find(id='__EVENTVALIDATION')
            if ev: payload_mac['__EVENTVALIDATION'] = ev['value']

            final_resp = self.session.post(resp.url, data=payload_mac)
            
            if final_resp.status_code == 200:
                return True, "Đổi MAC thành công."
            return False, f"Lỗi Server: {final_resp.status_code}"

        except Exception as e:
            return False, str(e)