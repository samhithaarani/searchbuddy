from django.shortcuts import render
from .import models
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from django.http import HttpResponseRedirect

BASE_URL="https://losangeles.craigslist.org/search/bbb?query={}"
BASE_IMAGE_URL="https://images.craigslist.org/{}_300x300.jpg"

def home(request):
    return render(request,"base.html")
def search(request):
    content=request.POST.get('content')
    models.search.objects.create(search=content)
    final_url=BASE_URL.format(quote_plus(content))
    response=requests.get(final_url)
    data=response.text
    soup=BeautifulSoup(data,features="html.parser")
    #returns all content in list of all posts 
    post_listing=soup.find_all('li',{'class':'result-row'})
    #getting title,url,price
    """post_title=post_listing[0].find(class_='result-title').text
    post_url=post_listing[0].find('a').get('href')
    post_price=post_listing[0].find(class_="result-price").text"""

    final_posting=[]
    for post in post_listing:
          post_title=post.find(class_='result-title').text
          post_url=post.find('a').get('href')
          if post.find(class_="result-price"):
              post_price=post.find(class_="result-price").text
          else:
              post_price="N/A"
          if post.find(class_="result-image").get('data-ids'):
               post_image_id=post.find(class_="result-image").get('data-ids').split(",")[0].split(':')[1]
               post_image_url=BASE_IMAGE_URL.format(post_image_id)
          else:
              post_image_url="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAY1BMVEUeHh7z8/X8/P4AAAASERH29vjr6+wICAh5enmZmZkbGxvk5OUNDQ3///9vb24WFhbQ0dOAgIDZ2tzExce9vsGJiYk+Pj2Pj4+vsLRKSkonJyezs7OoqKhVVVQxMTFnZ2ddXV2P0fWVAAAJpElEQVR4nO2dfZ+iIBDHkxErjTS12p73/b/KA6vbBS0GTJT98Ptnr7tb8usMz8MwW8SzP65A6L8Cof8KhP4rEPqvQOi/AqH/CoT+KxD6r0DovwKh/wqE/isQ+q9A6L8Cof8KhP4rEPqvQOi/AqH/CoT9lab5K6VpOvS3D0yYzwFgdt291HXF/8NqWMzhCHOAw77OIvZOJClPiyPMB4QcijCGwylhhNJII0oJK/c5DMY4DGEO64Jp4X4oCa2vQzEOQgiX0oDvDslO8WqARxmEMIeTKZ8QidagFpXGq4diawt/nhB2CTHnE2K17KkpHNebh9ZHWy/+OCGsiYUBH2bM0vynpHRek1+qLRE/TQgbJj00Je8lvw0aHX8QISMyfsuJUfowYQsw2262b7Q5yx5Nk/+Iq61cVET2c5tH+izh/KY8VcKHLG8Fa+WVJE9nhFrxdlpZGfGjhPlVaWPoWftQoNRFWjx+BSqVsBifEDL1oRCEiYLIlvffmaIN4ax2EzaEEds1VXGC9TDftfpBK0JaPow4ubYUilZHqHesdNUeHrB1M35LoSbs2auwCfSH+YG1njUiC9BIbU/Ee3laC463xUO3o50FLQnTGPms3B5J9lad0yt26yh+nusf7DOEKUB8W9ZFlih6MVijb9X9O5Fadlmc9gfetzogzOG6LImY2lqPPi0k3gVhUcV93rgymhHm8F0w+5F1b1BCz8YzZRPC1GJm+2kRcorN2hwDwnhVj83XMNKNkRnxhHCJLGe2nxYrwKBdRRPCvqO7G0k02uEHcFhCOE0HUDQ53+jKiCSE00Q89CmGRsQRwnlKFmxEDkjvQxHCYnKAvC4it3UwhB3TogkIO+XHELam7tMQ2aMQEYSw/4QJxfj5/4xCfOhfJJth/FRPmEJvQMFWPsDuoGVZio/9isUt3OgJ26svhniN0SJpLiJmJg1lP0h2QIxttIRp3qcSCoNxus5/ozTJCg5pXzqtEUbUEq629iYU5nuB93xGPrftYUhMTdQSQmlrwzfm+yUaCUbLr8AsMOoI051tZ59kr9Y1FPVgfC489iGcW3YV3IAGD5oUpZ2rEr2b6gi7V9C0SjT1TxXN7MzIbtq+QEto873cgKbvpTGj+TcR/aK6hjCdWTgpugZKojY9B2JwqiHsXMjWyNRD/z+tRYND9ZsZGsJY3fLUKzFoYtTHtUDsS7hamHqpPaAVIulNuDEkfA1IyXMniakBCj//xxjROeELQEpYUi9vu1xssRwvi3NBupdejeuic8JOQMqy806wrZqo0liEXMK6ol1F06IwcnPXhF3dBGXFt4BLJXFrrpZdS8zUrF90TJh0dPSsPAA0eFLBd8h91w5WZYLolrADkNIFzF9EOwvGuGr1RmatjVvCdgUixRzeRHMLxnXLjLwqTpSwbUJ2burfm/LTFK6tX6MGfuqSsN1RsC2852sYV1CqkVQZvj11SdiqPGyBABQLQVCoiHgjOiRs+SjboAAbRGWlhGYV1ogOCVUT8pkbDrBBVGYjBG1Ed4SqCWmJBhTRwOokDV0TXRLKn2m+Mjjyk6o7B7RGGtEdoQLYtDJoQIEo+wB6eOqMUHHSxkcNAPlUW/XTGjewcUaoPA67zA2PpaXKoh5Buqk7QukTLUxNKLZhJSOKieKUCBUnZd9gfLIwVcJTkwrlpu4If3+iibkJ+VfJi17I1tQVofy6ydLchMKIUpG0Qs0wnBFKn9jB6lioHJyP7C8cESbKuNLGSfl3rX9/F3Js6opQamhoZeOkvDWVdxASVI84CqGohhaAvCJKRLimxhnh70+ir7AhVI4zTIpQdid2tTx/DifJFWpMYzoKIcmtGhpOuJSaGlR3MQqhZVPKCbeB8M8RIjpEzwj3ntiQHS0Pz8sRdNNqS+X+0G5Yqg5MJ0xIFrY9vjS8pV8T6vGVcenZdtQmlzopQvnlF3aEyjpGMqVRmzJ7InaNqdKUllOaW0Ty2yZrKyMqA+9iSvNDpamhVoeSlQAz3pROi1B207mFm6oL+6iGxt1am1IR9+ZG5PNfqYxsWmttifI0FsuJczkFCK2mtV7aclNjI6pbM+RrWmverdU2ampEtRYindQlofw8pjkelHU23hzjnNTl/qFiRGbWJ7ZyaiCd1OUecKH8BTWZQ8krNKK7n94ecKIakWb4qghqJDLFmtBptEnLiOh9YLio8TRoE7qNp1GPDxHkPmkLEF8LHUd9tabkpMTkJlWzfYlomknGRIkYmFYIXrLTbdLksFQBaYY3oePYxLIdZcgHN++a1BRmRTvA9MsgwNRxBG3H0hEpd69r4xy27SBhUqGbGfeEbT8VYd71tbM6pgDrrF26kY+6j/MuOxA5Y/Wt5EMWMd7pPuk6dpGY+Kj7WP2k7DxxSllyWuf3fFbz5sduX3QfK6FfRoHsI5y3KF6cyxNnSorzcrvZ7Jengr5KxWQKOMaZmVeIzRH1R87Sl0fbaF2XZuemxjj39BpRK3PAEQgFou3pbw7owdm1BrGrRdWKJrwOGh/tG4OwQTQ/Rcr7wcrimOwohGLCXxlWRkqrL7ujzuMQ3j3VgJEb0LwKNupPaHxK9i6OiDcjjYQB7dIq9CaMW5M3rPgIDsdIo+Krsk6N0Zswv1jnwOKT/qrKdGkkBV9tn8OFJr0zDlx7ZPnijGLB5WWF5IOcrOb265GjBpH6Q5s1wva7GzWMlYBszY0poVn1VffiQ+Xg0RJap6d5MgrIWnR1vzPP8lpaP/B65VEiW21aWi3huW8msyYNVlFUtVDFVd//VHwiGdYj93cfQou0EV2Q9/xexVPlI/NX/5L7Z+CZwaey0T1TmT1+fqRMevoE4elTiAOIXfTpzLSENvlbXAmRuwWVka5nazqg2AaR4FtP2GNYM7AQAxoUYdeNANPQ44aB/oSpevPIRIRMYIrKXzqhNNC/RK+o7Ulcll01JcAUxNa4jNcoQjVeaQpCZGozIJzlR7sEZcOJYBJ7GhDO4uu0EPGA6Jzs8dH2vrghxBDjUVPCWQ7tdEAjibKNwQUQ+LsRUtiOd3fHb5HsYHLDhckNHnCsxr/ggtClyd0PhrewpHAp2JjVUVzDkhtei2R4k04Ou3Myzk0zzaWz27lx9LHxbUg5wGVZ8NrOui5sHEr8pWb11uriYJsbrcSO/PFwW7vT7XsX217+bHsrWZrHLmV78LYHoT8KhP4rEPqvQOi/AqH/CoT+KxD6r0DovwKh/wqE/isQ+q9A6L8Cof8KhP4rEPqvQOi/AqH/CoT+KxD6r0DovwKh/wqE/uvvE65h/rc1q5d/XP8AlAXMLS67L98AAAAASUVORK5CYII="

          final_posting.append((post_title,post_url,post_price,post_image_url,))
          #stuff for frontend
          stuff_for_frontend={"search":content,"final_posting":final_posting,}
            
    return render(request,"search.html",stuff_for_frontend)


# Create your views here.
