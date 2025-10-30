import ttkbootstrap as ttk


class Despesas:

    def __init__(self):
        
        #Criando a janela
        self.janela = ttk.Window(themename="morph",
                                   title="Controle de Despesas")
        
        #Tamanho da janela
        self.janela.geometry("1100x700+400+150")

        #Titulo da pagina
        label_titulo = ttk.Label(self.janela,
                                 text="Controle de Despesas",
                                 font=("Broadway", 20))
        label_titulo.pack(pady=(10,15))

        frame_texto = ttk.Frame(self.janela)
        frame_texto.pack(side="left", padx=20)

        #Testo da descrição
        label_desc = ttk.Label(frame_texto,
                               text="Descrição",
                               font=("Perpetua, 15"))
        label_desc.pack()

        #Caixa de texto da descrição
        entry_desc = ttk.Entry(frame_texto)
        entry_desc.pack()

        #Testo do valor
        label_valor = ttk.Label(frame_texto,
                               text="Valor",
                               font=("Perpetua, 15"))
        label_valor.pack()

        #Caixa de texto do valor
        entry_valor = ttk.Entry(frame_texto)
        entry_valor.pack()

        #Testo da categoria
        label_categ = ttk.Label(frame_texto,
                               text="Categoria",
                               font=("Perpetua, 15"))
        label_categ.pack()

        #Caixa de texto da descrição
        entry_categ = ttk.Entry(frame_texto)
        entry_categ.pack()

        #Testo da descrição
        label_data = ttk.Label(frame_texto,
                               text="Data",
                               font=("Perpetua, 15"))
        label_data.pack()

        #Caixa de texto da descrição
        entry_data = ttk.Entry(frame_texto)
        entry_data.pack()

        #Frame pra deixar os botão um do lado do outro
        frame_botao = ttk.Frame(frame_texto)
        frame_botao.pack(pady=10)

        #Botão para adicionar os itens na treeview
        botao_add = ttk.Button(frame_botao,
                           text="ADICIONAR",
                           style="success")
        botao_add.pack(side="left", pady=15, padx=5)

        #Botão para excluix os itens na treeview
        botao_exc = ttk.Button(frame_botao,
                           text="EXCLUIR",
                           style="danger")
        botao_exc.pack(side="left", pady=15, padx=5)

        #Botão para atualizar os itens na treeview
        botao_atl = ttk.Button(frame_botao,
                           text="ATUALIZAR",
                           style="warning")#secondary
        botao_atl.pack(side="right", pady=15, padx=5)




        def adicionar(self):
            pass
            






    



    def run(self):
        self.janela.mainloop()

if __name__ == "__main__":
    pag = Despesas()
    pag.run()
