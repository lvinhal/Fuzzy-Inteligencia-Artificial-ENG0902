import pandas as pd
import os
from tkinter import messagebox

def salvar_historico(dados):
    """
    Salva os dados do aluno no histórico CSV
    
    Args:
        dados (dict): Dicionário com dados do aluno e resultado da avaliação
    """
    arquivo_csv = "historico_alunos_fuzzy.csv"
    
    # Preparar o registro
    registro = {
        "Matricula": dados.get('matrícula', ''),
        "Nome": dados.get('nome_do_aluno', ''),
        "Nota_Teoria1": dados.get('nota_da_primeira_avaliação_teórica', 0),
        "Nota_Teoria2": dados.get('nota_da_segunda_avaliação_teórica', 0),
        "Nota_Pratica": dados.get('nota_da_avaliação_prática', 0),
        "Nota_Grupo": dados.get('nota_da_avaliação_em_grupo', 0),
        "Frequencia": dados.get('frequência', 0),
        "Participacao": dados.get('participação', 0),
        "Socioemocional": dados.get('habilidades_socioemocionais', 0),
        "Contexto": dados.get('contexto_socioeconômico', 0),
        "Motivacao": dados.get('motivação', 0),
        "Motivacao_Cat": dados.get('motivacao_valor', ''),
        "Desempenho": dados.get('desempenho', 0),
        "Classificacao": dados.get('classificacao', '')
    }
    
    # Verificar se o arquivo existe
    if os.path.exists(arquivo_csv):
        df = pd.read_csv(arquivo_csv)
        df = pd.concat([df, pd.DataFrame([registro])], ignore_index=True)
    else:
        df = pd.DataFrame([registro])
    
    # Salvar o arquivo
    df.to_csv(arquivo_csv, index=False)

def carregar_historico_para_treeview():
    """
    Carrega o histórico do arquivo CSV para exibição no treeview
    
    Returns:
        list: Lista com os registros formatados para o treeview
    """
    arquivo_csv = "historico_alunos_fuzzy.csv"
    
    # Verificar se o arquivo existe
    if not os.path.exists(arquivo_csv):
        messagebox.showinfo("Informação", "Não há histórico de avaliações disponível.")
        return []
    
    # Carregar o arquivo
    try:
        df = pd.read_csv(arquivo_csv)
        registros = []
        
        # Converter cada linha para um formato compatível com treeview
        for i, row in df.iterrows():
            registro = [
                str(row.get('Matricula', '')),
                str(row.get('Nome', '')),
                str(row.get('Nota_Teoria1', 0)),
                str(row.get('Nota_Teoria2', 0)),
                str(row.get('Nota_Pratica', 0)),
                str(row.get('Nota_Grupo', 0)),
                str(row.get('Frequencia', 0)),
                str(row.get('Participacao', 0)),
                str(row.get('Socioemocional', 0)),
                str(row.get('Contexto', 0)),
                str(row.get('Motivacao', 0)),
                str(row.get('Motivacao_Cat', '')),  
                str(row.get('Desempenho', 0)),
                str(row.get('Classificacao', ''))
            ]
            registros.append(registro)
        
        return registros
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar o histórico: {str(e)}")
        return []