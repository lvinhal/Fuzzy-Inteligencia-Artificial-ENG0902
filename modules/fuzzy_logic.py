import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def configurar_sistema_fuzzy():
    """
    Configura o sistema fuzzy com funções de pertinência otimizadas para cada variável
    
    Returns:
        tuple: (sistema_controle, variável_desempenho)
    """
    # === Definição das variáveis de entrada com precisão aumentada ===
    nota = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'nota')
    frequencia = ctrl.Antecedent(np.arange(0, 100.1, 0.1), 'frequencia')
    participacao = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'participacao')
    socioemocional = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'socioemocional')
    contexto = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'contexto')
    motivacao = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'motivacao')
    
    # Saída (Consequente) com maior precisão - Utilizando método do bisector para defuzzificação
    desempenho = ctrl.Consequent(np.arange(0, 100.1, 0.1), 'desempenho', defuzzify_method='centroid')
    
    # === Funções de pertinência para NOTAS ===
    # Definindo manualmente para melhor controle dos valores extremos
    nota['insuficiente'] = fuzz.trapmf(nota.universe, [0, 0, 3, 5])
    nota['regular'] = fuzz.trimf(nota.universe, [3, 5, 7])
    nota['bom'] = fuzz.trimf(nota.universe, [5, 7, 9])
    nota['excelente'] = fuzz.trapmf(nota.universe, [7, 9, 10, 10])
    
    # === Funções de pertinência para FREQUÊNCIA ===
    frequencia['baixa'] = fuzz.trapmf(frequencia.universe, [0, 0, 50, 70])
    frequencia['media'] = fuzz.trimf(frequencia.universe, [50, 75, 90])
    frequencia['alta'] = fuzz.trapmf(frequencia.universe, [75, 95, 100, 100])
    
    # === Funções de pertinência para PARTICIPAÇÃO ===
    participacao['baixa'] = fuzz.trapmf(participacao.universe, [0, 0, 3, 5])
    participacao['media'] = fuzz.trimf(participacao.universe, [3, 5, 7]) 
    participacao['alta'] = fuzz.trapmf(participacao.universe, [5, 7, 10, 10])
    
    # === Funções de pertinência para HABILIDADES SOCIOEMOCIONAIS ===
    socioemocional['baixa'] = fuzz.trapmf(socioemocional.universe, [0, 0, 3, 5])
    socioemocional['media'] = fuzz.trimf(socioemocional.universe, [3, 5, 7])
    socioemocional['alta'] = fuzz.trapmf(socioemocional.universe, [5, 7, 10, 10])
    
    # === Funções de pertinência para CONTEXTO SOCIOECONÔMICO ===
    # Quanto menor o valor, mais desafiador é o contexto
    contexto['desafiador'] = fuzz.trapmf(contexto.universe, [0, 0, 3, 5])
    contexto['moderado'] = fuzz.trimf(contexto.universe, [3, 5, 7])
    contexto['favoravel'] = fuzz.trapmf(contexto.universe, [5, 7, 10, 10])
    
    # === Funções de pertinência para MOTIVAÇÃO ===
    # Modificado para usar os mesmos intervalos das outras variáveis
    motivacao['baixa'] = fuzz.trapmf(motivacao.universe, [0, 0, 3, 5])
    motivacao['media'] = fuzz.trimf(motivacao.universe, [3, 5, 7])
    motivacao['alta'] = fuzz.trapmf(motivacao.universe, [5, 7, 10, 10])
    
    # === Funções de pertinência para DESEMPENHO (saída) ===
    # Modificado para garantir que 100 tenha pertinência total à categoria máxima
    desempenho['insuficiente'] = fuzz.trapmf(desempenho.universe, [0, 0, 20, 35])
    desempenho['regular_com_dificuldades'] = fuzz.trapmf(desempenho.universe, [25, 35, 45, 55])
    desempenho['regular_com_potencial'] = fuzz.trapmf(desempenho.universe, [45, 55, 65, 75])
    desempenho['bom_com_superacao'] = fuzz.trapmf(desempenho.universe, [65, 75, 85, 95])
    # Função de pertinência modificada para concentrar a "massa" em 100
    desempenho['excelente_com_equilibrio'] = fuzz.trapmf(desempenho.universe, [85, 97, 100, 100])
    
    # === Regras fuzzy expandidas (55 regras) ===
    regras = []
    
    # === GRUPO 1: REGRAS PARA NOTAS E FREQUÊNCIA (12 regras) ===
    
    # Combinações de notas excelentes com diferentes frequências
    regras.append(ctrl.Rule(nota['excelente'] & frequencia['alta'], 
                           desempenho['excelente_com_equilibrio']))
    
    regras.append(ctrl.Rule(nota['excelente'] & frequencia['media'], 
                           desempenho['bom_com_superacao']))
    
    regras.append(ctrl.Rule(nota['excelente'] & frequencia['baixa'], 
                           desempenho['regular_com_potencial']))
    
    # Combinações de notas boas com diferentes frequências
    regras.append(ctrl.Rule(nota['bom'] & frequencia['alta'], 
                           desempenho['bom_com_superacao']))
    
    regras.append(ctrl.Rule(nota['bom'] & frequencia['media'], 
                           desempenho['bom_com_superacao']))
    
    regras.append(ctrl.Rule(nota['bom'] & frequencia['baixa'], 
                           desempenho['regular_com_potencial']))
    
    # Combinações de notas regulares com diferentes frequências
    regras.append(ctrl.Rule(nota['regular'] & frequencia['alta'], 
                           desempenho['regular_com_potencial']))
    
    regras.append(ctrl.Rule(nota['regular'] & frequencia['media'], 
                           desempenho['regular_com_dificuldades']))
    
    regras.append(ctrl.Rule(nota['regular'] & frequencia['baixa'], 
                           desempenho['regular_com_dificuldades']))
    
    # Combinações de notas insuficientes com diferentes frequências
    regras.append(ctrl.Rule(nota['insuficiente'] & frequencia['alta'], 
                           desempenho['regular_com_dificuldades']))
    
    regras.append(ctrl.Rule(nota['insuficiente'] & frequencia['media'], 
                           desempenho['insuficiente']))
    
    regras.append(ctrl.Rule(nota['insuficiente'] & frequencia['baixa'], 
                           desempenho['insuficiente']))
    
    # === GRUPO 2: REGRAS PARA MOTIVAÇÃO (12 regras) ===
    
    # Impacto de diferentes níveis de motivação em notas excelentes
    regras.append(ctrl.Rule(nota['excelente'] & motivacao['alta'], 
                           desempenho['excelente_com_equilibrio']))
    
    regras.append(ctrl.Rule(nota['excelente'] & motivacao['media'], 
                           desempenho['bom_com_superacao']))
    
    regras.append(ctrl.Rule(nota['excelente'] & motivacao['baixa'], 
                           desempenho['bom_com_superacao']))
    
    # Impacto de diferentes níveis de motivação em notas boas
    regras.append(ctrl.Rule(nota['bom'] & motivacao['alta'], 
                           desempenho['bom_com_superacao']))
    
    regras.append(ctrl.Rule(nota['bom'] & motivacao['media'], 
                           desempenho['bom_com_superacao']))
    
    regras.append(ctrl.Rule(nota['bom'] & motivacao['baixa'], 
                           desempenho['regular_com_potencial']))
    
    # Impacto de diferentes níveis de motivação em notas regulares
    regras.append(ctrl.Rule(nota['regular'] & motivacao['alta'], 
                           desempenho['regular_com_potencial']))
    
    regras.append(ctrl.Rule(nota['regular'] & motivacao['media'], 
                           desempenho['regular_com_potencial']))
    
    regras.append(ctrl.Rule(nota['regular'] & motivacao['baixa'], 
                           desempenho['regular_com_dificuldades']))
    
    # Impacto de diferentes níveis de motivação em notas insuficientes
    regras.append(ctrl.Rule(nota['insuficiente'] & motivacao['alta'], 
                           desempenho['regular_com_dificuldades']))
    
    regras.append(ctrl.Rule(nota['insuficiente'] & motivacao['media'], 
                           desempenho['insuficiente']))
    
    regras.append(ctrl.Rule(nota['insuficiente'] & motivacao['baixa'], 
                           desempenho['insuficiente']))
    
    # === GRUPO 3: REGRAS PARA PARTICIPAÇÃO (8 regras) ===
    
    # Diferentes níveis de participação com outras variáveis
    regras.append(ctrl.Rule(participacao['alta'] & nota['bom'] & frequencia['media'], 
                           desempenho['bom_com_superacao']))
    
    regras.append(ctrl.Rule(participacao['alta'] & nota['regular'] & frequencia['alta'], 
                           desempenho['regular_com_potencial']))
    
    regras.append(ctrl.Rule(participacao['alta'] & motivacao['alta'] & nota['regular'], 
                           desempenho['bom_com_superacao']))
    
    regras.append(ctrl.Rule(participacao['alta'] & motivacao['baixa'] & nota['bom'], 
                           desempenho['regular_com_potencial']))
    
    regras.append(ctrl.Rule(participacao['baixa'] & nota['bom'] & motivacao['alta'], 
                           desempenho['regular_com_potencial']))
    
    regras.append(ctrl.Rule(participacao['baixa'] & nota['bom'] & motivacao['media'], 
                           desempenho['regular_com_dificuldades']))
    
    regras.append(ctrl.Rule(participacao['baixa'] & nota['regular'] & motivacao['media'], 
                           desempenho['regular_com_dificuldades']))
    
    regras.append(ctrl.Rule(participacao['baixa'] & nota['regular'] & motivacao['baixa'], 
                           desempenho['insuficiente']))
    
    # === GRUPO 4: REGRAS PARA CONTEXTO SOCIOECONÔMICO (6 regras) ===
    
    # Regras para superação de contexto desafiador
    regras.append(ctrl.Rule(contexto['desafiador'] & nota['bom'] & motivacao['alta'], 
                           desempenho['excelente_com_equilibrio']))
    
    regras.append(ctrl.Rule(contexto['desafiador'] & nota['regular'] & motivacao['alta'], 
                           desempenho['bom_com_superacao']))
    
    regras.append(ctrl.Rule(contexto['desafiador'] & nota['insuficiente'] & motivacao['alta'] & participacao['alta'], 
                           desempenho['regular_com_potencial']))
    
    # Regras para contexto moderado
    regras.append(ctrl.Rule(contexto['moderado'] & nota['bom'] & motivacao['media'], 
                           desempenho['bom_com_superacao']))
    
    # Regras para contexto favorável
    regras.append(ctrl.Rule(contexto['favoravel'] & nota['regular'] & motivacao['baixa'], 
                           desempenho['regular_com_dificuldades']))
    
    regras.append(ctrl.Rule(contexto['favoravel'] & nota['excelente'] & motivacao['alta'], 
                           desempenho['excelente_com_equilibrio']))
    
    # === GRUPO 5: REGRAS PARA HABILIDADES SOCIOEMOCIONAIS (6 regras) ===
    
    # Regras com diferentes níveis de habilidades socioemocionais
    regras.append(ctrl.Rule(socioemocional['alta'] & nota['regular'] & motivacao['media'], 
                           desempenho['regular_com_potencial']))
    
    regras.append(ctrl.Rule(socioemocional['alta'] & nota['bom'] & participacao['alta'], 
                           desempenho['bom_com_superacao']))
    
    regras.append(ctrl.Rule(socioemocional['baixa'] & participacao['alta'] & (nota['regular'] | nota['bom']), 
                           desempenho['bom_com_superacao']))
    
    regras.append(ctrl.Rule(socioemocional['baixa'] & nota['regular'] & participacao['baixa'], 
                           desempenho['regular_com_dificuldades']))
    
    regras.append(ctrl.Rule(socioemocional['media'] & nota['bom'] & motivacao['media'], 
                           desempenho['bom_com_superacao']))
    
    regras.append(ctrl.Rule(socioemocional['media'] & nota['regular'] & motivacao['baixa'], 
                           desempenho['regular_com_dificuldades']))
    
    # === GRUPO 6: REGRAS COMBINANDO MÚLTIPLOS FATORES (6 regras) ===
    
    # Combinações complexas de fatores
    regras.append(ctrl.Rule(nota['bom'] & frequencia['alta'] & participacao['alta'] & motivacao['alta'], 
                           desempenho['excelente_com_equilibrio']))
    
    regras.append(ctrl.Rule(nota['regular'] & frequencia['alta'] & participacao['alta'] & motivacao['alta'], 
                           desempenho['bom_com_superacao']))
    
    regras.append(ctrl.Rule(nota['regular'] & frequencia['media'] & participacao['media'] & motivacao['media'], 
                           desempenho['regular_com_potencial']))
    
    regras.append(ctrl.Rule(nota['regular'] & frequencia['baixa'] & participacao['baixa'] & motivacao['baixa'], 
                           desempenho['insuficiente']))
    
    regras.append(ctrl.Rule(nota['bom'] & frequencia['media'] & participacao['baixa'] & motivacao['baixa'], 
                           desempenho['regular_com_dificuldades']))
    
    regras.append(ctrl.Rule(nota['insuficiente'] & frequencia['alta'] & participacao['alta'] & motivacao['alta'], 
                           desempenho['regular_com_potencial']))
    
    # === GRUPO 7: CENÁRIOS EXTREMOS E CASOS ESPECIAIS (5 regras) ===
    
    # Todos os parâmetros máximos - Regra especial com peso duplo para garantir 100%
    regra_maxima = ctrl.Rule(
        (nota['excelente'] & frequencia['alta'] & participacao['alta'] &
        socioemocional['alta'] & motivacao['alta'] & contexto['favoravel']),
        desempenho['excelente_com_equilibrio'])
    regra_maxima.weight = 2.0  # Atribuir peso duplo para esta regra
    regras.append(regra_maxima)
    
    # Todos os parâmetros mínimos
    regras.append(ctrl.Rule(
        (nota['insuficiente'] & frequencia['baixa'] & participacao['baixa'] &
        socioemocional['baixa'] & motivacao['baixa']),
        desempenho['insuficiente']))
    
    # Desempenho acadêmico bom com contexto desafiador
    regras.append(ctrl.Rule(
        (nota['bom'] & contexto['desafiador'] & socioemocional['alta']),
        desempenho['excelente_com_equilibrio']))
    
    # Alta motivação e participação com nota regular
    regras.append(ctrl.Rule(
        (nota['regular'] & motivacao['alta'] & participacao['alta']),
        desempenho['regular_com_potencial']))
    
    # Frequência baixa mas alto esforço
    regras.append(ctrl.Rule(
        (frequencia['baixa'] & participacao['alta'] & motivacao['alta'] & nota['regular']),
        desempenho['regular_com_potencial']))
    
    # === Sistema de controle ===
    sistema_ctrl = ctrl.ControlSystem(regras)
    
    return sistema_ctrl, desempenho