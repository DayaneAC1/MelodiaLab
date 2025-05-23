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
    cursor.execute('''SELECT COUNT(email) FROM usuarios WHERE email=?''',(formulario['email'],))
    conexao.commit()
    
    quantidade_de_emails = cursor.fetchone()
    print(quantidade_de_emails)
    
    
    if quantidade_de_emails[0] == 0:
        print("E-mail não cadastrado! Tente novamente")
        return False
    
    cursor.execute('''SELECT senha FROM usuarios WHERE email=?''', (formulario['email'],))
    conexao.commit()
    senha_criptografada = cursor.fetchone()
    
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
        
def criar_musica (formulario, email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''INSERT INTO projetos_musicais (nome_musica, artista, status, letra, email_usuario) 
                   VALUES (?, ?, ?, ?, ?)''', (formulario ['nome_musica'],
                    formulario['artista'], formulario['status'], formulario['letra'], email))
    conexao.commit()
    
def pegar_musicas (email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT * FROM projetos_musicais WHERE email_usuario=?''', (email,))
    return cursor.fetchall()

def editar_musica(formulario, id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''UPDATE projetos_musicais SET nome_musica=?, artista=?, status=?, letra=? WHERE id=?''',
                   (formulario['nome_musica'], formulario['artista'], formulario['status'], formulario['letra'], id))
    conexao.commit()
    return True

def pegar_musica(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT * FROM projetos_musicais WHERE id=?''', (id,))
    return cursor.fetchone()

def excluir_musica(id, email_usuario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    #Verificar se o email que quer excluir a tarefa é realmente dono da tarefa
    cursor.execute('''SELECT email_usuario FROM projetos_musicais WHERE id=?''', (id,))
    email = cursor.fetchone()
    if(email_usuario != email[0]):
        return False
    else:
        cursor.execute('''DELETE FROM projetos_musicais WHERE id=?''', (id,))
        conexao.commit()
        return True

def excluir_usuario(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute('''DELETE FROM projetos_musicais WHERE email_usuario=?''',(email,))
    cursor.execute('''DELETE FROM usuarios WHERE email=?''',(email,))
    conexao.commit()
    return True
    

# PARTE PRINCIPAL DO PROGRAMA
if __name__ == '__main__':
    print("Hello, world!")
    criar_tabelas()