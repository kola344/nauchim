token = 'nauchim_admin'
organizers_token = 'nauchim_org'
#main_url = 'http://10.10.34.249:12345/'
main_url = ('http://127.0.0.1:5000/')
nauchim_url = 'https://naychimonline.vercel.app'

with open('regions.txt', 'r', encoding='utf-8') as f:
    regions = [i for i in f.read().split('\n')]
