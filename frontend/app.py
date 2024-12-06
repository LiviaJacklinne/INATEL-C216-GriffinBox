from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import os

app = Flask(__name__)

# Definindo as variáveis de ambiente
API_BASE_URL = "http://backend:8000"

# Rota para a página inicial
@app.route('/')
def home():
    return render_template('home.html')

# Rota para exibir o formulário de cadastro
@app.route('/cadastro', methods=['GET'])
def inserir_musica_form():
    return render_template('cadastro.html')

# Rota para enviar os dados do formulário de cadastro para a API
@app.route('/adicionar', methods=['POST'])
def inserir_musica():
    nome = request.form['nome']
    cantor = request.form['cantor']
    album = request.form['album']
    duracao = request.form['duracao']

    payload = {
        'nome': nome,
        'cantor': cantor,
        'album' : album,
        'duracao' : duracao
    }

    response = requests.post(f'{API_BASE_URL}/api/v1/musicas/', json=payload)
    
    if response.status_code == 201:
        return redirect(url_for('listar_musicas'))
    else:
        return "Erro ao inserir musica", 500

# Rota para listar todas as musicas
@app.route('/playlist', methods=['GET'])
def listar_musicas():
    response = requests.get(f'{API_BASE_URL}/api/v1/musicas/')
    try:
        musicas = response.json()
    except:
        musicas = []
    return render_template('playlist.html', musicas=musicas)

# Rota para exibir o formulário de edição de musica
@app.route('/atualizar/<int:musica_id>', methods=['GET'])
def atualizar_musica_form(musica_id):
    response = requests.get(f"{API_BASE_URL}/api/v1/musicas/")
    #filtrando apenas o musica correspondente ao ID
    musicas = [musica for musica in response.json() if musica['id'] == musica_id]
    if len(musicas) == 0:
        return "musica não encontrado", 404
    musica = musicas[0]
    return render_template('atualizar.html', musica=musica)

# Rota para enviar os dados do formulário de edição de musica para a API
@app.route('/atualizar/<int:musica_id>', methods=['POST'])
def atualizar_musica(musica_id):
    nome = request.form['nome']
    cantor = request.form['cantor']
    album = request.form['album']
    duracao = request.form['duracao']

    payload = {
        'id': musica_id,
        'nome': nome,
        'cantor': cantor,
        'album' : album,
        'duracao' : duracao
    }

    response = requests.patch(f"{API_BASE_URL}/api/v1/musicas/{musica_id}", json=payload)
    
    if response.status_code == 200:
        return redirect(url_for('listar_musicas'))
    else:
        return "Erro ao atualizar musica", 500


# Rota para excluir uma musica
@app.route('/excluir/<int:musica_id>', methods=['POST'])
def excluir_musica(musica_id):
    response = requests.delete(f"{API_BASE_URL}/api/v1/musicas/{musica_id}")
    
    if response.status_code == 200  :
        return redirect(url_for('listar_musicas'))
    else:
        return "Erro ao excluir musica", 500


#Rota para resetar o database
@app.route('/reset-database', methods=['GET'])
def resetar_database():
    response = requests.delete(f"{API_BASE_URL}/api/v1/musicas/")
    
    if response.status_code == 200  :
        return render_template('resetdb.html')
    else:
        return "Erro ao resetar o database", 500


if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')