## Como criar uma API em Python para exibir um gráfico com os dados informados

Neste artigo, vamos criar uma API em Python usando Flask que permitirá a submissão de dados através de um endpoint e
exibirá um gráfico gerado a partir desses dados. Vamos seguir um passo a passo para garantir que você possa reproduzir
esse processo facilmente.

### Passo 1: Instalar as dependências

Primeiro, precisamos instalar as bibliotecas necessárias. Vamos usar Flask para criar a API e Matplotlib para gerar os
gráficos. Para isso, você pode usar o pip:

```bash
pip install flask matplotlib
```

### Passo 2: Estruturar o projeto

Vamos criar uma estrutura básica para o nosso projeto. Crie um diretório para o projeto e dentro dele crie um arquivo
chamado `app.py`.

```
meu_projeto/
│
├── app.py
```

### Passo 3: Criar a aplicação Flask

Dentro do arquivo `app.py`, vamos importar as bibliotecas necessárias e configurar a aplicação Flask.

```python
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)


@app.route('/')
def home():
    return "Bem-vindo à API de Gráficos!"


@app.route('/grafico', methods=['POST'])
def gerar_grafico():
    data = request.get_json()

    if 'valores' not in data:
        return jsonify({"erro": "Os dados enviados devem conter a chave 'valores'."}), 400

    valores = data['valores']

    # Gerar o gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(valores)
    plt.title('Gráfico dos Valores Informados')
    plt.xlabel('Índice')
    plt.ylabel('Valor')

    # Salvar o gráfico em um buffer de bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Converter o gráfico para base64
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return jsonify({"imagem": img_base64})


if __name__ == '__main__':
    app.run(debug=True)
```

### Passo 4: Explicação do código

1. **Importação das bibliotecas**: Importamos Flask para criar a API, request e jsonify para manipular as requisições e
   respostas. Importamos também matplotlib.pyplot para gerar os gráficos, io para manipular streams de dados e base64
   para codificar a imagem gerada.

2. **Configuração da aplicação Flask**: Criamos uma instância do Flask e configuramos uma rota para a página inicial (
   home) que retorna uma mensagem de boas-vindas.

3. **Rota `/grafico`**: Esta é a rota onde nossa API aceitará dados via método POST. O JSON enviado deve conter uma
   lista de valores sob a chave 'valores'. Verificamos se essa chave está presente e, se não estiver, retornamos um
   erro.

4. **Geração do gráfico**: Usamos o Matplotlib para gerar um gráfico a partir dos valores enviados. Em seguida, salvamos
   o gráfico em um buffer de bytes e o convertemos para uma string base64 para que possa ser facilmente transmitido como
   parte da resposta JSON.

5. **Execução do servidor**: Se o script for executado diretamente, iniciamos o servidor Flask no modo debug.

### Passo 5: Testar a API

Para testar a API, você pode usar ferramentas como Postman ou cURL para enviar uma requisição POST
para `http://127.0.0.1:5000/grafico` com o seguinte corpo JSON:

```json
{
  "valores": [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10
  ]
}
```

A resposta será um JSON contendo a imagem do gráfico codificada em base64. Você pode usar essa string para exibir a
imagem em um navegador ou em um aplicativo.

Para visualizar a imagem do gráfico gerado pela API, você precisará decodificar a string base64 recebida na resposta e
exibir a imagem. Vamos ver como fazer isso usando HTML e JavaScript.

### Passo 1: Modificar a API para incluir um template HTML

Vamos modificar a nossa API para retornar uma página HTML com a imagem do gráfico. Atualize o arquivo `app.py` conforme
abaixo:

```python
from flask import Flask, request, render_template_string
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)


@app.route('/')
def home():
    return "Bem-vindo à API de Gráficos!"


@app.route('/grafico', methods=['POST'])
def gerar_grafico():
    data = request.get_json()

    if 'valores' not in data:
        return jsonify({"erro": "Os dados enviados devem conter a chave 'valores'."}), 400

    valores = data['valores']

    # Gerar o gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(valores)
    plt.title('Gráfico dos Valores Informados')
    plt.xlabel('Índice')
    plt.ylabel('Valor')

    # Salvar o gráfico em um buffer de bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Converter o gráfico para base64
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    html = '''
    <!doctype html>
    <title>Gráfico</title>
    <h1>Gráfico dos Valores Informados</h1>
    <img src="data:image/png;base64,{{ img_base64 }}">
    '''

    return render_template_string(html, img_base64=img_base64)


if __name__ == '__main__':
    app.run(debug=True)
```

### Passo 2: Enviar dados para a API e visualizar a imagem

Você pode usar um cliente HTTP como Postman para enviar uma requisição POST para `http://127.0.0.1:5000/grafico` com o
corpo JSON. A resposta será uma página HTML exibindo a imagem do gráfico.

### Exemplo de como enviar dados com Postman

1. **Abra o Postman.**
2. **Configure uma nova requisição:**
    - Método: POST
    - URL: `http://127.0.0.1:5000/grafico`
3. **No corpo da requisição, selecione a opção "raw" e o tipo "JSON".**
4. **Insira o seguinte JSON no corpo da requisição:**

```json
{
  "valores": [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10
  ]
}
```

5. **Envie a requisição.**

A resposta será uma página HTML exibindo a imagem do gráfico gerado.

### Passo 3: Visualizar a imagem diretamente no navegador

A partir da resposta recebida, o navegador renderizará a imagem do gráfico no HTML gerado, permitindo que você veja o
resultado diretamente.

### Conclusão

Com essa modificação, a API agora retorna uma página HTML que exibe o gráfico gerado a partir dos dados enviados. Isso
facilita a visualização do resultado diretamente em um navegador web.