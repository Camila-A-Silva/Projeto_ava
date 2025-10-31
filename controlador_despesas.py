import ttkbootstrap as ttk
import sqlite3
import tkinter as tk
from tkinter import messagebox


class Despesas:

    def __init__(self):
        
        #Criando a janela
        self.janela = ttk.Window(themename="morph",
                                   title="Controle de Despesas")
        
        #Tamanho da janela
        self.janela.geometry("1400x700+250+150")

        #Titulo da pagina
        label_titulo = ttk.Label(self.janela,
                                 text="Controle de Despesas",
                                 font=("Broadway", 25))
        label_titulo.pack(pady=(10,0))

        frame_texto = ttk.Frame(self.janela)
        frame_texto.pack(side="left", padx=(50,10))

        #Testo da descrição
        label_desc = ttk.Label(frame_texto,
                               text="Descrição",
                               font=("Perpetua", 20))
        label_desc.pack(pady=(0,5))

        #Caixa de texto da descrição
        self.entry_desc = ttk.Entry(frame_texto, width=35)
        self.entry_desc.pack()

        #Testo do valor
        label_valor = ttk.Label(frame_texto,
                               text="Valor",
                               font=("Perpetua", 20))
        label_valor.pack(pady=5)

        #Caixa de texto do valor
        self.entry_valor = ttk.Entry(frame_texto, width=35)
        self.entry_valor.pack()

        #Testo da categoria
        label_categ = ttk.Label(frame_texto,
                               text="Categoria",
                               font=("Perpetua", 20))
        label_categ.pack(pady=5)

        #Caixa de texto da descrição
        self.entry_categ = ttk.Entry(frame_texto, width=35)
        self.entry_categ.pack()

        #Testo da descrição
        label_data = ttk.Label(frame_texto,
                               text="Data",
                               font=("Perpetua", 20))
        label_data.pack(pady=5)

        #Caixa de texto da descrição
        self.entry_data = ttk.Entry(frame_texto, width=35)
        self.entry_data.pack()

        #Frame pra deixar os botão um do lado do outro
        frame_botao = ttk.Frame(frame_texto)
        frame_botao.pack(pady=10)

        #Botão para adicionar os itens na treeview
        botao_add = ttk.Button(frame_botao,
                           text="ADICIONAR",
                           style="success",
                           command=self.adicionar)
        botao_add.pack(side="left", pady=15, padx=5)

        #Botão para excluix os itens na treeview
        botao_exc = ttk.Button(frame_botao,
                           text="EXCLUIR",
                           style="danger",
                           command=self.excluir)
        botao_exc.pack(side="left", pady=15, padx=5)

        #Botão para atualizar os itens na treeview
        botao_atl = ttk.Button(frame_botao,
                           text="ATUALIZAR",
                           style="warning")#secondary
        botao_atl.pack(side="right", pady=15, padx=5)

        self.treeview = ttk.Treeview(self.janela, height= 30,padding=80)
        self.treeview.pack(pady=30)

        self.treeview["columns"] = ("descricao", "valor", "categoria", "data")
        self.treeview["show"] = "headings"
        
        self.treeview.heading("descricao",text="Descrição")
        self.treeview.heading("valor", text="Valor")
        self.treeview.heading("categoria", text="Categoria")
        self.treeview.heading("data",text="Data")
        
        #conectando ao banco de dado
        conexao = sqlite3.connect("bd_controle_despesas.sqlite")
        #criando o cursor, responsavel por comandas o bando de dados 
        cursor = conexao.cursor()

        sql_para_criar_tabela = """
                                    CREATE TABLE IF NOT EXISTS despesas (
                                    descricao VARCHAR(200),
                                    valor INT,
                                    categoria VARCHAR(200),
                                    data DATE PRIMARY KEY
                                    );
                                """
        
        #para executar
        cursor.execute(sql_para_criar_tabela)
        #Comitei as alterações
        conexao.commit()
        #Fechei a conexão
        cursor.close()
        conexao.close()
        
        # Ligando o def prencer com o init pelo event
        self.treeview.bind("<<TreeviewSelect>>", self.preencher)

        # Ligando o def lista_salva com o init pelo event
        self.lista_salva()
        

    #Função do botão adicionar
    def adicionar(self):
        # get para verificar se tem alguma coisa escrita no entry (caixa de texto)
        desc = self.entry_desc.get()
        valor = self.entry_valor.get()
        categ = self.entry_categ.get()
        date = self.entry_data.get()

        if desc == "" or valor == "" or categ == "" or date == "":
            messagebox.showerror(message="Digite para adicionar!")#mensagem de erro
                       
        else:
            self.treeview.insert("",tk.END,values=[desc, valor, categ, date])#end é para inserir
            #Apagar as coisas escritas no entry ao adicionar no tree
            self.entry_desc.delete(0,tk.END)
            self.entry_valor.delete(0,tk.END)
            self.entry_categ.delete(0,tk.END)
            self.entry_data.delete(0,tk.END)


            #Enviar para o banco de 
            #criando a conexão
            conexao = sqlite3.connect("bd_controle_despesas.sqlite")
            cursor = conexao.cursor()

            #sql do insert, inserir os items no bd
            sql_insert = """
                            INSERT INTO despesas (descricao, valor, categoria, data)
                            VALUES (?, ?, ?, ?)
                        """
             
            cursor.execute(sql_insert,[desc, valor, categ, date])#executar comando
            conexao.commit()#comitando o comando       

            #fechando cursor e a conexao
            cursor.close()
            conexao.close() 

    #função para excluir os dados do tree e do bd
    def excluir(self):
        escolhida = self.treeview.selection()
        if escolhida == "":
            messagebox.showerror(message="Selecione uma linha para excluir!")
        else:
            self.treeview.item(escolhida)
            self.treeview.delete(escolhida)

            desc = self.entry_desc.get()
            valor = self.entry_valor.get()
            categ = self.entry_categ.get()
            date = self.entry_data.get()

            #Excluindo no bd
            conexao = sqlite3.connect("bd_controle_despesas.sqlite")
            cursor = conexao.cursor()
            # função para excluir da tabela
            sql_delete = """
                            DELETE FROM despesas
                            WHERE descricao = (?) AND valor = (?) AND categoria = (?) AND data = (?)
                        """
            #função
            cursor.execute(sql_delete,[desc, valor, categ, date])
            conexao.commit()
            #Fechar
            cursor.close()
            conexao.close()

            #Excluir do entry se for deletado
            self.entry_desc.delete(0,tk.END)
            self.entry_valor.delete(0,tk.END)
            self.entry_categ.delete(0,tk.END)
            self.entry_data.delete(0,tk.END)

    #def para prencer o campo do entry ao clicar na linha do tree
    def preencher(self, event):
        # Obter o item da linha q foi selecionado
        linha_selecionada = self.treeview.focus()

        if linha_selecionada:
            # Obter os valores da linha selecionada
            valores = self.treeview.item(linha_selecionada, 'values')
            
            # Verificar se existem alguma coisa na linha
            if valores:
                # Inserir os valores nos campos Entry
                # Os índices correspondem às colunas na Treeview: [0] descrição, [1] valor, [2] categoria, [3] data
                self.entry_desc.insert(0, valores[0])
                self.entry_valor.insert(0, valores[1])
                self.entry_categ.insert(0, valores[2])
                self.entry_data.insert(0, valores[3])
        
    #def para atualizar a lsta
    def atualizar(self):
        pass


    #def para trazer a lista salva do bd para o treeview
    def lista_salva(self):
               
        conexao = sqlite3.connect("bd_controle_despesas.sqlite")
        cursor = conexao.cursor()

        sql_para_selecionar_despesas = """ SELECT descricao, valor, categoria, data FROM despesas; """

        cursor.execute(sql_para_selecionar_despesas)

        #O fatchall vai trazer uma lista de lista
        lista_de_despesas = cursor.fetchall()
         
        cursor.close()
        conexao.close()

        #Inserindo os itens na treeview
        for linha in lista_de_despesas:
            self.treeview.insert("","end",values=[linha[0], linha[1], linha[2], linha[3]])


    def run(self):
        self.janela.mainloop()

if __name__ == "__main__":
    pag = Despesas()
    pag.run()
