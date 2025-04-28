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
    
    # Saída (Consequente) com maior precisão
    desempenho = ctrl.Consequent(np.arange(0, 100.1, 0.1), 'desempenho')
    
    # === Funções de pertinência otimizadas para NOTAS ===
    nota['insuficiente'] = fuzz.trapmf(nota.universe, [0, 0, 3, 5])
    nota['regular'] = fuzz.trimf(nota.universe, [3, 5, 7])
    nota['bom'] = fuzz.trimf(nota.universe, [5, 7, 9])
    nota['excelente'] = fuzz.trapmf(nota.universe, [7, 9, 10, 10])
    
    # === Funções de pertinência otimizadas para FREQUÊNCIA ===
    frequencia['baixa'] = fuzz.trapmf(frequencia.universe, [0, 0, 50, 70])
    frequencia['media'] = fuzz.trimf(frequencia.universe, [50, 75, 85])
    frequencia['alta'] = fuzz.trapmf(frequencia.universe, [75, 90, 100, 100])
    
    # === Funções de pertinência otimizadas para PARTICIPAÇÃO ===
    participacao['baixa'] = fuzz.trapmf(participacao.universe, [0, 0, 3, 5])
    participacao['media'] = fuzz.trimf(participacao.universe, [3, 5, 7]) 
    participacao['alta'] = fuzz.trapmf(participacao.universe, [5, 7, 10, 10])
    
    # === Funções de pertinência otimizadas para HABILIDADES SOCIOEMOCIONAIS ===
    socioemocional['baixa'] = fuzz.trapmf(socioemocional.universe, [0, 0, 3, 5])
    socioemocional['media'] = fuzz.trimf(socioemocional.universe, [3, 5, 7])
    socioemocional['alta'] = fuzz.trapmf(socioemocional.universe, [5, 7, 10, 10])
    
    # === Funções de pertinência otimizadas para CONTEXTO SOCIOECONÔMICO ===
    # Quanto menor o valor, mais desafiador é o contexto
    contexto['desafiador'] = fuzz.trapmf(contexto.universe, [0, 0, 4, 6])
    contexto['moderado'] = fuzz.trapmf(contexto.universe, [4, 6, 7, 9])
    contexto['favoravel'] = fuzz.trapmf(contexto.universe, [7, 9, 10, 10])
    
    # === Funções de pertinência otimizadas para MOTIVAÇÃO ===
    motivacao['baixa'] = fuzz.trapmf(motivacao.universe, [0, 0, 3, 5])
    motivacao['media'] = fuzz.trimf(motivacao.universe, [3, 5, 7])
    motivacao['alta'] = fuzz.trapmf(motivacao.universe, [5, 7, 10, 10])
    
    # === Funções de pertinência otimizadas para DESEMPENHO (saída) ===
    # Usando combinação de trapezoidais e gaussianas para transição mais suave
    desempenho['insuficiente'] = fuzz.trapmf(desempenho.universe, [0, 0, 30, 45])
    desempenho['regular_com_dificuldades'] = fuzz.gaussmf(desempenho.universe, 40, 7)
    desempenho['regular_com_potencial'] = fuzz.gaussmf(desempenho.universe, 55, 7)
    desempenho['bom_com_superacao'] = fuzz.gaussmf(desempenho.universe, 70, 7)
    desempenho['excelente_com_equilibrio'] = fuzz.trapmf(desempenho.universe, [75, 90, 100, 100])
    
    # === Regras fuzzy otimizadas ===
    regras = []
    
    # Regras para alunos com bom desempenho acadêmico
    regras.append(ctrl.Rule(nota['excelente'] & frequencia['alta'], 
                           desempenho['excelente_com_equilibrio']))
    
    regras.append(ctrl.Rule(nota['bom'] & frequencia['alta'] & participacao['alta'], 
                           desempenho['bom_com_superacao']))
    
    # Regras para superação de contexto desafiador
    regras.append(ctrl.Rule(nota['bom'] & contexto['desafiador'] & motivacao['alta'], 
                           desempenho['excelente_com_equilibrio']))
    
    regras.append(ctrl.Rule(nota['regular'] & contexto['desafiador'] & motivacao['alta'], 
                           desempenho['bom_com_superacao']))
    
    # Regras que valorizam o desenvolvimento socioemocional
    regras.append(ctrl.Rule(socioemocional['alta'] & participacao['alta'] & (nota['regular'] | nota['bom']), 
                           desempenho['bom_com_superacao']))
    
    # Regras para alunos com dificuldades
    regras.append(ctrl.Rule(nota['insuficiente'] & frequencia['baixa'], 
                           desempenho['insuficiente']))
    
    regras.append(ctrl.Rule(nota['insuficiente'] & motivacao['baixa'], 
                           desempenho['insuficiente']))
    
    # Regras para motivação e participação
    regras.append(ctrl.Rule(motivacao['alta'] & participacao['alta'] & nota['regular'], 
                           desempenho['regular_com_potencial']))
    
    # Regras para frequência baixa
    regras.append(ctrl.Rule(frequencia['baixa'] & ~motivacao['alta'], 
                           desempenho['regular_com_dificuldades']))
    
    # Regra para valorizar melhoria e progresso
    regras.append(ctrl.Rule(
        (nota['regular'] & motivacao['alta'] & participacao['alta']),
        desempenho['regular_com_potencial']))
    
    # Regra para reconhecer excelência contextualizada
    regras.append(ctrl.Rule(
        (nota['bom'] & contexto['desafiador'] & socioemocional['alta']),
        desempenho['excelente_com_equilibrio']))
    
    # Regra para todos os parâmetros excelentes
    regras.append(ctrl.Rule(
        (nota['excelente'] & frequencia['alta'] & participacao['alta'] &
        socioemocional['alta'] & motivacao['alta']),
        desempenho['excelente_com_equilibrio']))
    
    # Regra para todos os parâmetros baixos
    regras.append(ctrl.Rule(
        (nota['insuficiente'] & frequencia['baixa'] & participacao['baixa'] &
        socioemocional['baixa'] & motivacao['baixa']),
        desempenho['insuficiente']))
    
    # Regra para equilíbrio entre fatores acadêmicos e socioemocionais
    regras.append(ctrl.Rule(
        (nota['bom'] & socioemocional['alta'] & participacao['alta']),
        desempenho['excelente_com_equilibrio']))
    
    # === Sistema de controle ===
    sistema_ctrl = ctrl.ControlSystem(regras)
    
    return sistema_ctrl, desempenho