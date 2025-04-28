import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import skfuzzy as fuzz

from modules.fuzzy_logic import configurar_sistema_fuzzy
from modules.compatibilidade import ajustar_nota
from modules.historico import salvar_historico, carregar_historico_para_treeview
from modules.analise import adicionar_analise_personalizada

class AvaliacaoFuzzyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Avaliação Fuzzy de Alunos")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        # Criar notebook (abas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Aba de entrada de dados
        self.tab_entrada = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_entrada, text="Entrada de Dados")
        
        # Aba de resultados
        self.tab_resultados = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_resultados, text="Resultados")
        
        # Aba de histórico
        self.tab_historico = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_historico, text="Histórico")
        
        # Configurar a entrada de dados
        self.configurar_entrada_dados()
        
        # Configurar a área de resultados
        self.configurar_resultados()
        
        # Configurar a área de histórico
        self.configurar_historico()
        
        # Configurar o sistema fuzzy
        self.sistema_ctrl, self.desempenho = configurar_sistema_fuzzy()
    
    def configurar_entrada_dados(self):
        # Frame para os dados do aluno
        frame_dados = ttk.LabelFrame(self.tab_entrada, text="Dados do Aluno")
        frame_dados.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Labels e entradas
        labels = [
            "Matrícula", "Nome do Aluno", 
            "Nota da Primeira Avaliação Teórica (0-10)", "Nota da Segunda Avaliação Teórica (0-10)",
            "Nota da Avaliação Prática (0-10)", "Nota da Avaliação em Grupo (0-10)",
            "Frequência (0-100%)", "Participação (0-10)",
            "Habilidades Socioemocionais (0-10)", "Contexto Socioeconômico (0-10)"
        ]
        
        self.entries = {}
        
        # Função de validação para entradas numéricas
        def validar_entrada(texto, tipo):
            if not texto:  # Permite campo vazio
                return True
                
            try:
                valor = float(texto)
                if tipo == "frequencia":
                    return 0 <= valor <= 100
                else:  # notas e outros
                    return 0 <= valor <= 10
            except ValueError:
                return False
                
        # Registrar validação para cada tipo
        validar_nota = self.root.register(lambda texto: validar_entrada(texto, "nota"))
        validar_frequencia = self.root.register(lambda texto: validar_entrada(texto, "frequencia"))
        
        for i, label in enumerate(labels):
            ttk.Label(frame_dados, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            
            # Determinar qual validação usar
            field_name = label.split("(")[0].strip().lower().replace(" ", "_")
            
            # Criar entrada com validação apropriada
            entry = ttk.Entry(frame_dados, width=30)
            
            # Aplicar a validação apropriada
            if "frequência" in field_name:
                entry.configure(validate="key", validatecommand=(validar_frequencia, "%P"))
            elif field_name not in ["matrícula", "nome_do_aluno"]:
                entry.configure(validate="key", validatecommand=(validar_nota, "%P"))
                
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            self.entries[field_name] = entry
        
        # Adicionar combobox para Motivação
        ttk.Label(frame_dados, text="Motivação").grid(row=len(labels), column=0, padx=10, pady=5, sticky="e")
        self.motivacao = ttk.Combobox(frame_dados, values=["Alta", "Média", "Baixa"])
        self.motivacao.grid(row=len(labels), column=1, padx=10, pady=5, sticky="w")
        
        # Adicionar comboboxes para perfil e método
        ttk.Label(frame_dados, text="Perfil do Aluno").grid(row=len(labels)+1, column=0, padx=10, pady=5, sticky="e")
        self.perfil_aluno = ttk.Combobox(frame_dados, values=["Visual", "Auditivo", "Cinestésico"])
        self.perfil_aluno.grid(row=len(labels)+1, column=1, padx=10, pady=5, sticky="w")
        
        ttk.Label(frame_dados, text="Método de Ensino").grid(row=len(labels)+2, column=0, padx=10, pady=5, sticky="e")
        self.metodo_ensino = ttk.Combobox(frame_dados, values=["Visual", "Auditivo", "Cinestésico"])
        self.metodo_ensino.grid(row=len(labels)+2, column=1, padx=10, pady=5, sticky="w")
    
    def configurar_resultados(self):
        # Área de resultados
        frame_resultados = ttk.LabelFrame(self.tab_resultados, text="Resultados da Avaliação")
        frame_resultados.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Área para texto de resultados
        self.resultado_texto = tk.Text(frame_resultados, height=10, width=80)
        self.resultado_texto.pack(padx=10, pady=10)
        
        # Área para gráfico
        self.frame_grafico = ttk.Frame(frame_resultados)
        self.frame_grafico.pack(fill="both", expand=True, padx=10, pady=10)
    
    def configurar_historico(self):
        # Frame para o histórico
        frame_historico = ttk.Frame(self.tab_historico)
        frame_historico.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Treeview para exibir o histórico
        colunas = ["Matricula", "Nome", "Nota T1", "Nota T2", "Nota P", "Nota G", "Frequencia", 
                   "Participacao", "Socioemocional", "Contexto", "Motivacao", "Motivacao_Cat", 
                   "Desempenho", "Classificacao"]
        
        self.treeview = ttk.Treeview(frame_historico, columns=colunas, show="headings")
        
        # Configurar cabeçalhos
        for col in colunas:
            exibir = col.replace("_", " ").title()
            self.treeview.heading(col, text=exibir)
            self.treeview.column(col, width=80)
        
        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(frame_historico, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        
        self.treeview.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botões
        frame_botoes = ttk.Frame(self.tab_entrada)
        frame_botoes.pack(fill="x", padx=10, pady=10)
        frame_botoes.configure(style='TFrame')  # Se estiver usando ttk

        ttk.Button(frame_botoes, text="Avaliar Aluno", command=self.avaliar_aluno).pack(side="left", padx=5)
        ttk.Button(frame_botoes, text="Limpar Campos", command=self.limpar_campos).pack(side="left", padx=5)

        # Botão para carregar histórico
        ttk.Button(self.tab_historico, text="Carregar Histórico", 
                  command=self.carregar_historico).pack(pady=10)
    
    def avaliar_aluno(self):
        try:
            # Obter dados dos campos
            dados = {}
            for campo, entry in self.entries.items():
                valor = entry.get().strip()
                if campo not in ["matrícula", "nome_do_aluno"]:
                    if not valor:
                        messagebox.showerror("Erro", f"O campo {campo} não pode estar vazio.")
                        return
                    try:
                        valor_numerico = float(valor)
                        
                        # Verificar se o valor está no intervalo permitido
                        if campo == "frequência":
                            if valor_numerico < 0 or valor_numerico > 100:
                                messagebox.showerror("Erro", f"O valor do campo {campo} deve estar entre 0 e 100.")
                                return
                        else:  # Para outros campos numéricos
                            if valor_numerico < 0 or valor_numerico > 10:
                                messagebox.showerror("Erro", f"O valor do campo {campo} deve estar entre 0 e 10.")
                                return
                                
                        dados[campo] = valor_numerico
                    except ValueError:
                        messagebox.showerror("Erro", f"O valor '{valor}' no campo {campo} não é um número válido.")
                        return
                else:
                    dados[campo] = valor
            
            # Validar matrícula e nome
            if not dados.get("matrícula"):
                messagebox.showerror("Erro", "A matrícula do aluno é obrigatória.")
                return
                
            if not dados.get("nome_do_aluno"):
                messagebox.showerror("Erro", "O nome do aluno é obrigatório.")
                return
            
            # Obter motivação
            motivacao_valor = self.motivacao.get()
            if not motivacao_valor:
                messagebox.showerror("Erro", "O campo Motivação não pode estar vazio.")
                return
                
            # Converter motivação para valor numérico para o sistema fuzzy
            motivacao_numerica = {"Alta": 9.0, "Média": 5.0, "Baixa": 2.0}.get(motivacao_valor, 5.0)
            dados['motivação'] = motivacao_numerica
            dados['motivacao_valor'] = motivacao_valor  # Guardar a versão texto também
            
            # Obter perfil e método de ensino
            perfil_aluno = self.perfil_aluno.get()
            metodo_ensino = self.metodo_ensino.get()
            
            # Verificar se perfil e método foram selecionados
            if not perfil_aluno or not metodo_ensino:
                messagebox.showerror("Erro", "Perfil do aluno e método de ensino são obrigatórios.")
                return
            
            # Calcular média das notas para usar no sistema fuzzy
            nota_media = (dados.get('nota_da_primeira_avaliação_teórica', 0) + 
                        dados.get('nota_da_segunda_avaliação_teórica', 0) + 
                        dados.get('nota_da_avaliação_prática', 0) + 
                        dados.get('nota_da_avaliação_em_grupo', 0)) / 4
            dados['nota'] = nota_media
            
            # Ajustar nota baseado na compatibilidade
            nota_ajustada = ajustar_nota(nota_media, perfil_aluno, metodo_ensino)
            
            # Instanciar o sistema de controle fuzzy
            from skfuzzy import control as ctrl
            sistema = ctrl.ControlSystemSimulation(self.sistema_ctrl)
            
            # Definir entradas do sistema com a nota ajustada
            sistema.input['nota'] = nota_ajustada
            sistema.input['frequencia'] = dados.get('frequência', 0)
            sistema.input['participacao'] = dados.get('participação', 0)
            sistema.input['socioemocional'] = dados.get('habilidades_socioemocionais', 0)
            sistema.input['contexto'] = dados.get('contexto_socioeconômico', 0)
            sistema.input['motivacao'] = dados.get('motivação', 0)

            # Calcular resultado
            sistema.compute()
            
            # Obter o resultado
            resultado = sistema.output['desempenho']
            
            # Verificação para notas máximas
            todas_maximas = (
                nota_ajustada >= 9.5 and
                dados.get('frequência', 0) >= 95 and
                dados.get('participação', 0) >= 9.5 and
                dados.get('habilidades_socioemocionais', 0) >= 9.5 and
                dados.get('contexto_socioeconômico', 0) >= 9.5 and
                dados.get('motivação', 0) >= 9.5
            )
            
            if todas_maximas:
                resultado = 100  # Forçar resultado 100 quando todas as notas são máximas
            
            # Classificar o resultado com categorias atualizadas
            if resultado < 30:
                classificacao = "Insuficiente"
            elif resultado < 45:
                classificacao = "Regular com dificuldades"
            elif resultado < 60:
                classificacao = "Regular com potencial"
            elif resultado < 75:
                classificacao = "Bom com superação"
            else:
                classificacao = "Excelente com equilíbrio"
            
            # Exibir resultado
            self.resultado_texto.delete(1.0, tk.END)
            self.resultado_texto.insert(tk.END, f"Aluno: {dados.get('nome_do_aluno')}\n")
            self.resultado_texto.insert(tk.END, f"Matrícula: {dados.get('matrícula')}\n\n")
            
            # Mostrar ajuste de compatibilidade
            self.resultado_texto.insert(tk.END, 
            f"Compatibilidade: {perfil_aluno} (aluno) × {metodo_ensino} (método)\n"
            f"Nota média das avaliações: {nota_media:.1f} → Nota ajustada: {nota_ajustada:.1f}\n\n")
            
            self.resultado_texto.insert(tk.END, f"Resultado da avaliação fuzzy: {resultado:.2f}/100\n")
            self.resultado_texto.insert(tk.END, f"Classificação: {classificacao}\n\n")
            
            # Adicionar análise personalizada
            adicionar_analise_personalizada(self.resultado_texto, dados, resultado, classificacao)
            
            # Exibir gráfico
            self.exibir_grafico(sistema)
            
            # Salvar no histórico (incluindo perfil e método)
            dados_historico = {
                **dados,
                'perfil_aluno': perfil_aluno,
                'metodo_ensino': metodo_ensino,
                'nota_ajustada': nota_ajustada,
                'desempenho': resultado,
                'classificacao': classificacao
            }
            
            # Salvar histórico e adicionar ao treeview
            salvar_historico(dados_historico)
            self.adicionar_ao_treeview(dados_historico)
            
            # Alternar para a aba de resultados
            self.notebook.select(self.tab_resultados)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro durante a avaliação: {str(e)}")
    
    def exibir_grafico(self, sistema):
        """Exibe o gráfico do desempenho fuzzy com as funções de pertinência otimizadas"""
        # Limpar o frame de gráfico
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()
        
        # Criar a figura para o gráfico
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
        
        # === GRÁFICO 1: FUNÇÕES DE PERTINÊNCIA DA SAÍDA ===
        # Plotar as funções de pertinência para o desempenho
        x_desempenho = np.arange(0, 100.1, 0.1)
        
        # Utilizar as novas funções de pertinência
        y_insuficiente = fuzz.interp_membership(self.desempenho.universe, 
                                        self.desempenho['insuficiente'].mf, 
                                        x_desempenho)
        y_regular_dif = fuzz.interp_membership(self.desempenho.universe, 
                                        self.desempenho['regular_com_dificuldades'].mf, 
                                        x_desempenho)
        y_regular_pot = fuzz.interp_membership(self.desempenho.universe, 
                                        self.desempenho['regular_com_potencial'].mf, 
                                        x_desempenho)
        y_bom = fuzz.interp_membership(self.desempenho.universe, 
                                    self.desempenho['bom_com_superacao'].mf, 
                                    x_desempenho)
        y_excelente = fuzz.interp_membership(self.desempenho.universe, 
                                        self.desempenho['excelente_com_equilibrio'].mf, 
                                        x_desempenho)
        
        # Plotar as curvas com cores diferentes
        ax1.plot(x_desempenho, y_insuficiente, 'r', linewidth=2, label='Insuficiente')
        ax1.plot(x_desempenho, y_regular_dif, 'orange', linewidth=2, label='Regular com dificuldades')
        ax1.plot(x_desempenho, y_regular_pot, 'y', linewidth=2, label='Regular com potencial')
        ax1.plot(x_desempenho, y_bom, 'g', linewidth=2, label='Bom com superação')
        ax1.plot(x_desempenho, y_excelente, 'b', linewidth=2, label='Excelente com equilíbrio')
        
        # Marcar o resultado
        resultado = sistema.output['desempenho']
        ax1.axvline(x=resultado, color='k', linestyle='--', alpha=0.7, label=f'Resultado: {resultado:.1f}')
        
        # Configurar o gráfico
        ax1.set_title('Avaliação de Desempenho Fuzzy')
        ax1.set_xlabel('Nível de Desempenho')
        ax1.set_ylabel('Grau de Pertinência')
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=3)
        
        # === GRÁFICO 2: VISUALIZAÇÃO DO RESULTADO ===
        # Criar um gráfico de barras para mostrar o grau de pertinência do resultado em cada categoria
        categorias = ['Insuficiente', 'Regular com\ndificuldades', 'Regular com\npotencial', 'Bom com\nsuperação', 'Excelente com\nequilíbrio']
        
        # Calcular o grau de pertinência do resultado em cada categoria
        graus = [
            fuzz.interp_membership(self.desempenho.universe, self.desempenho['insuficiente'].mf, resultado),
            fuzz.interp_membership(self.desempenho.universe, self.desempenho['regular_com_dificuldades'].mf, resultado),
            fuzz.interp_membership(self.desempenho.universe, self.desempenho['regular_com_potencial'].mf, resultado),
            fuzz.interp_membership(self.desempenho.universe, self.desempenho['bom_com_superacao'].mf, resultado),
            fuzz.interp_membership(self.desempenho.universe, self.desempenho['excelente_com_equilibrio'].mf, resultado)
        ]
        
        cores = ['red', 'orange', 'yellow', 'green', 'blue']
        
        # Criar o gráfico de barras
        barras = ax2.bar(categorias, graus, color=cores, alpha=0.7)
        
        # Adicionar valores nas barras
        for i, barra in enumerate(barras):
            altura = barra.get_height()
            ax2.text(barra.get_x() + barra.get_width()/2., 
                    altura + 0.02, 
                    f'{graus[i]:.2f}', 
                    ha='center', va='bottom', 
                    fontweight='bold')
        
        # Configurar o gráfico
        ax2.set_title(f'Grau de Pertinência do Resultado ({resultado:.1f}) em Cada Categoria')
        ax2.set_ylabel('Grau de Pertinência')
        ax2.set_ylim(0, 1.1)  # Para dar espaço para os textos
        ax2.grid(True, linestyle='--', alpha=0.3, axis='y')
        
        # Ajuste de layout e exibição
        fig.tight_layout(pad=3.0)
        
        # Adicionar o gráfico à interface
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def adicionar_ao_treeview(self, dados):
        """Adiciona um registro ao treeview"""
        # Usando apenas campos que existem nos dados
        valores = [
            dados.get('matrícula', ''),
            dados.get('nome_do_aluno', ''),
            str(dados.get('nota_da_primeira_avaliação_teórica', 0)),
            str(dados.get('nota_da_segunda_avaliação_teórica', 0)),
            str(dados.get('nota_da_avaliação_prática', 0)),
            str(dados.get('nota_da_avaliação_em_grupo', 0)),
            str(dados.get('frequência', 0)),
            str(dados.get('participação', 0)),
            str(dados.get('habilidades_socioemocionais', 0)),
            str(dados.get('contexto_socioeconômico', 0)),
            str(dados.get('motivação', 0)),
            dados.get('motivacao_valor', ''),
            str(dados.get('desempenho', 0)),
            dados.get('classificacao', '')
        ]
        self.treeview.insert('', 'end', values=valores)
    
    def carregar_historico(self):
        """Carrega o histórico do arquivo CSV para o treeview"""
        # Limpar o treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        # Carregar e exibir histórico
        try:
            registros = carregar_historico_para_treeview()
            for registro in registros:
                self.treeview.insert('', 'end', values=registro)
            
            messagebox.showinfo("Sucesso", f"Histórico carregado com {len(registros)} registros.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o histórico: {str(e)}")
    
    def limpar_campos(self):
        """Limpa todos os campos de entrada"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        
        # Limpar comboboxes
        self.motivacao.set('')
        self.perfil_aluno.set('')
        self.metodo_ensino.set('')