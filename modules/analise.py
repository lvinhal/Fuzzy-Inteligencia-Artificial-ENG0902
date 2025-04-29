import tkinter as tk

def adicionar_analise_personalizada(resultado_texto, dados, resultado, classificacao):
    """
    Adiciona uma análise personalizada com base nos dados e no resultado
    
    Args:
        resultado_texto (tk.Text): Elemento de texto onde será adicionada a análise
        dados (dict): Dicionário com dados do aluno
        resultado (float): Resultado numérico da avaliação fuzzy
        classificacao (str): Classificação qualitativa do desempenho
    """
    analise = "Análise personalizada:\n"
    
    # Analisar notas
    nota_teoria1 = dados.get('nota_da_primeira_avaliação_teórica', 0)
    nota_teoria2 = dados.get('nota_da_segunda_avaliação_teórica', 0)
    nota_pratica = dados.get('nota_da_avaliação_prática', 0)
    nota_grupo = dados.get('nota_da_avaliação_em_grupo', 0)
    
    if nota_teoria1 < 5 and nota_teoria2 > 7:
        analise += "• O aluno mostrou evolução significativa entre as avaliações teóricas.\n"
    elif nota_teoria1 > 7 and nota_teoria2 < 5:
        analise += "• O aluno apresentou queda no rendimento nas avaliações teóricas.\n"
    
    if nota_pratica > 7 and (nota_teoria1 < 5 or nota_teoria2 < 5):
        analise += "• O aluno demonstra melhor desempenho prático que teórico.\n"
    elif nota_pratica < 5 and (nota_teoria1 > 7 or nota_teoria2 > 7):
        analise += "• O aluno demonstra melhor desempenho teórico que prático.\n"
        
    if nota_grupo > 7 and (nota_pratica < 5 or (nota_teoria1 + nota_teoria2)/2 < 5):
        analise += "• O aluno tem melhor desempenho em trabalhos colaborativos.\n"
    
    # Analisar nota vs. motivação
    motivacao = dados.get('motivação', 0)
    
    if nota_pratica < 5 and motivacao > 7:
        analise += "• O aluno demonstra alta motivação apesar do baixo desempenho prático.\n"
    elif nota_pratica > 7 and motivacao < 5:
        analise += "• O aluno tem bom desempenho prático com baixa motivação registrada.\n"
    elif nota_pratica > 7 and motivacao > 7:
        analise += "• Excelente combinação de desempenho prático e motivação.\n"
    
    # Analisar participação e frequência
    participacao = dados.get('participação', 0)
    frequencia = dados.get('frequência', 0)
    
    if frequencia < 60:
        analise += "• A baixa frequência pode estar prejudicando o desempenho geral do aluno.\n"
    if participacao < 5:
        analise += "• Aumentar a participação em aula poderia melhorar o envolvimento com o conteúdo.\n"
    
    # Analisar fatores contextuais
    contexto = dados.get('contexto_socioeconômico', 0)
    if contexto < 5 and resultado > 60:
        analise += "• O aluno demonstra capacidade de superação frente a desafios socioeconômicos.\n"
    
    # Analisar habilidades socioemocionais
    socioemocional = dados.get('habilidades_socioemocionais', 0)
    
    if socioemocional > 7:
        analise += "• Boas habilidades socioemocionais contribuem para o desempenho.\n"
    elif socioemocional < 5:
        analise += "• O desenvolvimento de habilidades socioemocionais pode beneficiar o aluno.\n"
    
    # Analisar perfil vs. método
    perfil_aluno = dados.get('perfil_aluno', '')
    metodo_ensino = dados.get('metodo_ensino', '')
    
    if perfil_aluno and metodo_ensino and perfil_aluno != metodo_ensino:
        analise += f"• O método de ensino {metodo_ensino} apresenta discrepância com o perfil de aprendizagem {perfil_aluno} do aluno.\n"
    
    # Adicionar recomendações com base na classificação atualizada
    analise += "\nRecomendações:\n"
    
    if classificacao == "Insuficiente":
        analise += "• Estabelecer metas específicas de curto prazo para melhorar frequência e participação.\n"
        analise += "• Criar plano de recuperação com foco nas áreas de maior dificuldade.\n"
        analise += "• Considerar adaptações no método de ensino para maior compatibilidade com o perfil do aluno.\n"
        analise += "• Realizar feedback mais frequente para acompanhar a evolução do aluno.\n"
        
    elif classificacao == "Regular com dificuldades":
        analise += "• Identificar fatores específicos que afetam a consistência do desempenho.\n"
        analise += "• Considerar tutoria ou apoio adicional para superar dificuldades pontuais.\n"
        analise += "• Verificar se o método de ensino está adequado ao perfil de aprendizagem.\n"
        analise += "• Propor atividades que alternem entre trabalho individual e em grupo.\n"
        
    elif classificacao == "Regular com potencial":
        analise += "• Reconhecer e incentivar áreas de maior aptidão do aluno.\n"
        analise += "• Propor atividades desafiadoras nas áreas onde demonstra maior facilidade.\n"
        analise += "• Considerar estratégias para aumentar a motivação e o engajamento.\n"
        analise += "• Estabelecer metas progressivas que estimulem o desenvolvimento.\n"
        
    elif classificacao == "Bom com superação":
        analise += "• Reconhecer e valorizar o esforço e a superação do aluno.\n"
        analise += "• Continuar estimulando o desenvolvimento das áreas de maior potencial.\n"
        analise += "• Incentivar a colaboração com outros alunos para compartilhar experiências.\n"
        analise += "• Propor desafios que integrem diferentes habilidades.\n"
        
    elif classificacao == "Excelente com equilíbrio":
        analise += "• Propor desafios adicionais para manter o engajamento e motivação.\n"
        analise += "• Considerar o aluno como potencial monitor ou apoio a outros estudantes.\n"
        analise += "• Incentivar o desenvolvimento de projetos pessoais relacionados ao conteúdo.\n"
        analise += "• Explorar possibilidades de participação em atividades extracurriculares.\n"
    
    resultado_texto.insert(tk.END, analise)