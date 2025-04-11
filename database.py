from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from flask import Flask, session

def conectar_banco():
    conexao = sqlite3.connect("tarefa.db")
    return conexao

def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''create table if not exists usuarios
                   (email text primary key,nome text,senha text)''')
    
    cursor.execute('''create table if not exists projetos_musicais 
                   (id integer primary key, nome_musica text, artista text, 
                   status text, letra text, caminho_capa text, email_usuario text,
                   foreign key (email_usuario) references usuarios(email))''')
    
def criar_usuario (formulario):
    # Verificar se o email já existe no Banco de Dados
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT COUNT (email) FROM usuarios WHERE email=?''',(formulario['email'],))
    
    quantidade_de_emails_cadastrados = cursor.fetchone()
    
    if(quantidade_de_emails_cadastrados[0] > 0):
        print("LOG: Já existe esse e-mail cadastrado no banco!")
        return False 
    
    cursor.execute('''INSERT INTO usuarios (email, nome, senha) 
                   VALUES (?, ?, ?)''', (formulario ['email'],
                    formulario['nome'], generate_password_hash (formulario['senha'],)))
    conexao.commit()
    return True

def login(formulario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    #Verificando se o e-mail existe no banco de dados
    cursor.execute('''SELECT COUNT(email) FROM usuarios WHERE email=?''',(formulario['email'],))
    conexao.commit()
    
    quantidade_de_emails = cursor.fetchone()
    print(quantidade_de_emails)
    
    #Se o e-mail não estiver cadastrado, retorna False
    
    if quantidade_de_emails[0] == 0:
        print("E-mail não cadastrado! Tente novamente")
        return False
    
    #Obtenha a senha criptografada do usuário no banco
    
    cursor.execute('''SELECT senha FROM usuarios WHERE email=?''', (formulario['email'],))
    conexao.commit()
    senha_criptografada = cursor.fetchone()
    
    #Verificando se a senha fornecida corresponde à senha armazenada
    return check_password_hash(senha_criptografada[0], formulario['senha'])

def verificar_usuario (formulario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT senha FROM usuarios WHERE email=?''',(formulario['email'],) )
    
    usuario = cursor.fetchone()
    
    if usuario is None:
        return False
        
    else:
        if check_password_hash(usuario[0], (formulario ["senha"])):
            return True
        else:
            return False
        
def criar_musica (formulario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''INSERT INTO projetos_musicais (nome_musica, artista, status, letra) 
                   VALUES (?, ?, ?, ?)''', (formulario ['nome_musica'],
                    formulario['artista'], formulario['status'], formulario['letra']))
    conexao.commit()
    
def pegar_musicas ():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT * FROM projetos_musicais ''')
    return cursor.fetchall()
    
    

# PARTE PRINCIPAL DO PROGRAMA
if __name__ == '__main__':
    print("Hello, world!")
    criar_tabelas()