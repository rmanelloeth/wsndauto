


from seleniumwire import webdriver
import time
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from imap_tools import MailBox
from bs4 import BeautifulSoup
from imap_tools import AND
from random import randint, choice, sample
from colorama import init, Fore
from fp.fp import FreeProxy


init(autoreset=True)
import os



# from mailpass import email_login, email_pass




action_path = ['//*[@id="activity-id-147853"]'
     ,'//*[@id="activity-id-133141"]','//*[@id="activity-id-129557"]'
     ,'//*[@id="activity-id-130408"]','//*[@id="activity-id-129562"]','//*[@id="activity-id-133253"]'
     ,'//*[@id="activity-id-130424"]','//*[@id="activity-id-139372"]','//*[@id="activity-id-146308"]']
# '//*[@id="activity-id-146308"]/div[2]/a','//*[@id="activity-id-146309"]/div[2]/div' '//*[@id="activity-id-148267"]/div[2]/a',
#split authdata from file
def authdataread(i):
     authdata = line[i].split(':')
     return authdata[0], authdata[1], authdata[2], authdata[3].replace('\n', '')
def random_actions():
     n = randint(1,9)
     f = 0
     # n = 9
     updated_activities = action_path
     # updated_activities = action_path
     # print(action_path)
     # print(updated_activities)
     if n > 0:
          for i in range(0, n):
               try:
                    action = driver.find_element(By.XPATH, updated_activities[i])
                    action.click()
                    time.sleep(2)
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(1)
                    driver.close()
                    time.sleep(1)
                    driver.switch_to.window(driver.window_handles[0])
                    f = f + 1
               except Exception as ex:
                    print(i, Fore.RED + '  action error')


          else:
               print(f, '   actions made')



          # action =

def choose_proxy_from_file():
     authdata = choice(line)
     authdata = authdata.split(':')
     return authdata[0], authdata[1], authdata[2], authdata[3].replace('\n', '')
#function mail:pass split
def authmailpass(b):
     authdata = linemail[b].split(':')
     return authdata[0], authdata[1].replace('\n', '')
def get_random_proxy_free():
    proxy = FreeProxy(timeout=0.8, rand=True, elite= True).get()
    #print(proxy)
    return proxy
# imapchoice = input ('choose imap server from: outlook or firstmail  ')
# if imapchoice == 'outlook' or imapchoice == 'ol':
#      imap_server = 'outlook.office365.com'
# elif imapchoice == 'firstmail' or imapchoice == 'fm':
#      imap_server = 'imap.firstmail.ltd'
imap_server = 'outlook.office365.com'
# imap_server = 'imap.firstmail.ltd'
#options

#initialise Useragent, webdriver
useragent = UserAgent()
options = webdriver.ChromeOptions()
#selenium options
#web driver detection off
options.add_argument('--disable-blink-features=AutomationControlled')
#headless mode
options.add_argument('--headless')


#variables
timeout = 10
accounts = 0
i = 0
proxy_default = ''
proxylogged = None
#REFFERAL URL
url = 'https://wesendit.io/waitlist/?kid=2KFWTY'
# url = 'https://2ip.ru/'
proxy_usage = input('choose proxy option: 0 - without proxy, 1 - random free proxy, 2 - proxies from file proxy.txt  ')
number_of_accounts = input ('Number of accounts to be registered?    ')
#splitting line into login:pass:ip:port
with open('proxy.txt') as file1:
     line = file1.readlines()
#splitting mail auth data mail:pass
with open('email.txt') as file2:
     linemail = file2.readlines()
n = len(line)

while i < (int(number_of_accounts)):
     print('current i number is  ', Fore.RED + str(i))
     proxy_options = {}
     email_login, email_pass = authmailpass(i)
     print('Startin account... ', email_login)
     #useragent
     options.add_argument(f'user-agent={useragent.random}')

     #working
     print('Trying to get web page...')
     # while proxylogged == None:
     if int(proxy_usage) == 0:
          proxy_options = {}
          print('no proxy')
          proxy = ''
     elif int(proxy_usage) == 1:
          proxy = get_random_proxy_free()
          proxy_options = {
               'proxy': {
                    'https': proxy
               }
          }
          print('proxy random ', proxy)
     elif int(proxy_usage) == 2:
          ip, port, login, passwd = authdataread(i)
          # ip, port, login, passwd = authdata[]
          print('proxy from file ', ip,':',port)
          proxy = 'https://' + login + ':' + passwd + '@' + ip + ':' + port
          proxy_options = {'proxy': {'https': f'https://{login}:{passwd}@{ip}:{port}'}}

     # proxy_options = {'proxy': {'https': 'https://user96287:lb6ru0@5.180.50.173:9828'}}
     driver = webdriver.Chrome(
          executable_path='C:\\Users\\topar\\PycharmProjects\\pythonProject\\Wesend autoreger\\chromedriver\\chromedriver.exe'
          , options=options, seleniumwire_options=proxy_options)

     try:
          driver.get(url=url)
          print(driver.get_issue_message())
          print('Registering with mail...')
          email_input = driver.find_element(By.ID, 'email')
          email_input.clear()
          email_input.send_keys(f'{email_login}')
          time.sleep(1)
          accept_cookie = driver.find_element(By.ID, 'cn-accept-cookie')
          time.sleep(1)
          accept_cookie.click()
          button = driver.find_element(By.CLASS_NAME, 'waitlist-button')
          button.click()
          time.sleep(5)
          proxylogged = True
          time.sleep(5)

     except Exception as ex:
          print(Fore.RED + 'proxy error: ')
          with open('usedproxy.txt', 'a') as f:
               f.write(proxy + '\n')
          with open('usedmails.txt', 'a') as dd:
               dd.write(email_login + '\n')
          proxylogged = None


     bodies = []
     verif = []
     if proxylogged==True:
          os.environ["HTTPS_PROXY"] = proxy
          attempts = 1
          while attempts < 4:
               print('Checking message...')
               try:
                    with MailBox(imap_server).login(email_login, email_pass) as mailbox:
                         # bodies1 = [msg.html for msg in mailbox.fetch(AND(subject = 'IMPORTANT'), reverse=True)]
                         for msg in mailbox.fetch(AND(subject='IMPORTANT')):
                              bodies.append(msg.html)

               except Exception as ex:
                    print(email_login, Fore.RED + ' error_due_logging')
                    with open('usedproxy.txt', 'a') as f:
                         f.write(proxy + '\n')
                    with open('usedmails.txt', 'a') as dd:
                         dd.write(email_login + '\n')
                    break
               time.sleep(7)
               if bool(bodies):
                    print('Link fetching...')
                    soup = BeautifulSoup(str(bodies), 'html.parser')
                    links = []
                    # rx = re.compile("^https://")
                    for link in soup.find_all('a'):
                         links.append(link.get('href'))
                    url1 = links[1].replace("\\'", '')
                    os.environ["HTTPS_PROXY"] = proxy_default
                    try:
                         driver.get(url=url1)
                         time.sleep(5)
                         print(Fore.GREEN + 'link loaded...')
                         accounts = accounts + 1
                    except Exception as ex:
                         print(Fore.RED + 'page not loaded')
                    # except Exception as didntclick:
                    #      print(Fore.RED + 'didnt get verification page')
                    time.sleep(7)
                    random_actions()
                    os.environ["HTTPS_PROXY"] = proxy
                    try:

                         with MailBox(imap_server).login(email_login, email_pass) as mailbox:
                              # bodies1 = [msg.html for msg in mailbox.fetch(AND(subject = 'IMPORTANT'), reverse=True)]
                              for msg in mailbox.fetch(AND(subject='Thank you for signing up!')):
                                   verif.append(msg.html)
                    finally:
                         if bool(verif):
                              print(Fore.GREEN + 'verified')
                         else:
                              print(Fore.RED + 'not verified')
                    print(url1)
                    print('registered num: ', accounts ,'', email_login, Fore.GREEN + "successful")
                    print(Fore.BLUE + '=============================================================')
                    with open('usedproxy.txt', 'a') as f:
                         f.write(proxy + '\n')
                    with open('usedmails.txt', 'a') as dd:
                         dd.write(email_login + '\n')
                    break
               else:
                    print('attempt ', attempts, Fore.RED + 'failed', 'trying again')
                    attempts = attempts + 1
                    time.sleep(5)
          else:
               print(email_login,Fore.RED +  'no message')
               print(Fore.BLUE + '==================================================================')
               with open('usedproxy.txt', 'a') as f:
                    f.write(proxy + '\n')
               with open('usedmails.txt', 'a') as dd:
                    dd.write(email_login + '\n')
     i = i + 1
     proxylogged = None
# time.sleep(randint(10, 20))
     time.sleep(randint(60, 1000))
     # time.sleep(7)


else:
     driver.close()
     driver.quit()
     print(Fore.GREEN + 'successfully registered ', accounts, Fore.GREEN + 'accounts')

# username = 'login'
# password = 'passwd'
# ip = 'ip'
# port = 'port'

 #proxy_options = f'{login}:{passwd}@{ip}:{port}'


#print(proxy)
#options.add_argument = (f'user-agent = {useragent.random}')



