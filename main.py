#!/usr/bin/python3
import sys
import time

start_time = time.time()

class TrieNode:
  def __init__(self, simbolo = '', valor = 0):
    self.TrieProps(simbolo, valor)

  def TrieProps(self, simbolo, valor):
      self.filhos = {}
      self.valor = valor
      self.simbolo = simbolo
      
  def criaFilho(self, node):
    self.filhos.update({node.simbolo: node})

def param_entrada():

    # Verificação necessária para garantir que crie o arquivo mesmo se os argumentos opcionais 
    # não forem passados (por isso não existe um else pedindo para ajustar a entrada)

    if(len(sys.argv) == 3) and (sys.argv[1] == '-c'):
        new_file_name = (sys.argv[2])[:-4] + '.z78'
    elif(len(sys.argv) == 3) and (sys.argv[1] == '-x'):
        new_file_name = (sys.argv[2])[:-4] + '.txt'
    elif(len(sys.argv) == 5):
        new_file_name = (sys.argv[4])
    return new_file_name

def leitura_inicial():
    return param_entrada()

new_file_name = leitura_inicial()
orig_file = open(sys.argv[2], 'r', encoding='utf-8')
new_file = open(new_file_name, 'w', encoding='utf-8')

def compr_file(TrieNode, new_file, valor, char, no):
    if no.filhos.get(char) == None:
        new_file.write(str(no.valor) + "´" + char + '\\')         # Escrever no arquivo de saída o trecho comprimido
        new_node = TrieNode(char, valor)                          # Inserir novo nó na trie, correspondente ao novo símbolo lido
        no.criaFilho(new_node)                                    # Insere um novo nó na trie como filho do nó em que a busca foi finalizada


def descompr_file(new_file, token_list, decomp_dict, decompCount):
    for i in token_list:
        if i == '':
            break
        cod_char_list = i.split("´")
        index = int(cod_char_list[0])
        char = cod_char_list[1]
        text = decomp_dict.get(index) + char
        decomp_dict.update({decompCount: text})
        decompCount+=1
        new_file.write(text)

# Aqui é onde o fluxo do código vai entrar caso na entrada seja solicitada a COMPRESSÃO do arquivo passado por parâmetro

if(sys.argv[1] == '-c'):
    
    root = TrieNode()
    valor = 1

    # Leitura do arquivo 
    while 1:
        
        # Lê arquivo até não ter mais nada pra ler
        char = orig_file.read(1)       
        if not char:
            break
        
        no = root
        match_padrao = ''

        # Se buscarmos um caractere no dicionário de filhos no nó em questão e encontrarmos algo, continuaremos procurando o 
        # próximo caractere no arquivo nos filhos. 
        while(no.filhos.get(char) != None):
            no = no.filhos.get(char)                      # O nó corresponde ao caractere lido e é onde continuaremos a busca
            match_padrao = match_padrao + char            # Atualiza o padrão que vai para o no dicionário
            char = orig_file.read(1)                      # Leitura de um novo caractere

       
        compr_file(TrieNode, new_file, valor, char, no)
        
        valor += 1

    numBits = 0
    valor -= 1
    while valor > 2**(numBits):
        numBits += 1

    # Temos x entradas no arquivo comprimido: cada inteiro é representado pelo cálculo de: (numBits) * bits + 8 bits por caractere
    tam_arq_comp = valor*numBits + 8*valor
    orig_file.seek(0)
    arq_inteiro = orig_file.read()
    print("Tamanho inicial do arquivo: " + str(8*(len(arq_inteiro))))
    print("Tamanho do arquivo após compressão: " + str(tam_arq_comp))
    print("Taxa de compressão obtida: " + str(round((((8*len(arq_inteiro))/tam_arq_comp)),6)))


else:
    
    # Aqui é onde o fluxo do código vai entrar caso na entrada seja solicitada a DESCOMPRESSÃO do arquivo passado por parâmetro

    sys.argv[1] == '-x'
    codif = orig_file.read()
    token_list = codif.split("\\")
    decomp_dict = {0: ''}
    decompCount = 1

    descompr_file(new_file, token_list, decomp_dict, decompCount)


orig_file.close()
new_file.close()
print("Tempo de execução: %s segundos" % round((time.time() - start_time),6))