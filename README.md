# covidmonitor

Ferramenta desenvolvida para monitorar boletins diários sobre Covid em São Carlos - SP, para acompanhamento junto às portarias envolvendo a volta presencial do IFSP.
A ferramenta foi desenvolvida através do microframework python Flask, utilizando JavaScript para exibir os gráficos e Bootstrap para estilização.
Os dados são obtidos através de webscrap com BeautifulSoup e Pytesseract para extrair dados do boletim, consumindo uma API externa de OCR em caso de falha do Pytesseract.
O armazenamento dos dados é realizado em três tabelas Sqlite.
Deploy pelo Heroku
