import psycopg2 as pg
from psycopg2 import Error
from dotenv import load_dotenv
import os
import pandas as pd
import yfinance as yf
from datetime import date, timedelta

class Acoes:
    def __init__(self):
        load_dotenv()        

    def conn (self):
        try:
            senha = os.getenv('db_passowrd')
            self.conectar = pg.connect(
                user = "postgres",
                password=senha ,
                host = "localhost",
                port= 5432,
                dbname="teste" 
                )
            print("Conectado com sucesso...")
            self.cursor = self.conectar.cursor() 
            return self.conectar,self.cursor

        except Error as e:
            print(f'Ocorreu um erro... {e}')

    def encerrar_conexao (self):
        if self.conectar:
            self.conectar.close()
            print("Conexao encerrada...")

    def pegar_acao (self,acao):
        self.data_1 = date.today() - timedelta(days=5)
        self.data_2 =date.today() - timedelta(days=1)
        self.acao = acao
        df_acao = yf.download(tickers=self.acao, start=self.data_1,end=self.data_2,interval='1d') 
        self.preco_inicial= df_acao['Open'].iloc[-1:].values[0].round(2)
        self.preco_inicial=float(self.preco_inicial[0])
        self.preco_final= df_acao['Close'].iloc[-1:].values[0].round(2)
        self.preco_final=float(self.preco_final[0])
        self.ultima_data = df_acao.index[-1]
        self.ultima_data = self.ultima_data.date()

        return self.ultima_data,self.preco_inicial,self.preco_final

    def inserir_acoes(self):
            comando_inserir="INSERT INTO acoes_python (ticter, nome, preco_inicial, preco_final,data_1) VALUES (%s,%s,%s,%s,%s);"
            values= self.acao, self.acao, self.preco_inicial, self.preco_final,self.ultima_data
            #values= 'aaaa', 'bbbbb', 5, 6,'2026-01-01'
            self.cursor.execute(comando_inserir,values)
            self.conectar.commit()
            print("Dados inseridos com sucesso...")  

    def selecao (self):
            comando_select="SELECT ticter, nome, preco_inicial, preco_final,data_1 FROM acoes_python"
            self.cursor.execute(comando_select)
            acoes=self.cursor.fetchall()
            for acoes in acoes:
                print(acoes)
            return acoes
    
    def atualizar (self):
        comando_atualizar=f"UPDATE acoes_python SET preco_inicial = {self.preco_inicial}, preco_final = {self.preco_final}, data_1 = '{self.ultima_data}' WHERE ticter='{self.acao}'"       
        self.cursor.execute(comando_atualizar)
        self.conectar.commit()
        print('Atualizacao realizada...')
  
    def deletar (self,acao):
        comando_delete=f"DELETE FROM acoes_python WHERE ticter='{acao}'"
        self.cursor.execute(comando_delete)
        self.conectar.commit()
        print(f'Comando executado... {acao} deletado...')
    
        
