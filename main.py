
from funcoes import *

def main():
    
    acao = Acoes()
    acao.conn()
    #acao.pegar_acao("CYRE3.SA")
    #acao.inserir_acoes()
    #acao.selecao()   
    #acao.atualizar() 
    #acao.deletar('PETR4')
    
    acao.encerrar_conexao()

if __name__ =='__main__':
    main()