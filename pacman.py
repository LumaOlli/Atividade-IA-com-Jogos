import heapq
import time

# --- 1. MODELAGEM DO AMBIENTE (LABIRINTO) ---

# W = Parede (1), Caminho Livre (0)
# S = Início (0,0), O = Objetivo (2,2)
LABIRINTO_3X3 = [
    [0, 0, 0],  # Linha 0
    [0, 1, 0],  # Linha 1 (Parede em [1,1])
    [0, 0, 0]   # Linha 2
]

# Definições do Problema
INICIO = (0, 0)
OBJETIVO = (2, 2)
DIMENSAO_X = len(LABIRINTO_3X3)
DIMENSAO_Y = len(LABIRINTO_3X3[0])

# Movimentos possíveis (Direita, Esquerda, Baixo, Cima)
MOVIMENTOS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
CUSTO_PASSO = 1  # Custo uniforme para cada movimento

# --- 2. IMPLEMENTAÇÃO DO ALGORITMO UCS ---

def busca_custo_uniforme(labirinto, inicio, objetivo):
    # Fila de Prioridade: (custo_acumulado, nó, caminho_percorrido)
    # UCS é sinônimo de Dijkstra com objetivo único.
    fronteira = [(0, inicio, [inicio])] 
    
    # Dicionário para armazenar o menor custo conhecido até cada nó
    # Essencial para otimalidade do UCS (evita revisitar caminhos mais caros)
    custos = {inicio: 0}
    
    # Conjunto para rastrear nós visitados (para contagem de eficiência)
    nos_expandidos = 0

    while fronteira:
        # Extrai o nó com o menor custo acumulado (g_n)
        g_n, atual, caminho = heapq.heappop(fronteira)
        
        # O nó foi removido da fronteira e será expandido
        nos_expandidos += 1

        # Verificação do Objetivo
        if atual == objetivo:
            return caminho, g_n, nos_expandidos

        # Funções Sucessoras
        x, y = atual
        
        for dx, dy in MOVIMENTOS:
            proximo_x, proximo_y = x + dx, y + dy
            proximo_estado = (proximo_x, proximo_y)

            # 1. Checa se está dentro dos limites do labirinto
            if 0 <= proximo_x < DIMENSAO_X and 0 <= proximo_y < DIMENSAO_Y:
                
                # 2. Checa se não é parede (LABIRINTO_3X3[x, y] == 1)
                if labirinto[proximo_x][proximo_y] == 0:
                    
                    # Novo custo acumulado
                    novo_custo = g_n + CUSTO_PASSO

                    # 3. Princípio de Otimalidade do UCS: 
                    # Só atualiza/adiciona se o novo caminho for mais barato (ou se for o primeiro caminho)
                    if proximo_estado not in custos or novo_custo < custos[proximo_estado]:
                        custos[proximo_estado] = novo_custo
                        novo_caminho = caminho + [proximo_estado]
                        
                        # Adiciona à fila de prioridade para futura expansão
                        heapq.heappush(fronteira, (novo_custo, proximo_estado, novo_caminho))

    return None, 0, nos_expandidos # Solução não encontrada

# --- 3. EXECUÇÃO E COMPARAÇÃO DE DESEMPENHO ---

if __name__ == "__main__":
    
    print("--- Simulação: Busca de Custo Uniforme (UCS) ---")
    print(f"Jogo: Pac-Man Simplificado ({DIMENSAO_X}x{DIMENSAO_Y})")
    print(f"Início: {INICIO} | Objetivo: {OBJETIVO}")
    
    start_time = time.time()
    caminho, custo_total, nos_expandidos = busca_custo_uniforme(LABIRINTO_3X3, INICIO, OBJETIVO)
    end_time = time.time()
    
    if caminho:
        print("\nRESULTADOS DO DESEMPENHO:")
        print(f"Caminho Ótimo Encontrado (Nós): {caminho}")
        print(f"Custo Total da Solução (Passos): {custo_total}")
        print(f"Nós Expandidos (Métrica de Eficiência): {nos_expandidos}")
        print(f"Tempo de Execução: {round((end_time - start_time) * 1000, 4)} ms")
    else:
        print("\nSolução não encontrada.")