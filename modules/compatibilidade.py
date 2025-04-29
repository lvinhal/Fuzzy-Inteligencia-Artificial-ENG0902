# Matriz de dificuldade (quanto maior, mais compensação)
MATRIZ_DIFICULDADE = {
    'Visual': {'Visual': 0.0, 'Auditivo': 0.5, 'Cinestésico': 1.0},
    'Auditivo': {'Visual': 0.5, 'Auditivo': 0.0, 'Cinestésico': 1.0,},
    'Cinestésico': {'Visual': 1.0, 'Auditivo': 0.5, 'Cinestésico': 0.0}
}

PESO_AJUSTE = 0.12  # 12% de ajuste máximo

def ajustar_nota(nota_original, perfil_aluno, metodo_ensino):
    """
    Ajusta a nota baseada na incompatibilidade perfil-método
    
    Args:
        nota_original (float): Nota original do aluno
        perfil_aluno (str): Perfil de aprendizagem do aluno (Visual, Auditivo, Cinestésico)
        metodo_ensino (str): Método de ensino utilizado (Visual, Auditivo, Cinestésico)
        
    Returns:
        float: Nota ajustada considerando a compatibilidade
    """
    try:
        fator = MATRIZ_DIFICULDADE[perfil_aluno][metodo_ensino]
        nota_ajustada = nota_original * (1 + fator * PESO_AJUSTE)
        return min(nota_ajustada, 10.0)  # Limita em 10.0
    except KeyError:
        return nota_original  # Retorna sem ajuste se houver erro