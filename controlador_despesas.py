import ttkbootstrap as ttk
import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime



class Despesas:

    def __init__(self):
        
        #Criando a janela
        self.janela = ttk.Window(themename="morph",
                                   title="Controle de Despesas")
        
        #Tamanho da janela
        self.janela.geometry("1400x700+250+150")

        notebook = ttk.Notebook(self.janela)
        notebook.pack(expand=True)

        # Aba de Gerenciamento
        aba_gerenciar = ttk.Frame(notebook)
        notebook.add(aba_gerenciar, text="Gerenciar Despesas")
        #Frame que vai colocar tudo em um 'notebook' de página
        janela = ttk.Frame(aba_gerenciar)
        janela.pack()

        #Titulo da pagina
        label_titulo = ttk.Label(janela,
                                 text="Controle de Despesas",
                                 font=("Broadway", 25))
        label_titulo.pack(pady=(10,0))

        #frame para colocar os texto em um conteiner para ficar todos juntos
        frame_texto = ttk.Frame(janela)
        frame_texto.pack(side="left", padx=(50,10))

        #Testo da descrição
        label_desc = ttk.Label(frame_texto,
                               text="Descrição",
                               font=("Perpetua", 15))
        label_desc.pack(pady=(0,5))

        #Caixa de texto da descrição
        self.entry_desc = ttk.Entry(frame_texto, width=35)
        self.entry_desc.pack()

        #Testo da categoria
        label_categ = ttk.Label(frame_texto,
                               text="Categoria",
                               font=("Perpetua", 15))
        label_categ.pack(pady=5)

        #Caixa de texto da descrição
        self.entry_categ = ttk.Entry(frame_texto, width=35)
        self.entry_categ.pack()

        #Testo do valor
        label_valor = ttk.Label(frame_texto,
                               text="Valor",
                               font=("Perpetua", 15))
        label_valor.pack(pady=5)

        #Caixa de texto do valor
        self.entry_valor = ttk.Entry(frame_texto, width=35)
        self.entry_valor.pack()

        #Testo da descrição
        label_data = ttk.Label(frame_texto,
                               text="Data (YYYY-MM-DD)",
                               font=("Perpetua", 15))
        label_data.pack(pady=5)

        #Caixa de texto da descrição
        self.entry_data = ttk.Entry(frame_texto, width=35)
        self.entry_data.pack()

        #Frame pra deixar os botão um do lado do outro dentro do conteiner dos textos
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
                           style="warning",
                           command=self.atualizar)#secondary
        botao_atl.pack(side="right", pady=15, padx=5)


        # Aba de Dashboard 
        aba_dashboard = ttk.Frame(notebook)
        notebook.add(aba_dashboard, text="Gasto total do mês")

        self.mes_label = ttk.Label(aba_dashboard, text="💰 Total gasto no mês atual:", font=("Broadway", 25))
        self.mes_label.pack(pady=(200,20))

        self.total_label = ttk.Label(aba_dashboard, text="R$ 0.00", font=("Broadway", 25))
        self.total_label.pack()


        #Treeview
        self.treeview = ttk.Treeview(janela, height= 30,padding=80)
        self.treeview.pack(pady=30)

        self.treeview["columns"] = ("descricao", "categoria", "valor", "data")
        self.treeview["show"] = "headings"
        
        self.treeview.heading("descricao",text="Descrição")
        self.treeview.heading("categoria", text="Categoria")
        self.treeview.heading("valor", text="Valor")
        self.treeview.heading("data",text="Data")
        
        #conectando ao banco de dado
        conexao = sqlite3.connect("bd_controle_despesas.sqlite")
        #criando o cursor, responsavel por comandas o bando de dados 
        cursor = conexao.cursor()

        sql_para_criar_tabela = """
                                    CREATE TABLE IF NOT EXISTS despesas (
                                    descricao VARCHAR(200),
                                    categoria VARCHAR(200),
                                    valor DECIMAL,
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

        # Ligando o def lista_salva com o init 
        self.lista_salva()

        #ligando o def atualizar_dashboard para atualizar o tottal gasto do mês
        self.atualizar_dashboard()
        

    #Função do botão adicionar
    def adicionar(self):
        # get para verificar se tem alguma coisa escrita no entry (caixa de texto)
        desc = self.entry_desc.get()
        categ = self.entry_categ.get()
        valor = self.entry_valor.get()
        date = self.entry_data.get()

        if desc == "" or categ == "" or valor == "" or date == "":
            messagebox.showerror(message="Digite para adicionar!")#mensagem de erro
                       
        else:
            self.treeview.insert("",tk.END,values=[desc, categ, valor, date])#end é para inserir
            #Apagar as coisas escritas no entry ao adicionar no tree
            self.entry_desc.delete(0,tk.END)
            self.entry_categ.delete(0,tk.END)
            self.entry_valor.delete(0,tk.END)
            self.entry_data.delete(0,tk.END) 

        #Enviar para o banco de 
        #criando a conexão
        conexao = sqlite3.connect("bd_controle_despesas.sqlite")
        cursor = conexao.cursor()

        #sql do insert, inserir os items no bd
        sql_insert = """
                        INSERT INTO despesas (descricao, categoria, valor, data)
                        VALUES (?, ?, ?, ?)
                    """
            
        cursor.execute(sql_insert,[desc, categ, valor, date])#executar comando
        conexao.commit()#comitando o comando       

        #fechando cursor e a conexao
        cursor.close()
        conexao.close()

        #Para manter a dashboard atualizada
        self.atualizar_dashboard()

    #função para excluir os dados do tree e do bd
    def excluir(self):
        escolhida = self.treeview.selection()
        if escolhida == "":
            messagebox.showerror(message="Selecione uma linha para excluir!")
        else:
            self.treeview.item(escolhida)
            self.treeview.delete(escolhida)

            desc = self.entry_desc.get()
            categ = self.entry_categ.get()
            valor = self.entry_valor.get()
            date = self.entry_data.get()

            #Excluindo no bd
            conexao = sqlite3.connect("bd_controle_despesas.sqlite")
            cursor = conexao.cursor()
            # função para excluir da tabela
            sql_delete = """
                            DELETE FROM despesas
                            WHERE descricao = (?) AND categoria = (?) AND valor = (?) AND data = (?)
                        """
            #função
            cursor.execute(sql_delete,[desc, categ, valor, date])
            conexao.commit()
            #Fechar
            cursor.close()
            conexao.close()

            #Excluir do entry se for deletado
            self.entry_desc.delete(0,tk.END)
            self.entry_categ.delete(0,tk.END)
            self.entry_valor.delete(0,tk.END)
            self.entry_data.delete(0,tk.END)
        
        #Para manter a dashboard atualizada
        self.atualizar_dashboard()

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
                self.entry_categ.insert(0, valores[1])
                self.entry_valor.insert(0, valores[2])
                self.entry_data.insert(0, valores[3])
        
    #def para atualizar a lIsta
    def atualizar(self):
        # Verificar se há uma linha selecionada
        selecionado = self.treeview.selection()
        if not selecionado:
            messagebox.showinfo("Info", "Selecione uma despesa para atualizar.")
            return

        # Obter os valores antigos (antes da atualização)
        valores_antigos = self.treeview.item(selecionado, "values")
        data_antiga = valores_antigos[3]  # usamos a data antiga como chave primária

        desc = self.entry_desc.get()
        categ = self.entry_categ.get()
        valor = self.entry_valor.get()
        data = self.entry_data.get()

        # Verificações básicas
        if not (desc and categ and valor and data):
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        try:
            valor = float(valor)
            datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Valor ou data inválidos.")
            return

        # Atualizar no banco de dados
        conexao = sqlite3.connect("bd_controle_despesas.sqlite")
        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE despesas
            SET descricao = ?, categoria = ?, valor = ?, data = ?
            WHERE data = ?
        """, (desc, categ, valor, data, data_antiga))
        conexao.commit()
    
        cursor.close()
        conexao.close()

        # Atualizar a linha na Treeview
        self.treeview.item(selecionado, values=(desc, categ, valor, data))

        # Atualizar o dashboard
        self.atualizar_dashboard()

        # Limpar os campos
        self.entry_desc.delete(0, tk.END)
        self.entry_categ.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
        self.entry_data.delete(0, tk.END)
        
    #def para trazer a lista salva do bd para o treeview
    def lista_salva(self):
               
        conexao = sqlite3.connect("bd_controle_despesas.sqlite")
        cursor = conexao.cursor()

        sql_para_selecionar_despesas = """ SELECT descricao, categoria, valor, data FROM despesas; """

        cursor.execute(sql_para_selecionar_despesas)

        #O fatchall vai trazer uma lista de lista
        lista_de_despesas = cursor.fetchall()
         
        cursor.close()
        conexao.close()

        #Inserindo os itens na treeview
        for linha in lista_de_despesas:
            self.treeview.insert("","end",values=[linha[0], linha[1], linha[2], linha[3]])

    #def para atualizar o Dashboard
    def atualizar_dashboard(self):
        data = datetime.now()
        mes_atual = data.strftime("%Y-%m")

        conexao = sqlite3.connect("bd_controle_despesas.sqlite")
        cursor = conexao.cursor()

        # Consulta SQL correta para somar o valor das despesas do mês atual
        cursor.execute("""
            SELECT SUM(valor)
            FROM despesas
            WHERE strftime('%Y-%m', data) = ?
        """, (mes_atual,))

        total = cursor.fetchone()[0]
        total = total if total else 0.0

        cursor.close()
        conexao.close()

        # Atualiza o label no dashboard
        self.mes_label.configure(text=f"💰 Total gasto em {mes_atual}: ")
        self.total_label.configure(text=f"R$ {total:.2f}")

    def run(self):
        self.janela.mainloop()

if __name__ == "__main__":
    pag = Despesas()
    pag.run()
