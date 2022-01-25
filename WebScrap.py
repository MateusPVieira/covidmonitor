import requests
from bs4 import BeautifulSoup
import re
from datetime import date


def request_page_day(teste):
    status = 0
    link = titulostr = ultimoboletim = ''
    data_atual = date.today()
    data_atual = data_atual.strftime('%d-%m-%Y')
 

    if type(teste) == type(None):
        status = 1
    else:

        if teste.databoletim == data_atual:
            ultimoboletim = teste.databoletim
    page = requests.get('http://coronavirus.saocarlos.sp.gov.br/page/1')
    soup = BeautifulSoup(page.content, 'html.parser')

    if ultimoboletim != data_atual:

        titulo = soup.find_all(attrs={'class': "news-thumb col-md-6"})
        for i in range(len(titulo)):
            if "BOLETIM" in (str(titulo[i])).upper():
                if data_atual in str(titulo[i]):
                    link = re.findall(r'href\s?=\s?[\'"]?([^\'" >]+)', str(titulo[i]))
                    link = link[0]
                    titulostr = str(re.findall(r'title\s?=\s?[\'"]?([^\'" >]+)', str(titulo[i])))
                    titulostr = titulostr[1]
                    status = 1
                    break

    info = {'dia': data_atual, 'titulo': titulostr, 'link': link, 'status': status}
    return info


def get_image(link):
    page = requests.get(link)
    imagefont = BeautifulSoup(page.content, 'html.parser')
    tag = imagefont('div', class_='news-thumb')
    link = str(tag[0])
    link = re.findall(r'src\s?=\s?[\'"]?([^\'" >]+)', link)
    link = link[0]
    r = requests.get(link, stream=True)
    if r.status_code == 200:
        with open("static\img\oletim.png", 'wb') as f:
            for chunk in r:
                f.write(chunk)


def get_news(link):
    news = []
    dates = []
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    allnews = soup.find_all(attrs={'class': "tileHeadline"})
    predates = soup.find_all('li')
    for li in range(len(predates)):
        if "/22" in str(predates[li]):
            dates.append(predates[li].text)
    for num in range(len(allnews)):
        link = str(allnews[num])
        link = re.findall(r'href\s?=\s?[\'"]?([^\'" >]+)', link)
        link = 'https://portais.ifsp.edu.br' + link[0]
        news.append({'titulo': allnews[num].text.strip('\n'), 'data': dates[num], 'link': link})
    return news



