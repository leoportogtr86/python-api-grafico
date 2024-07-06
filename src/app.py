from flask import Flask, request, render_template_string, jsonify
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
