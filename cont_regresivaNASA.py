import sys
import argparse
from typing import Dict, List, Tuple, Optional
def cont_recursiva_simples(n: int) -> int:  #metodo recursivo simples 
    # caso base (se ja chegamos a 1, 
    # nao precisamos de mais operacoes)
    if n == 1:          # se n for 1 
        return 0 # retorna 0 
    operacoes_minimas = 1 + cont_recursiva_simples(n - 1)      #  chama a funcao recursivamente para n-1
    # verificar se podemos dividir por 2
    if n % 2 == 0: # se n for par, tenta a operacao de divisao por 2
                # compara com a opcao de decrementar
        operacoes_minimas = min(operacoes_minimas, 1 + cont_recursiva_simples(n // 2)) # chama a funcao recursivamente para n//2
    
    # verificar se podemos dividir por 3
    if n % 3 == 0: # se n for divisivel por 3, tenta a operacao de divisao por 3
        # compara com as opcoes anteriores (decrementar e dividir por 2)
        operacoes_minimas = min(operacoes_minimas, 1 + cont_recursiva_simples(n // 3)) # chama a funcao recursivamente para n//3
    
    return operacoes_minimas # retorna o menor numero de operacoes encontrado

def cont_com_memo(n: int, memoria: Optional[Dict[int, int]] = None) -> int: #metodo recursivo com memoria
    if memoria is None: #se o dic de memoria nao tenha sido inicializado
        memoria = {} #          inicializa o dicionario de memoizacao
        # verifica se ja foi calculado o resultado para este valor de n
    # se sim 
    # retorna o valor armazenado (evita recalcular)
    if n in memoria: # se n ja esta no dicionario de memoria 
        return memoria[n] # retorna o valor armazenado no dicionario de memoizacao

        # caso base 
    #      se ja chegamos a 1 nao é preciso de mais operações
    if n == 1: # se n for 1
        memoria[n] = 0  # armazena o resultado no dicionario para uso futuro
        return 0 # retorna 0
    
        #decrementar o numero para n-1 para encontrar o menor numero de operacoes possível
    operacoes_minimas = 1 + cont_com_memo(n - 1, memoria) # chama a funcao recursivamente para n-1
    
        # verificar se podemos dividir por 2
            #se n for par 
    # tenta a operacao de divisao por 2
    if n % 2 == 0: # se n for par 
        operacoes_minimas = min(operacoes_minimas, 1 + cont_com_memo(n // 2, memoria)) # chama a func recursivamente para n//2
    
         #verifica se podemos dividir por 3
        #  se n for divisivel por 3
    #    tenta a operacao de divisao por 3 
    if n % 3 == 0: # se n for divisivel por 3
        operacoes_minimas = min(operacoes_minimas, 1 + cont_com_memo(n // 3, memoria)) # chama a func recursivamente para n//3
    # armazena o resultado calculado no dicionario para uso futuro
    memoria[n] = operacoes_minimas # armazena o resultado no dicionario para uso futuro
    return operacoes_minimas # retorna o resultado calculado

def cont_bottomUp(n: int) -> Tuple[int, Optional[List[str]]]: # metodo bottom-up 
    # caso especial 
    # se n ja é 1 
    # nao precisamos de operacoes
    if n == 1: # se n for 1
        return 0, []        # retorna 0 e uma lista vazia
            # dp[i] = número min de operacoes para chegar de i até  1
    programacao_dinamica = [0] * (n + 1) # inicializa o array com zeros
            # prev[i] = estado anterior que levou ao estado otimo i
    # usado para reconstruir o caminho otimo
    estado_anterior = [0] * (n + 1)
    # op[i] = operacao usada para chegar ao estado i
            # armazena a operacao que foi aplicada para chegar ao estado atual
    operacao = [''] * (n + 1) 
        # preenche o array dp de baixo para cima
    # comeca em 2 porque dp[1] ja é 0 (caso base)
    for x in range(2, n + 1): #cada val de x de 2 a n
        # inicializa com a operacao de decremento
        programacao_dinamica[x] = 1 + programacao_dinamica[x - 1]#atualiza o nmr min de operacoes
        estado_anterior[x] = x - 1      #o estado anterior é x-1
        operacao[x] = '-1'             # a operacao usada foi decrementadaa
        # verificar se podeos dividir por 2
        # se x for par e a divisão por 2 resultar em menos operações
        if x % 2 == 0 and 1 + programacao_dinamica[x // 2] < programacao_dinamica[x]: 
            programacao_dinamica[x] = 1 + programacao_dinamica[x // 2]  # atualiza o numero min de operacoes
            estado_anterior[x] = x // 2 #o estado anterior e x//2
            operacao[x] = '/2'           # a operacao usada foi dividir por 2
        
        # verificar se podemos dividir por 3
        # se x for divisivel por 3 
        # e a divisao por 3 resultar em menos operacoes
        if x % 3 == 0 and 1 + programacao_dinamica[x // 3] < programacao_dinamica[x]:
            programacao_dinamica[x] = 1 + programacao_dinamica[x // 3]  #  atualiza o numero min de operacoes
            estado_anterior[x] = x // 3                #o estado anterior e x//3
            operacao[x] = '/3'         #a operacao usada foi dividir por 3
    
    # construir a sequencia otima de operacoes
    #comeca do val n e vai retrocedendo ate chegar a 1
    sequencia = []         # inicializa a lista vazia
    valor_atual = n  # comeca do valor inicial
    while valor_atual != 1:             # enquanto valor_atual nao for 1 (nao chegamos ao estado final (1))
        sequencia.append(operacao[valor_atual])             # adiciona a operacao usada para chegar ao estado valor_atual
        valor_atual = estado_anterior[valor_atual] # retrocede para o estado anterior
    return programacao_dinamica[n], sequencia        #   retorna o numero min de operacoes e a sequencia otima

def validar_seq(n: int, sequencia: List[str]) -> bool: # valida se a sequencia de operacoes leva ao resultado correto 
    valor = n # comeca com o valor inicial n
    for operacao_atual in sequencia:      # aplica cada operacao da sequencia sobre o valor atual
        if operacao_atual == '-1': 
            valor -= 1#decrementa o valor em 1

        elif operacao_atual == '/2': # operacao de divisao por 2
            # operacao de divisao por 2
            if valor % 2 != 0: # se valor nao e par 
                # se valor nao  e par
                # a operacao nao e valida
                return False 
            valor //= 2  # divide o valor por 2

        elif operacao_atual == '/3': # operacao de divisao por 3
            #verifica se valor e divisivel por 3
            if valor % 3 != 0:
                # se o  valor nao e divisivel por  3
                # a operacao nao e valida
                return False
            valor //= 3        # divide o valor por 3
    #verifica se o valor final é   1
    return valor == 1

def main():     # funcao principal que implementa a interface de linha de comando    
    #processa os args da linha de comando, valida a entrada,executa o metodo escolhido e exibe os results
    parser = argparse.ArgumentParser( # cria o parser de argumentos
        description='==== contagem_regressiva_da_nasa ===== - encontra o menor numero de operacoes para reduzir n ate 1'
    ) 
    # argumento obrigatorio (numero inteiro positivo para reduzir ate 1) 
    parser.add_argument('n', type=int, help='numero int positivo para reduzir ate 1')
    
    parser.add_argument(  # argumento opcional (metodo a ser usado)  
        '--metodo',          # metodo a ser usado
        choices=['rec', 'memo', 'dp'],  # escolhas de metodos
        default='dp',                     #   metodo padrao
        help='metodos a serem usados: rec = recursivo, memo = memoizacao, dp = (bottom-up = programação dinamica) '  #mensagem de ajuda
    )
    parser.add_argument(        # argumento opcional   (mostrar seq de operacoes)
        '--caminho',               # mostrar seq de operacoes
        action='store_true',          #  action que armazena o val True se o argumento for passado
        help='mostrar a sequencia otima de operacoes'   #mensagem de ajuda
    )
    args = parser.parse_args() # processa os args da linha de comando (valida a entrada)
    # validacoes de entrada ( int positivo para reduzir ate 1)
    if args.n <= 0: # se n for menor ou igual a 0
        print("erro: n deve ser int positivo", file=sys.stderr)     #mensagem de erro
        sys.exit(1)
    #exec metodo escolhido (rec, memo, dp)
    try:
        if args.metodo == 'rec': #   metodo recursivo simples
            if args.n > 20:         # limitar para evitar stack overflow
                print("aviso: n muito grande para metodo recursivo simples. use --metodo memo ou dp") #mensagem de aviso
                sys.exit(1)
            passos = cont_recursiva_simples(args.n) # chama a funcao recursiva simples
            sequencia = None  # este  metodo nao retorna sequencia
                         #se n for maior que 20, avisa que o metodo recursivo 
                         # simples nao é recomendado
                          #e sai do programa com erro
            
        elif args.metodo == 'memo':     # metodo recursivo com memoria
            passos = cont_com_memo(args.n)  # chama a funcao recursiva com memoria
            sequencia = None                          # este metodo nao retorna sequencia
            
        elif args.metodo == 'dp': # metodo bottom-up dp
            passos, sequencia = cont_bottomUp(args.n)         # chama a funcao bottom-up dp
        print(f"numero de passos minimos: {passos}")     #mostra o n minimo de passos
        
        # mostrar sequencia se solicitado e disp
        if args.caminho and sequencia is not None:    # se a  sequencia for solicitada e disp
            print(f"sequencia de operacoes: {' '.join(sequencia)}")   # mostra a sequencia de operacoes
            if validar_seq(args.n, sequencia):    #valida a sequencia  
                print("sequencia validada com sucesso")
            else:
                print("erro: validacao da sequencia sem sucesso", file=sys.stderr) # mensagem de erro
        elif args.caminho and sequencia is None: #se a sequencia for solicitada e nao disp
            #    para metodos que nao retornam sequencia por padrao, calcular usando dp
            _, sequencia = cont_bottomUp(args.n)  # chama a funcao bottom-up dp para fazer o calc da sequencia 
            print(f"sequencia de operacoes: {' '.join(sequencia)}")   # mostra a sequencia de operacoes
            
            #    validar sequencia para garantir que esta correta
            if validar_seq(args.n, sequencia):   # valida a sequencia
                print("sequencia validada com sucesso") # mensagem de sucesso
            else:
                print("erro: validacao da sequencia sem sucesso", file=sys.stderr) #mensagem de erro
    except RecursionError:  
        #   captura erro de stack overflow em funcs recursivas para evitar stack overflow
        print("erro: stack overflow. use um metodo nao-recursivo (--metodo dp)", file=sys.stderr) #mensagem de erro
        sys.exit(1)
    except Exception as e: #  captura outros erros inesperados
        print(f"houve um erro inesperado: {e}", file=sys.stderr) # mensagem de erro
        sys.exit(1)

if __name__ == '__main__': 
    main()