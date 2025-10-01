#!/usr/bin/env python3
"""
contagem regressiva - nasa
programa para determinar o menor numero de operacoes para reduzir n ate 1
usando operacoes: -1, /2 (se divisivel), /3 (se divisivel)

o problema consiste em encontrar o menor numero de operacoes para reduzir
um numero inteiro positivo n ate 1, usando apenas tres operacoes:
- decremento de uma unidade (-1)
- divisao por 2 (/2) - apenas quando n e divisivel por 2
- divisao por 3 (/3) - apenas quando n e divisivel por 3

o programa implementa quatro metodos diferentes para resolver o problema:
1. recursao simples (apenas para validacao em numeros pequenos)
2. recursao com memoizacao (evita recomputacoes)
3. programacao dinamica bottom-up (metodo recomendado)
4. busca em largura bfs (alternativa elegante)
"""

import sys
import argparse
from typing import Dict, List, Tuple, Optional


def contagem_recursiva_simples(n: int) -> int:
    """
    versao 1: recursiva simples (baseline)
    implementa a recorrencia literalmente para validar a logica.
    
    esta funcao e uma implementacao direta da recorrencia:
    f(1) = 0
    f(n) = 1 + min(f(n-1), f(n/2) se n%2==0, f(n/3) se n%3==0)
    
    complexidade: exponencial o(3^n) - muito lenta para numeros grandes
    uso: apenas para validacao em numeros pequenos (n <= 20)
    
    parametros:
        n (int): numero inteiro positivo a ser reduzido ate 1
    
    retorna:
        int: numero minimo de operacoes necessarias
    """
    # caso base: se ja chegamos a 1, nao precisamos de mais operacoes
    if n == 1:
        return 0
    
    # sempre podemos decrementar o numero
    # calcula recursivamente o numero de operacoes para n-1
    min_ops = 1 + contagem_recursiva_simples(n - 1)
    
    # verificar se podemos dividir por 2
    # se n for par, tenta a operacao de divisao por 2
    if n % 2 == 0:
        # compara com a opcao de decrementar
        min_ops = min(min_ops, 1 + contagem_recursiva_simples(n // 2))
    
    # verificar se podemos dividir por 3
    # se n for divisivel por 3, tenta a operacao de divisao por 3
    if n % 3 == 0:
        # compara com as opcoes anteriores (decrementar e dividir por 2)
        min_ops = min(min_ops, 1 + contagem_recursiva_simples(n // 3))
    
    # retorna o menor numero de operacoes encontrado
    return min_ops


def contagem_com_memoizacao(n: int, memo: Optional[Dict[int, int]] = None) -> int:
    """
    versao 2: recursiva com memoizacao (top-down dp)
    usa um dicionario para evitar recomputacoes desnecessarias.
    
    esta funcao implementa a mesma logica da versao recursiva simples,
    mas com uma otimizacao importante: armazena os resultados ja calculados
    em um dicionario (memo) para evitar recalcular os mesmos valores.
    
    complexidade: o(n) tempo e o(n) espaco
    vantagem: mantem a simplicidade da recursao mas com performance otimizada
    
    parametros:
        n (int): numero inteiro positivo a ser reduzido ate 1
        memo (dict): dicionario para armazenar resultados ja calculados
    
    retorna:
        int: numero minimo de operacoes necessarias
    """
    # inicializar o dicionario de memoizacao se nao foi fornecido
    if memo is None:
        memo = {}
    
    # verificar se ja calculamos o resultado para este valor de n
    # se sim, retorna o valor armazenado (evita recalcular)
    if n in memo:
        return memo[n]
    
    # caso base: se ja chegamos a 1, nao precisamos de mais operacoes
    if n == 1:
        memo[n] = 0  # armazena o resultado no dicionario
        return 0
    
    # sempre podemos decrementar o numero
    # calcula recursivamente o numero de operacoes para n-1
    min_ops = 1 + contagem_com_memoizacao(n - 1, memo)
    
    # verificar se podemos dividir por 2
    # se n for par, tenta a operacao de divisao por 2
    if n % 2 == 0:
        # compara com a opcao de decrementar
        min_ops = min(min_ops, 1 + contagem_com_memoizacao(n // 2, memo))
    
    # verificar se podemos dividir por 3
    # se n for divisivel por 3, tenta a operacao de divisao por 3
    if n % 3 == 0:
        # compara com as opcoes anteriores (decrementar e dividir por 2)
        min_ops = min(min_ops, 1 + contagem_com_memoizacao(n // 3, memo))
    
    # armazena o resultado calculado no dicionario para uso futuro
    memo[n] = min_ops
    return min_ops


def contagem_bottom_up(n: int) -> Tuple[int, Optional[List[str]]]:
    """
    versao 3: nao-recursiva (bottom-up dp)
    constroi a solucao de baixo para cima usando programacao dinamica.
    
    esta funcao implementa a abordagem bottom-up da programacao dinamica,
    calculando os valores menores primeiro e usando-os para calcular os maiores.
    tambem constroi a sequencia otima de operacoes para chegar ao resultado.
    
    complexidade: o(n) tempo e o(n) espaco
    vantagem: nao usa recursao, evita problemas de stack overflow
    
    parametros:
        n (int): numero inteiro positivo a ser reduzido ate 1
    
    retorna:
        tuple: (numero minimo de operacoes, sequencia otima de operacoes)
    """
    # caso especial: se n ja e 1, nao precisamos de operacoes
    if n == 1:
        return 0, []
    
    # dp[i] = numero minimo de operacoes para chegar de i ate 1
    # inicializa o array com zeros
    dp = [0] * (n + 1)
    
    # prev[i] = estado anterior que levou ao estado otimo i
    # usado para reconstruir o caminho otimo
    prev = [0] * (n + 1)
    
    # op[i] = operacao usada para chegar ao estado i
    # armazena a operacao que foi aplicada para chegar ao estado atual
    op = [''] * (n + 1)
    
    # preenche o array dp de baixo para cima
    # comeca em 2 porque dp[1] ja e 0 (caso base)
    for x in range(2, n + 1):
        # inicializa com a operacao de decremento (sempre possivel)
        dp[x] = 1 + dp[x - 1]
        prev[x] = x - 1  # o estado anterior e x-1
        op[x] = '-1'     # a operacao usada foi decrementar
        
        # verificar se podemos dividir por 2
        # se x for par e a divisao por 2 resultar em menos operacoes
        if x % 2 == 0 and 1 + dp[x // 2] < dp[x]:
            dp[x] = 1 + dp[x // 2]  # atualiza o numero minimo de operacoes
            prev[x] = x // 2        # o estado anterior e x//2
            op[x] = '/2'            # a operacao usada foi dividir por 2
        
        # verificar se podemos dividir por 3
        # se x for divisivel por 3 e a divisao por 3 resultar em menos operacoes
        if x % 3 == 0 and 1 + dp[x // 3] < dp[x]:
            dp[x] = 1 + dp[x // 3]  # atualiza o numero minimo de operacoes
            prev[x] = x // 3        # o estado anterior e x//3
            op[x] = '/3'            # a operacao usada foi dividir por 3
    
    # construir a sequencia otima de operacoes
    # comeca do valor n e vai retrocedendo ate chegar a 1
    sequencia = []
    current = n  # comeca do valor inicial
    
    # enquanto nao chegamos ao estado final (1)
    while current != 1:
        # adiciona a operacao usada para chegar ao estado current
        sequencia.append(op[current])
        # retrocede para o estado anterior
        current = prev[current]
    
    # retorna o numero minimo de operacoes e a sequencia otima
    return dp[n], sequencia


def contagem_bfs(n: int) -> Tuple[int, List[str]]:
    """
    versao alternativa: bfs (busca em largura)
    modela o problema como um grafo e usa bfs para encontrar o caminho minimo.
    
    esta funcao implementa uma abordagem diferente ao problema, modelando-o
    como um grafo onde cada numero e um no e as operacoes sao arestas.
    usa busca em largura (bfs) para encontrar o caminho mais curto de n ate 1.
    
    complexidade: o(n) tempo e o(n) espaco
    vantagem: encontra naturalmente o caminho minimo, implementacao elegante
    
    parametros:
        n (int): numero inteiro positivo a ser reduzido ate 1
    
    retorna:
        tuple: (numero minimo de operacoes, sequencia de operacoes)
    """
    # caso especial: se n ja e 1, nao precisamos de operacoes
    if n == 1:
        return 0, []
    
    # importa deque para implementar uma fila eficiente
    from collections import deque
    
    # fila de bfs: cada elemento e uma tupla (valor_atual, operacoes_realizadas)
    # comeca com o valor inicial n e uma lista vazia de operacoes
    fila = deque([(n, [])])
    
    # conjunto de valores ja visitados para evitar ciclos
    visitados = {n}
    
    # executa a busca em largura
    while fila:
        # remove o primeiro elemento da fila (fifo)
        valor, operacoes = fila.popleft()
        
        # verificar se chegamos ao objetivo (valor 1)
        if valor == 1:
            # retorna o numero de operacoes e a sequencia
            return len(operacoes), operacoes
        
        # tentar todas as operacoes possiveis a partir do valor atual
        proximos = []
        
        # operacao de decremento (sempre possivel se valor > 1)
        if valor > 1:
            proximos.append((valor - 1, operacoes + ['-1']))
        
        # operacao de divisao por 2 (apenas se valor for par)
        if valor % 2 == 0:
            proximos.append((valor // 2, operacoes + ['/2']))
        
        # operacao de divisao por 3 (apenas se valor for divisivel por 3)
        if valor % 3 == 0:
            proximos.append((valor // 3, operacoes + ['/3']))
        
        # adicionar a fila apenas valores nao visitados
        # isso garante que nao processamos o mesmo valor duas vezes
        for novo_valor, novas_ops in proximos:
            if novo_valor not in visitados:
                visitados.add(novo_valor)  # marca como visitado
                fila.append((novo_valor, novas_ops))  # adiciona a fila
    
    # nao deveria chegar aqui para n > 0
    # pois sempre e possivel chegar a 1 usando apenas decrementos
    return -1, []


def validar_sequencia(n: int, sequencia: List[str]) -> bool:
    """
    valida se uma sequencia de operacoes realmente leva de n ate 1.
    
    esta funcao simula a aplicacao das operacoes da sequencia sobre o valor n
    e verifica se o resultado final e realmente 1. tambem valida se as
    operacoes de divisao sao aplicadas apenas quando o valor e divisivel.
    
    parametros:
        n (int): valor inicial
        sequencia (list): lista de operacoes a serem aplicadas
    
    retorna:
        bool: true se a sequencia e valida, false caso contrario
    """
    # comeca com o valor inicial n
    valor = n
    
    # aplica cada operacao da sequencia sobre o valor atual
    for op in sequencia:
        if op == '-1':
            # operacao de decremento: subtrai 1 do valor
            valor -= 1
        elif op == '/2':
            # operacao de divisao por 2: verifica se valor e par
            if valor % 2 != 0:
                # se valor nao e par, a operacao nao e valida
                return False
            valor //= 2  # divide o valor por 2
        elif op == '/3':
            # operacao de divisao por 3: verifica se valor e divisivel por 3
            if valor % 3 != 0:
                # se valor nao e divisivel por 3, a operacao nao e valida
                return False
            valor //= 3  # divide o valor por 3
    
    # verifica se o valor final e realmente 1
    return valor == 1


def main():
    """
    funcao principal que implementa a interface de linha de comando.
    
    processa os argumentos da linha de comando, valida a entrada,
    executa o metodo escolhido e exibe os resultados.
    """
    # configura o parser de argumentos da linha de comando
    parser = argparse.ArgumentParser(
        description='contagem regressiva nasa - encontra o menor numero de operacoes para reduzir n ate 1'
    )
    
    # argumento obrigatorio: numero inteiro positivo
    parser.add_argument('n', type=int, help='numero inteiro positivo para reduzir ate 1')
    
    # argumento opcional: metodo a ser usado
    parser.add_argument(
        '--method', 
        choices=['rec', 'memo', 'dp', 'bfs'], 
        default='dp',
        help='metodo a ser usado: rec (recursivo), memo (com memoizacao), dp (bottom-up), bfs (busca em largura)'
    )
    
    # argumento opcional: mostrar sequencia de operacoes
    parser.add_argument(
        '--path', 
        action='store_true',
        help='mostrar a sequencia otima de operacoes'
    )
    
    # processa os argumentos da linha de comando
    args = parser.parse_args()
    
    # validacoes de entrada
    if args.n <= 0:
        print("erro: n deve ser um inteiro positivo", file=sys.stderr)
        sys.exit(1)
    
    # executar metodo escolhido
    try:
        if args.method == 'rec':
            # metodo recursivo simples - limitado para numeros pequenos
            if args.n > 20:  # limitar para evitar stack overflow
                print("aviso: n muito grande para metodo recursivo simples. use --method memo ou dp")
                sys.exit(1)
            passos = contagem_recursiva_simples(args.n)
            sequencia = None  # este metodo nao retorna sequencia
            
        elif args.method == 'memo':
            # metodo recursivo com memoizacao
            passos = contagem_com_memoizacao(args.n)
            sequencia = None  # este metodo nao retorna sequencia
            
        elif args.method == 'dp':
            # metodo bottom-up dp (recomendado)
            passos, sequencia = contagem_bottom_up(args.n)
            
        elif args.method == 'bfs':
            # metodo bfs (busca em largura)
            passos, sequencia = contagem_bfs(args.n)
        
        # mostrar resultado principal
        print(f"passos minimos: {passos}")
        
        # mostrar sequencia se solicitado e disponivel
        if args.path and sequencia is not None:
            print(f"operacoes: {' '.join(sequencia)}")
            
            # validar sequencia para garantir que esta correta
            if validar_sequencia(args.n, sequencia):
                print("sequencia validada com sucesso!")
            else:
                print("erro na validacao da sequencia!", file=sys.stderr)
                
        elif args.path and sequencia is None:
            # para metodos que nao retornam sequencia por padrao, calcular usando dp
            _, sequencia = contagem_bottom_up(args.n)
            print(f"operacoes: {' '.join(sequencia)}")
            
            # validar sequencia para garantir que esta correta
            if validar_sequencia(args.n, sequencia):
                print("sequencia validada com sucesso!")
            else:
                print("erro na validacao da sequencia!", file=sys.stderr)
                
    except RecursionError:
        # captura erro de stack overflow em metodos recursivos
        print("erro: stack overflow. use um metodo nao-recursivo (--method dp ou bfs)", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # captura outros erros inesperados
        print(f"erro inesperado: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
