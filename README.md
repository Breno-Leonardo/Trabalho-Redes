# Trabalho-Redes

## Trabalho Redes de Computadores I

SOCKET SHARE - Equipe 05 : 
* Benjamin Anderson
* Breno Leonardo Lima Macedo
* Julio Cesar Lopes
* Raquel Marques

## Bibliotecas Utilizadas

Para o trabalho, foram utilizadas as seguintes bibliotecas:

* EEL: Para a interface gráfica, foi utilizado eel que permite utilizar HTML, CSS e JavaScript  juntamente com Python, expondo funções Python para o JavaScript e vice-versa, utilizando a tag @eel.expose e eel.expose().

* Bootstrap: É um framework web que permite o desenvolvimento responsivo de sites mobile-first

* SweetAlert: Interface que permite a criação de alertas responsivos e customizados em aplicações web. 

* jQuery: jQuery é uma biblioteca de código aberto, possui sintaxe que simplifica: a navegação do documento HTML, a seleção de elementos DOM.

### Para instalar a Ell:

```
pip install eel
```

## main.py

Define a pasta do HTML e CSS.

```
eel.init('www')
```

Inicia a aplicação e passa a função close_callback para quando fechar a pagina fechar o socket

```
eel.start('index.html', block=False, mode='edge-app', close_callback=close_callback)
```

## Funções
```
 listDirHashCodes()
```

Encontra o caminho absoluto para o local files e obtém todos os arquivos juntamente com o HashCode de cada arquivo.
```
add_file(byteArray, fileName)
```

Adiciona o arquivo, escrevendo bytes recebidos por parâmetro no arquivo no local files 

```
upload_file(file, copies)
```
Faz o upload do arquivo

```
delete_file(fileName)
```

Recebe o nome do arquivo como parâmetro, encontra o caminho dele e exclui se existe.

```
client = Client(9001, eel.updateOnline, eel.updateIp)
client.online()
client.listen()
```

Nessas linhas é definido a porta do cliente e passando funções callback para fazer o update da interface. Em client.online() ele conecta com o servidor e .listen() ele fica escutando.
 
 ```
while True:
   _dirFiles, _hashcodes = listDirHashCodes()
   # print(writingFile)
   if not writingFile:
       if _hashcodes != hashcodes:
           hashcodes = _hashcodes
           eel.showFiles(_dirFiles)
   eel.sleep(1)
```

Nessa parte ele lê o diretório e  verifica se houve alguma mudança no diretório para alterar na pasta de arquivos.

## File.py

Cria um objeto com todas as informações necessárias do arquivo, nome, tamanho, tipo e sha256.

## ClientClass.py

A classe que faz a conexão com o ambiente.

```
def __init__(self, PORT, activeConnectionsFunction, ipAddressFunction, HOST=SERVER_HOST)
```
Informa o host, porta e cria uma thread para o processamento paralelo, passando para ela a função (.thread_listen ), para assim não interferir na execução principal.  

```
def closeConnection(self)
```

Fecha a conexão

```
def online(self)
```

Cria a conexão

```
def uploadFile(self, message)
```

```
def send(self, msg)
```

Informa inicialmente o tamanho da mensagem, após a leitura o socket cria um buffer do tamanho da mensagem e completa o header que precisa ter 64 bytes.

```
def thread_listen(self)
```

Dependendo do inicio da mensagem toma determinada ação:

```
[ACTIVE CONNECTIONS]
```
Mensagem referente a quantidade de pessoas conectadas

```
[IP ADDRESS]
```

Mensagem referente ao IP

```
[DOWNLOAD]
```

Mensagem referente ao Download

## www

Nessa pasta estão os arquivos html, css e js, com o eel.expose() é possível expor as funções dentro da tag <script> para o python 

## Melhorias

* O menu lateral na esquerda tem as opções de Uploads e Downloads, em uma melhoria de versão, seria interessante adicionar o horário e mais informações de cada upload e download de arquivos.

* A tabela de arquivos locais tem um pequeno erro que ao excluir todos os arquivos o botão trava e não conseguimos adicionar arquivos novamente.

## Referências

* Tanenbaum, A.S., Redes de Computadores, Tradução da 4a Edição, Editora Campus, 2003.
* Stallings, W., Redes e Sistemas de Comunicação de Dados, Editora Campus, 2005.
* COMER, D. E. Interligação de Redes com TCP/IP, Vol. I: Princípios, Protocolos e Arquitetura.
5a ed., Ed. Campus, 2006.
* PAULA FILHO, W.P. Multimídia: Conceitos e Aplicações. LTC editora, Rio de Janeiro, 2000.
* LOPES, Raquel V., SAUVÉ, Jacques P. e NICOLLETTI, Pedro S. Melhores Práticas para
Gerência de Redes de Computadores. E
Kurose, J., Ross, K., Redes de Computadores e a Internet - Uma Abordagem Top-Down, 6a
Edição. Addison Wesley, 2013.
* Kurose, J., Ross, K., Computer Networking, 7th. Ed., Addison-Wesley, 2016.

* https://realpython.com/python-sockets/
