import sys
import argparse
from typing import Dict, List, Tuple, Optional


def cont_recursiva_simples(n: int) -> int:
    # caso base: se ja chegamos a 1, nao precisamos de mais operacoes
    if n == 1:
        return 0 
    
    min_ops = 1 + cont_recursiva_simples(n - 1) # chama a funcao recursivamente para n-1
    
    # verificar se podemos dividir por 2
    if n % 2 == 0: # se n for par, tenta a operacao de divisao por 2
        # compara com a opcao de decrementar
        min_ops = min(min_ops, 1 + cont_recursiva_simples(n // 2)) # chama a funcao recursivamente para n//2
    
    # verificar se podemos dividir por 3
    if n % 3 == 0: # se n for divisivel por 3, tenta a operacao de divisao por 3
        # compara com as opcoes anteriores (decrementar e dividir por 2)
        min_ops = min(min_ops, 1 + cont_recursiva_simples(n // 3))
    
    # retorna o menor numero de operacoes encontrado
    return min_ops


def cont_com_memo(n: int, memo: Optional[Dict[int, int]] = None) -> int:
    # inicializar o dicionario de memoizacao se nao foi fornecido
    if memo is None:
        memo = {}
    
    # verifica se ja foi calculado o resultado para este valor de n
    # se sim, retorna o valor armazenado (evita recalcular)
    if n in memo: # se n ja esta no dicionario
        return memo[n] # retorna o valor armazenado
    
    # caso base 
    # se ja chegamos a 1 nao é preciso de mais operações
    if n == 1: # se n for 1
        memo[n] = 0  # armazena o resultado no dicionario para uso futuro
        return 0 # retorna 0
    
    #decrementar o numero para n-1 para encontrar o menor numero de operacoes possivel
    min_ops = 1 + cont_com_memo(n - 1, memo) # chama a funcao recursivamente para n-1
    
    # verificar se podemos dividir por 2
    #se n for par tenta a operacao de divisao por 2
    if n % 2 == 0: # se n for par 
        # compara com a opcao de decrementar
        min_ops = min(min_ops, 1 + cont_com_memo(n // 2, memo)) # chama a funcao recursivamente para n//2
    
    #verifica se podemos dividir por 3
    # se n for divisivel por 3, tenta a operacao de divisao por 3
    if n % 3 == 0: # se n for divisivel por 3
        # compara com as opcoes anteriores (decrementar e dividir por 2)
        min_ops = min(min_ops, 1 + cont_com_memo(n // 3, memo)) # chama a funcao recursivamente para n//3
    
    # armazena o resultado calculado no dicionario para uso futuro
    memo[n] = min_ops # armazena o resultado no dicionario para uso futuro
    return min_ops # retorna o resultado calculado


def cont_bottomUp(n: int) -> Tuple[int, Optional[List[str]]]: # metodo bottom-up dp 
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
        prev[x] = x - 1  # oestado anterior e x-1
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
    seq = []
    current = n  # comeca do valor inicial
    
    # enquanto nao chegamos ao estado final (1)
    while current != 1:
        # adiciona a operacao usada para chegar ao estado current
        seq.append(op[current])
        # retrocede para o estado anterior
        current = prev[current]
    
    # retorna o numero minimo de operacoes e a sequencia otima
    return dp[n], seq


def validar_seq(n: int, seq: List[str]) -> bool: # valida se a sequencia de operacoes leva ao resultado correto 
    val = n # comeca com o valor inicial n
    
    # aplica cada operacao da sequencia sobre o valor atual
    for op in seq:
        if op == '-1':
            val -= 1 # decrementa o valor em 1
        elif op == '/2': # operacao de divisao por 2
            # operacao de divisao por 2
            if val % 2 != 0: # se valor nao e par 
                # se valor nao e par, a operacao nao e valida
                return False 
            val //= 2  # divide o valor por 2
        elif op == '/3':
            # operacao de divisao por 3: verifica se valor e divisivel por 3
            if val % 3 != 0:
                # se valor nao e divisivel por 3, a operacao nao e valida
                return False
            val //= 3  # divide o valor por 3
    
    # verifica se o valor final e realmente 1
    return val == 1


def main(): # funcao principal que implementa a interface de linha de comando    
    #processa os argumentos da linha de comando, valida a entrada,
    #executa o metodo escolhido e exibe os resultados.
    
    parser = argparse.ArgumentParser( # cria o parser de argumentos
        description='contagem regressiva nasa - encontra o menor numero de operacoes para reduzir n ate 1'
    ) 
    
    # argumento obrigatorio (numero inteiro positivo para reduzir ate 1) 
    parser.add_argument('n', type=int, help='numero inteiro positivo para reduzir ate 1')
    
    # argumento opcional (metodo a ser usado)
    parser.add_argument(
        '--method',  # metodo a ser usado
        choices=['rec', 'memo', 'dp'],  # escolhas de metodos
        default='dp',  # metodo padrao
        help='metodo a ser usado: rec (recursivo), memo (com memoizacao), dp (bottom-up)' 
    )
    
    # argumento opcional (mostrar sequencia de operacoes)
    parser.add_argument(
        '--path', 
        action='store_true',
        help='mostrar a sequencia otima de operacoes'
    )
    
    # processa os argumentos da linha de comando (valida a entrada)
    args = parser.parse_args()
    
    # validacoes de entrada (numero inteiro positivo para reduzir ate 1)
    if args.n <= 0: # se n for menor ou igual a 0
        print("erro: n deve ser um inteiro positivo", file=sys.stderr) #mensagem de erro
        sys.exit(1)
    
    # executar metodo escolhido (rec, memo, dp, bfs)
    try:
        if args.method == 'rec': # metodo recursivo simples
            # metodo recursivo simples - limitado para numeros pequenos
            if args.n > 20:  # limitar para evitar stack overflow
                print("aviso: n muito grande para metodo recursivo simples. use --method memo ou dp")
                sys.exit(1)
            passos = cont_recursiva_simples(args.n)
            seq = None  # este metodo nao retorna sequencia
            
        elif args.method == 'memo': # metodo recursivo com memoria
            # metodo recursivo com memo
            passos = cont_com_memo(args.n) # chama a funcao recursiva com memoria
            seq = None  # este metodo nao retorna sequencia
            
        elif args.method == 'dp':
            # metodo bottom-up dp (recomendado)
            passos, seq = cont_bottomUp(args.n)
            
        
        print(f"numero de passos minimos: {passos}") # mostra o numero minimo de passos
        
        # mostrar sequencia se solicitado e disponivel
        if args.path and seq is not None: # se a sequencia for solicitada e disponivel
            print(f"sequencia de operacoes: {' '.join(seq)}") # mostra a sequencia de operacoes
            
            if validar_seq(args.n, seq): # valida a sequencia 
                print("sequencia validada com sucesso")
            else:
                print("erro na validacao da sequencia", file=sys.stderr) # mensagem de erro
                
        elif args.path and seq is None: # se a sequencia for solicitada e nao disponivel
            # para metodos que nao retornam sequencia por padrao, calcular usando dp
            _, seq = cont_bottomUp(args.n) 
            print(f"operacoes: {' '.join(seq)}")
            
            # validar sequencia para garantir que esta correta
            if validar_seq(args.n, seq): 
                print("sequencia validada com sucesso")
            else:
                print("erro na validacao da sequencia", file=sys.stderr) # mensagem de erro
                
    except RecursionError: 
        # captura erro de stack overflow em metodos recursivos para evitar stack overflow
        print("erro: stack overflow. use um metodo nao-recursivo (--method dp ou bfs)", file=sys.stderr)
        sys.exit(1)
    except Exception as e: # captura outros erros inesperados
        print(f"erro inesperado: {e}", file=sys.stderr) # mensagem de erro
        sys.exit(1)

if __name__ == '__main__':
    main()