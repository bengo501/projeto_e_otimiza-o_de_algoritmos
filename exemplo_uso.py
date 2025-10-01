#!/usr/bin/env python3
"""
Exemplo de uso do programa de contagem regressiva
"""

import subprocess
import sys

def executar_comando(comando):
    """Executa um comando e mostra o resultado"""
    print(f"\n{'='*50}")
    print(f"Comando: {comando}")
    print('='*50)
    
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        print(resultado.stdout)
        if resultado.stderr:
            print("Erro:", resultado.stderr)
    except Exception as e:
        print(f"Erro ao executar comando: {e}")

def main():
    print("EXEMPLOS DE USO DO PROGRAMA DE CONTAGEM REGRESSIVA")
    print("=" * 60)
    
    # Exemplo 1: Número pequeno com método recursivo simples
    executar_comando("python contagem_regressiva.py 10 --method rec --path")
    
    # Exemplo 2: Número médio com memoização
    executar_comando("python contagem_regressiva.py 100 --method memo --path")
    
    # Exemplo 3: Número grande com bottom-up DP
    executar_comando("python contagem_regressiva.py 780 --method dp --path")
    
    # Exemplo 4: Mesmo número com BFS
    executar_comando("python contagem_regressiva.py 780 --method bfs --path")
    
    # Exemplo 5: Caso especial - n = 1
    executar_comando("python contagem_regressiva.py 1 --method dp --path")
    
    # Exemplo 6: Sem mostrar o caminho
    executar_comando("python contagem_regressiva.py 50 --method dp")
    
    # Exemplo 7: Caso de erro - número negativo
    executar_comando("python contagem_regressiva.py -5 --method dp")

if __name__ == '__main__':
    main()
