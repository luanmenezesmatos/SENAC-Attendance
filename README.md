# SENAC-Attendance

Este repositório foi criado com o objetivo de automatizar o monitoramento de faltas no site do SENAC (Sistema Nacional de Aprendizagem Comercial) semanalmente.

## Aviso Legal

- 🚧 É importante ressaltar que o código foi desenvolvido para fins de estudo e não deve ser utilizado para fins maliciosos. Quaisquer danos causados pelo uso indevido do código não são de responsabilidade do autor.

## Por que automatizar?

O site do SENAC não possui uma opção de notificação de faltas, sendo assim, o aluno precisa acessar o site semanalmente para verificar se há alguma falta. Com o código, o aluno pode automatizar esse processo e receber um e-mail com a quantidade de faltas semanais.

## Como funciona?

O código utiliza a biblioteca Selenium para automatizar o processo de login e navegação no site do SENAC. Após o login, o código acessa a página de frequência e verifica se há alguma falta na semana atual. Caso haja, o código envia um e-mail para o usuário com a quantidade de faltas.

## Como utilizar?

Para utilizar o código, é necessário ter o Python 3 instalado na máquina. Além disso, é necessário instalar a biblioteca Selenium e o driver do navegador utilizado. Para instalar a biblioteca, basta executar o seguinte comando no terminal:

```bash
pip install selenium
pip install python-dotenv
```

- O **Selenium** é uma biblioteca que permite a automação de processos em navegadores. Para mais informações, acesse: https://www.selenium.dev/pt-br/documentation/webdriver/getting_started/
- O **python-dotenv** é uma biblioteca que permite a utilização de variáveis de ambiente. Para mais informações, acesse: https://pypi.org/project/python-dotenv/

É necessário que, caso o usuário seja um aluno do SENAC, o e-mail e senha sejam alterados no código (pode ser encontrado em **.env.example**). Além disso, é necessário que o usuário altere o e-mail de destino para que o código possa enviar o e-mail com as informações.
- Certifique-se de renomear o arquivo **.env.example** para **.env**

Após a instalação das dependências, basta executar o código com o seguinte comando:

```bash
python attendance.py
```

## Observações

- O código foi desenvolvido para o navegador **Google Chrome**, porém pode ser facilmente adaptado para outros navegadores. Para isso, basta alterar a linha 14 do arquivo **attendance.py** para o navegador desejado, os disponíveis são:
	- **"`chrome`" - Chrome (padrão)**
	- **"`firefox`" - Firefox**
	- **"`edge`" - Edge**
	- **"`safari`" - Safari**
	- **"`opera`" - Opera**
	- **"`ie`" - Ie**

Certifique-se de que o nome do navegador está escrito corretamente (deve ser escrito exatamente `chrome` ou o navegador desejado), caso contrário o código não irá funcionar.

## Me Apoie

> Se você gostou do código e quer me apoiar, me ajude dando uma estrela no repositório e me siga aqui no **GitHub** e no [**LinkedIn**](https://www.linkedin.com/in/luanmenezesmatos/), muito obrigado!