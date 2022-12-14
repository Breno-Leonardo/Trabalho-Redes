# Trabalho-Redes

## Trabalho Redes de Computadores I

Equipe 05: 
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
