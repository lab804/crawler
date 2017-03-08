# WEB SCRAPING

This is WebScraping!

http://www.cemaden.gov.br/

A classe RequestFile é responsavel por requisitar - atraves de
dados fornecidos de cidade, estado, data e hora - o encaminhamento
dos dados do Cemaden para o email scrapring.cemaden@gmail.com.
Ocorre também o download da imagem do captcha e salva
o código deste mesmo captcha, a fim de formar um banco de dados
para quebra-lo sem a necessidade de digitação ou de serviços terceiros.

A class ReadFile é responsavel por ler o arquivo baixado, realizando
as verificações devidas - se existe, se esta vazio e alertando se
ja foi realizado anteriormente o download -, em busca dos dados pertinentes,
a fim de encaminha-los para o banco de dados.
