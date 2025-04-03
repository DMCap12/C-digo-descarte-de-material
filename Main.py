import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pandas as pd
import os
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk

class PesaDeDescarte:
    def __init__(self, root):
        self.root = root
        self.root.title("Pesagem de Descarte")
        self.root.geometry("1280x800")
        self.root.configure(bg="")
        self.material_selecionado = None

        # Carregar a imagem de fundo
        self.bg_image = Image.open("fundo.png")  # Substitua pelo caminho da sua imagem
        self.bg_image = self.bg_image.resize((1280, 800), Image.LANCZOS)  # Redimensiona se necessário
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Criar um label para o fundo
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  # Faz a imagem cobrir toda a tela

        # Tela Principal
        self.frame = tk.Frame(root, bg="", bd=1)
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
        tk.Label(self.frame, text="Selecione o material para descarte", font=("Arial", 12)).grid(row=0, column=1)
        lista_de_materiais = ["PPS-FORTRON (5.516.115.902)", "PPS-RYTON (5.516.119.404)", "POLIOXIMETILENO (5.515.286.901)", "POM - CELCON (5.515.264.418)", "POM - CELCON PRETO (5.515.264.427)", "POM (5.515.253.021)", "POM HOSTAFORM (5.515.264.023)", "POM HOSTAFORM AMARELO (5.515.264.406)", "GRANULADO PBT ULTRADOR (5.515.753.419)"]

        self.lb_materiais = tk.Listbox(self.frame, width=50, height=10)
        for material in lista_de_materiais:
            self.lb_materiais.insert(tk.END, material)
        self.lb_materiais.grid(row=1, column=1, pady=10)

        # Botão confirmação escolha
        self.botao_confirmar_selecao_material = tk.Button(
            self.frame, text="Confirmar Material", command=self.confirmar_material,width=30, height=3, font=("Arial", 12)
        )
        self.botao_confirmar_selecao_material.grid(row=2, column=1, pady=30)

        # Pesar
        tk.Label(self.frame, text="Digite o peso do material em gramas", font=("Arial", 12)).grid(row=3, column=0)
        self.entrada_peso = tk.Entry(self.frame, width=30)
        self.entrada_peso.grid(row=3, column=2)

        # Botão confirmação Peso
        self.botao_confirmar_peso = tk.Button(
            self.frame, text="Confirmar Peso", command=self.confirmar_peso, width=30, height=3, font=("Arial", 12)
        )
        self.botao_confirmar_peso.grid(row=4, column=1, pady=30)

        # Botão Validar
        self.botao_validar = tk.Button(
            self.frame, text="Validar medição", command=self.validar_medicao, width=30, height=3, font=("Arial", 12)
        )
        self.botao_validar.grid(row=7, column=1, pady=30)

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
            messagebox.showinfo("Peso", f"{peso}g adicionado")

    def validar_medicao(self):
        if self.material_selecionado is None:
            ("Erro de ordem", "Insira o material antes de prosseguir e logo em seguida o peso")
        elif self.entrada_peso is None:
            ("Erro de ordem", "Insira o peso antes de prosseguir")
        else:


            if self.material_selecionado is None or not self.entrada_peso.get().strip():
                messagebox.showerror("Erro", "Preencha todos os campos antes de validar.")
                return

            resposta = messagebox.askyesno(
                "Confirmar validação",
                f"Confirmar o descarte de {self.entrada_peso.get().strip()}g do material {self.material_selecionado}?"
            )

            if resposta:
                hora_no_momento = datetime.now().strftime('%Y-%m-%d %H:%M')
                peso = self.entrada_peso.get().strip() + "g"

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
