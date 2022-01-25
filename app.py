from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import ProcessamentoImagem, Process, WebScrap


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.sqlite3'
db = SQLAlchemy(app)

class Dados(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  databoletim = db.Column(db.String(50))
  totcasos = db.Column(db.String(50))
  novoscasos = db.Column(db.String(150))
  novoscasosmedia = db.Column(db.String(50))
  uti = db.Column(db.String(150))

  def __init__(self, databoletim, totcasos, novoscasos, novoscasosmedia, uti):
    self.databoletim = databoletim
    self.totcasos = totcasos
    self.novoscasos = novoscasos
    self.novoscasosmedia = novoscasosmedia
    self.uti = uti


class News(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  titulo = db.Column(db.String(250))
  link = db.Column(db.String(250))
  data = db.Column(db.String(50))

  def __init__(self, titulo, link, data):
    self.titulo = titulo
    self.link = link
    self.data = data
    

class Graph(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  datagraph = db.Column(db.String(50))
  newcases = db.Column(db.Integer)
  newcasesmedia = db.Column(db.Integer)
  uti = db.Column(db.Integer)

  def __init__(self, datagraph, newcases, newcasesmedia, uti):
    self.datagraph = datagraph
    self.newcases = newcases
    self.newcasesmedia = newcasesmedia
    self.uti = uti

    
@app.route('/')

def index():
  news = db.session.query(News).order_by(News.id.desc()).limit(5)
  dados = db.session.query(Dados).order_by(Dados.id.desc()).first()
  graph = db.session.query(Graph).order_by(Graph.id.desc()).limit(10)
  graphdata = Process.get_graph_data(graph)

  return render_template('index.html', dados=dados, news=news, graphdata=graphdata)
  

@app.route('/att')
def att():  
    data_atual = datetime.now()
    data_atual = data_atual.strftime('%a')
    newstest = db.session.query(News).order_by(News.id.desc()).first()
    newsdata = WebScrap.get_news('https://portais.ifsp.edu.br/scl/index.php/ultimas-noticias.html')
    dbnewsap = []
    for element in range(len(newsdata)):
      if newsdata[element]['titulo'] in newstest.titulo:
        break
      else:
        dbnews = News(newsdata[element]['titulo'], newsdata[element]['link'], newsdata[element]['data'])
        dbnewsap.append(dbnews)
    db.session.add_all(dbnewsap)   
    db.session.commit()

    if data_atual.upper() not in "SATSUN":
      teste = db.session.query(Dados).order_by(Dados.id.desc()).first()
      info = WebScrap.request_page_day(teste)
      if info['status'] == 1:          
          cases = db.session.query(Dados)
          WebScrap.get_image(info['link'])
          ProcessamentoImagem.process_image_data()
          comparativeData = ProcessamentoImagem.load_data()
          comparativeData['data'] = info['dia']
          get = Process.get_newcases(cases, comparativeData)
          dados = Dados(comparativeData['data'],comparativeData['confirmados'], get['novoscasos'], get['novoscasosmedia'], comparativeData['UTI'])
          graph = Graph(comparativeData['data'], get['novoscasos'], get['novoscasosmedia'], comparativeData['UTI'])
          db.session.add(dados)
          db.session.add(graph)
          db.session.commit()
          return redirect(url_for('index'))
      
      else:
        return redirect(url_for('index'))

    else:
      return redirect(url_for('index'))


if __name__ == '__main__':
  db.create_all()
  app.run()


