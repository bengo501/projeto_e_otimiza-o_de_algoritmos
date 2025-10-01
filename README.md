# Contagem Regressiva - NASA

Este programa resolve o problema da NASA de encontrar o menor número de operações para reduzir um número inteiro positivo `n` até 1, usando apenas as operações disponíveis no computador danificado:

- **Decremento de uma unidade** (`-1`)
- **Divisão por 2** (`/2`) - somente quando o número é divisível por 2
- **Divisão por 3** (`/3`) - somente quando o número é divisível por 3

## Funcionalidades

O programa implementa **4 métodos diferentes** para resolver o problema:

1. **Recursivo Simples** (`rec`) - Implementação direta da recorrência (apenas para números pequenos)
2. **Recursivo com Memoização** (`memo`) - Otimização com cache para evitar recomputações
3. **Bottom-up DP** (`dp`) - Programação dinâmica não-recursiva (recomendado)
4. **BFS** (`bfs`) - Busca em largura modelando como grafo

## Uso

```bash
python contagem_regressiva.py <n> [--method <metodo>] [--path]
```

### Parâmetros

- `<n>`: Número inteiro positivo para reduzir até 1
- `--method`: Método a ser usado (`rec`, `memo`, `dp`, `bfs`) - padrão: `dp`
- `--path`: Mostrar a sequência ótima de operações (opcional)

### Exemplos

```bash
# Usar método bottom-up DP (padrão) com número 780
python contagem_regressiva.py 780

# Mostrar também a sequência de operações
python contagem_regressiva.py 780 --path

# Usar método com memoização
python contagem_regressiva.py 100 --method memo --path

# Usar BFS para encontrar o caminho
python contagem_regressiva.py 50 --method bfs --path

# Caso especial - n = 1
python contagem_regressiva.py 1 --path
```

### Saída Esperada

```
Passos mínimos: 10
Operações: /2 /2 /3 -1 -1 /3 /3 -1 /2 /3
✓ Sequência validada com sucesso!
```

## Exemplo Completo (n=780)

Para o número 780, o programa encontra que são necessárias **10 operações**:

1. 780 → 390 (`/2`)
2. 390 → 195 (`/2`) 
3. 195 → 65 (`/3`)
4. 65 → 64 (`-1`)
5. 64 → 63 (`-1`)
6. 63 → 21 (`/3`)
7. 21 → 7 (`/3`)
8. 7 → 6 (`-1`)
9. 6 → 3 (`/2`)
10. 3 → 1 (`/3`)

## Complexidade

- **Recursivo Simples**: O(3^n) - exponencial, apenas para teste
- **Recursivo com Memo**: O(n) tempo e espaço
- **Bottom-up DP**: O(n) tempo e espaço  
- **BFS**: O(n) tempo e espaço

## Validações

- ✅ Números negativos ou zero são rejeitados
- ✅ A sequência de operações é validada automaticamente
- ✅ Caso especial n=1 retorna 0 operações
- ✅ Proteção contra stack overflow em métodos recursivos

## Executar Exemplos

Para ver vários exemplos de uso:

```bash
python exemplo_uso.py
```

## Estrutura do Código

- `contagem_recursiva_simples()`: Versão baseline recursiva
- `contagem_com_memoizacao()`: Versão otimizada com cache
- `contagem_bottom_up()`: Versão DP não-recursiva
- `contagem_bfs()`: Versão usando busca em largura
- `validar_sequencia()`: Valida se uma sequência leva ao resultado correto
- `main()`: Interface de linha de comando

O programa está pronto para impressionar a NASA! 🚀
