import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pandas as pd
import os
from tkinter import simpledialog, messagebox

class PesaDeDescarte:
    def __init__(self, root):
        self.root = root
        self.root.title("Pesagem de Descarte")
        self.root.geometry("800x600")
        self.root.configure(bg="white")
        self.material_selecionado = None

        # Tela Principal
        self.frame = tk.Frame(root, bg="white")
        self.frame.pack(pady=5)

        # Ativar modo tela cheia
        self.root.attributes('-fullscreen', True)

        self.root.bind("<F11>", lambda event: self.root.attributes("-fullscreen", True))

        # Permitir sair do fullscreen com senha ao pressionar Esc
        self.root.bind("<Escape>", self.verificar_senha)

    def verificar_senha(self, event):
        senha_correta = "AWE9CA"  # Defina a senha desejada
        senha_digitada = simpledialog.askstring("Senha", "Digite a senha para sair do fullscreen:", show="*")

        if senha_digitada == senha_correta:
            self.root.attributes("-fullscreen", False)
            messagebox.showinfo("Sucesso", "Modo fullscreen desativado!")
        else:
            messagebox.showerror("Erro", "Senha incorreta!")


        # Selecionar Material
        tk.Label(self.frame, text="Selecione o material para descarte").grid(row=0, column=1)
        lista_de_materiais = ["Material 1", "Material 2", "Material 3", "Material 4", "Material 5"]

        self.lb_materiais = tk.Listbox(self.frame, width=15, height=5)
        for material in lista_de_materiais:
            self.lb_materiais.insert(tk.END, material)
        self.lb_materiais.grid(row=1, column=1, pady=10)

        # Botão confirmação escolha
        self.botao_confirmar_selecao_material = tk.Button(
            self.frame, text="Confirmar Material", command=self.confirmar_material
        )
        self.botao_confirmar_selecao_material.grid(row=2, column=1, pady=10)

        # Pesar
        tk.Label(self.frame, text="Digite o peso do material").grid(row=3, column=0)
        self.entrada_peso = tk.Entry(self.frame, width=30)
        self.entrada_peso.grid(row=3, column=3)

        # Botão confirmação Peso
        self.botao_confirmar_peso = tk.Button(
            self.frame, text="Confirmar Peso", command=self.confirmar_peso
        )
        self.botao_confirmar_peso.grid(row=4, column=1, pady=10)

        # Botão Validar
        self.botao_validar = tk.Button(
            self.frame, text="Validar medição", command=self.validar_medicao
        )
        self.botao_validar.grid(row=7, column=1, pady=10)

    def confirmar_material(self):
        self.material_selecionado = self.lb_materiais.get(tk.ACTIVE)
        if self.material_selecionado:
            messagebox.showinfo("Material", f"{self.material_selecionado} adicionado")
        else:
            messagebox.showerror("Erro", "Selecione um material antes de confirmar.")

    def confirmar_peso(self):

        if self.material_selecionado is None:
            messagebox.showerror("Erro de ordem", "Insira o material antes do peso")

        else:
            peso = self.entrada_peso.get().strip()
            if not peso:
                messagebox.showerror("Erro", "Digite um peso válido.")
                return
            if self.material_selecionado is None:
                messagebox.showerror("Erro", "Selecione um material antes de inserir o peso.")
                return
            messagebox.showinfo("Peso", f"{peso}Kg adicionado")

    def validar_medicao(self):
        if self.material_selecionado is None or not self.entrada_peso.get().strip():
            messagebox.showerror("Erro", "Preencha todos os campos antes de validar.")
            return
        else:


            if self.material_selecionado is None or not self.entrada_peso.get().strip():
                messagebox.showerror("Erro", "Preencha todos os campos antes de validar.")
                return

            resposta = messagebox.askyesno(
                "Confirmar validação",
                f"Confirmar o descarte de {self.entrada_peso.get().strip()}Kg do material {self.material_selecionado}?"
            )

            if resposta:
                hora_no_momento = datetime.now().strftime('%Y-%m-%d %H:%M')
                peso = self.entrada_peso.get().strip() + "Kg"

                # Criando um DataFrame corretamente formatado
                df_novo = pd.DataFrame([[self.material_selecionado, peso, hora_no_momento]],
                                    columns=["Material", "Peso", "Data"])

                try:
                    # Carrega os dados antigos e adiciona os novos
                    df_antigo = pd.read_excel("Descarte.xlsx", sheet_name="Descarte", engine='openpyxl')
                    df_final = pd.concat([df_antigo, df_novo], ignore_index=True)

                    # Salva o novo arquivo sobrescrevendo o antigo
                    with pd.ExcelWriter("Descarte.xlsx", mode='w', engine='openpyxl') as writer:
                        df_final.to_excel(writer, sheet_name="Descarte", index=False)

                    messagebox.showinfo("Sucesso", "Registro salvo com sucesso!")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao salvar no Excel: {e}")

                print(df_novo)

                self.entrada_peso.delete(0, tk.END)
                self.material_selecionado = None
            else:
                self.entrada_peso.delete(0, tk.END)
                self.material_selecionado = None
                messagebox.showinfo("Registro cancelado", "O registro foi cancelado.")
if __name__ == "__main__":
    root = tk.Tk()
    app = PesaDeDescarte(root)
    root.mainloop()
