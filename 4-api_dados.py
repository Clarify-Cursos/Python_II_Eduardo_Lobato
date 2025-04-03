# O código cria um aplicativo simples Flask que, quando acessado na URL raiz (por exemplo, http://localhost:5000/), retorna a mensagem "Hello woooooooooorld".

# A aplicação está configurada para rodar em modo de depuração, o que facilita o desenvolvimento.


from flask import Flask, jsonify, send_file
# import pandas as pd
# import io
# import base64
# import matplotlib.pyplot

# Criar o app do Flask
app = Flask(__name__)

@app.route('/')
def pagina_inicial():
    return "Hello woooooooooorld"



# Rodar a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True)
