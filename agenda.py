import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  print(cor + texto + RESET)
  

# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração. 
def adicionar(descricao, extras):

  # não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '':
    return False
  else:
    novaAtividade = ''
    if dataValida(extras[0]):
      novaAtividade += extras[0] + ' '
    if horaValida(extras[1]):
      novaAtividade += extras[1] + ' '
    if prioridadeValida(extras[2]):
      novaAtividade += extras[2] + ' '
    novaAtividade += descricao + ' '
    if contextoValido(extras[3]):
      novaAtividade += extras[3] + ' '
    if projetoValido(extras[4]):
      novaAtividade += extras[4]

    # Escreve no TODO_FILE. 
    try: 
      fp = open(TODO_FILE, 'a', encoding = 'utf-8-sig')
      fp.write(novaAtividade + "\n")
      fp.close()
    except IOError as err:
      print("Não foi possível escrever para o arquivo " + TODO_FILE)
      print(err)
      return False

    return True


# Valida a prioridade.
def prioridadeValida(pri):
  if len(pri) == 3 and pri[0] == '(' and pri[2] == ')' and (pri[1].upper() >= 'A' and pri[1].upper() <= 'Z'):
    return True
  else:
    return False



# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin) \
  or not(int(horaMin[0]+horaMin[1]) >= 0 and int(horaMin[0]+horaMin[1]) <= 23) and (int(horaMin[0]+horaMin[1]) >= 0 and int(horaMin[0]+horaMin[1]) <= 59):
    return False
  else:
      return True

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data) :
  if soDigitos(data) and len(data) == 8:
    dia = int(data[0]+data[1])
    mes = int(data[2]+data[3])
    if (dia >= 1 and dia <= 31) and (mes >= 1 and mes <= 12) and (mes >= 1 and mes <= 12) and (len(data[4:]) == 4) and \
    ((mes in [4, 6, 7, 11] and dia <= 30) or (mes in [1, 3, 5, 7, 8, 10, 12] and dia <= 31) or (mes == 2 and dia <= 29)):
      return True
    else:
      return False
  else:
    return False 
  

# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):
  if len(proj) >= 2 and proj[0] == '+':
    return True
  else:
    return False

# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):
  if len(cont) >= 2 and cont[0] == '@':
    return True
  else:
    return False

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas):
  itens = []
  #linhas = open("todo.txt", 'r', encoding = 'utf-8-sig')
  for l in linhas:
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
    
    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
    tokens = l.split() # quebra o string em palavras

    i = 0
    
    while (i < len(tokens)):
      if dataValida(tokens[i]):
        data = tokens.pop(i)
      elif horaValida(tokens[i]):
        hora = tokens.pop(i)
      elif prioridadeValida(tokens[i]):
        pri = tokens.pop(i)
      elif contextoValido(tokens[i]):
        contexto = tokens.pop(i)
      elif projetoValido(tokens[i]):
        projeto = tokens.pop(i)
      else:
        i += 1

    i = 0
    
    while i < len(tokens):
      if i == len(tokens) - 1:
        desc += tokens[i]
      else:
        desc += tokens[i] + " "
      i += 1
      
    
    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis. 

    #print((desc, (data, hora, pri, contexto, projeto)))
    itens.append((desc, (data, hora, pri, contexto, projeto)))

  #linhas.close()
  return itens


# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não


# é uma das tarefas básicas do projeto, porém. 
def listar():
  arq = open("todo.txt", "r", encoding = "utf-8-sig")
  linhas = arq.read().splitlines()
  arq.close()
  linhas_organizadas = organizar(linhas)
  linhas_ordenadas = ordenarPorPrioridade(ordenarPorDataHora(linhas_organizadas))
  linhas_organizadas = organizar(linhas)
  i = 0
  j = 0
  #print(linhas_organizadas)
  #print(linhas_ordenadas)
  achou = False
  linha = ""
  while i < len(linhas_organizadas):
    extras = linhas_ordenadas[i][1]
    while j < len(linhas_organizadas) and achou == False:
      if (linhas_ordenadas[i] == linhas_organizadas[j]) and (linhas_organizadas[j][0] != ''):
        linha += str(j+1) + " "
        if dataValida(extras[0]):
          linha += extras[0][0:2] + '/' + extras[0][2:4] + '/' + extras[0][4:] + ' '
        if horaValida(extras[1]):
          linha += extras[1][0:2] + 'h' + extras[1][2:] + 'm' + ' '
        if prioridadeValida(extras[2]):
          linha += extras[2] + ' '
        linha += linhas_ordenadas[i][0] + ' '
        if contextoValido(extras[3]):
          linha += extras[3] + ' '
        if projetoValido(extras[4]):
          linha += extras[4]
          
        if extras[2] == '(A)' or extras[2] == '(a)':
          printCores(linha, RED + BOLD)
        elif extras[2] == '(B)' or extras[2] == '(b)':
          printCores(linha, CYAN)
        elif extras[2] == '(C)' or extras[2] == '(c)':
          printCores(linha, GREEN)
        elif extras[2] == '(D)' or extras[2] == '(d)':
          printCores(linha, YELLOW)
        else:
          print(linha)
        achou = True
        
      j += 1
    j = 0
    achou = False
    linha = ""
    i += 1
    
def ordenarPorDataHora(itens):
  i = 0
  j = 0
  temp = ''
  #ordena por data: 
  while i < len(itens):
    while j < len(itens) - 1:
      strdata = itens[j][1][0]
      strdataprox = itens[j+1][1][0]
      if strdata == '':
        temp = itens[j+1]
        itens[j+1] = itens[j]
        itens[j] = temp
      elif strdataprox != '':
        if (int(strdata[4:]) > int(strdataprox[4:]))\
        or((int(strdata[4:]) == int(strdataprox[4:])) and (int(strdata[2]+strdata[3]) > int(strdataprox[2]+strdataprox[3])))\
        or ((int(strdata[4:]) == int(strdataprox[4:])) and (int(strdata[2]+strdata[3]) == int(strdataprox[2]+strdataprox[3]))\
        and (int(strdata[0]+strdata[1]) > int(strdataprox[0]+strdataprox[1]))):
          temp = itens[j+1]
          itens[j+1] = itens[j]
          itens[j] = temp
      j += 1
    j = 0
    i += 1
  #ordena por hora:
  i = 0
  j = 0
  temp = ''
  while i < len(itens):
    while j < len(itens) - 1:
      strdata = itens[j][1][0]
      strdataprox = itens[j+1][1][0]
      strhora = itens[j][1][1]
      strhoraprox = itens[j+1][1][1]
      if strdata == strdataprox and strhora == '' and strhoraprox != '':
        temp = itens[j + 1]
        itens[j+1] = itens[j]
        itens[j] = temp
      elif strdata == strdataprox and strhora != '' and strhoraprox != '':
        if (int(strhora[0]+strhora[1]) > int(strhoraprox[0]+strhoraprox[1])) or ((int(strhora[0]+strhora[1]) == int(strhoraprox[0]+strhoraprox[1]))\
        and (int(strhora[2]+strhora[3]) > int(strhoraprox[2]+strhoraprox[3]))):
          temp = itens[j + 1]
          itens[j+1] = itens[j]
          itens[j] = temp
      j += 1
    j = 0
    i += 1
  return itens
   
def ordenarPorPrioridade(itens):
  i = 0
  j = 0
  temp = ''
  while i < len(itens):
    while j < len(itens) - 1:
      strdata = itens[j][1][0]
      strdataprox = itens[j+1][1][0]
      strhora = itens[j][1][1]
      strhoraprox = itens[j+1][1][1]
      strpri = itens[j][1][2].upper()
      strpriprox = itens[j+1][1][2].upper()
      if strpri == '':
        if strpriprox != '':
          temp = itens[j+1]
          itens[j+1] = itens[j]
          itens[j] = temp
        else:
          if strdata != strdata and strdata != '' and strdataprox != '':
            if (int(strdata[4:]) > int(strdataprox[4:]))\
            or((int(strdata[4:]) == int(strdataprox[4:])) and (int(strdata[2]+strdata[3]) > int(strdataprox[2]+strdataprox[3])))\
            or ((int(strdata[4:]) == int(strdataprox[4:])) and (int(strdata[2]+strdata[3]) == int(strdataprox[2]+strdataprox[3]))\
            and (int(strdata[0]+strdata[1]) > int(strdataprox[0]+strdataprox[1]))):
              temp = itens[j+1]
              itens[j+1] = itens[j]
              itens[j] = temp
          elif strdata == strdataprox and strhora != '' and strhoraprox != '':
            if (int(strhora[0]+strhora[1]) > int(strhoraprox[0]+strhoraprox[1])) or ((int(strhora[0]+strhora[1]) == int(strhoraprox[0]+strhoraprox[1]))\
            and (int(strhora[2]+strhora[3]) > int(strhoraprox[2]+strhoraprox[3]))):
              temp = itens[j+1]
              itens[j+1] = itens[j]
              itens[j] = temp
      elif strpriprox != '' and strpri > strpriprox:
        temp = itens[j+1]
        itens[j+1] = itens[j]
        itens[j] = temp
      j += 1
    j = 0
    i += 1
        
  return itens

def fazer(num):
  arq = open("todo.txt", "r", encoding = "utf-8-sig")
  linhas = arq.read().splitlines()
  arq.close()
  linhas_organizadas = organizar(linhas)
  try:
    if int(num) >= 1 and linhas_organizadas[int(num)-1][0] != "":
      atividade_concluida = linhas_organizadas.pop(int(num)-1)
      descricao = atividade_concluida[0]
      extras = atividade_concluida[1]
    else:
      raise ValueError("ERRO: VERIFIQUE SE A ATIVIDADE "+num+" EXISTE")
    
    linhas = open("todo.txt", 'w', encoding = 'utf-8-sig')
    linhas.close()
    for i in linhas_organizadas:
      adicionar(i[0], i[1])
      
    atividade_concluida = ''
    if dataValida(extras[0]):
      atividade_concluida += extras[0] + ' '
    if horaValida(extras[1]):
      atividade_concluida += extras[1] + ' '
    if prioridadeValida(extras[2]):
      atividade_concluida += extras[2] + ' '
    atividade_concluida += descricao + ' '
    if contextoValido(extras[3]):
      atividade_concluida += extras[3] + ' '
    if projetoValido(extras[4]):
      atividade_concluida += extras[4]
    try: 
      fp = open(ARCHIVE_FILE, 'a', encoding = 'utf-8-sig')
      fp.write(atividade_concluida + "\n")
      fp.close()
    except IOError as err:
      print("Não foi possível escrever para o arquivo " + ARCHIVE_FILE)
      print(err)
  except Exception:
    print("ERRO: VERIFIQUE SE A ATIVIDADE "+num+" EXISTE")

def remover(n):
  arq = open("todo.txt", "r", encoding = "utf-8-sig")
  linhas = arq.read().splitlines()
  arq.close()
  linhas_organizadas = organizar(linhas)
  try:
    if int(n) >= 1 and linhas_organizadas[int(n)-1][0] != "":
      linhas_organizadas.pop(int(n)-1)
    else:
      raise ValueError("VERIFIQUE SE A ATIVIDADE "+n+" EXISTE")
    linhas = open("todo.txt", 'w', encoding = 'utf-8-sig')
    linhas.close()
    for i in linhas_organizadas:
      adicionar(i[0], i[1])
  except Exception as e:
    print("ERRO: VERIFIQUE SE A ATIVIDADE "+n+" EXISTE")

# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):
  arq = open("todo.txt", "r", encoding = "utf-8-sig")
  linhas = arq.read().splitlines()
  arq.close()
  linhas_organizadas = organizar(linhas)
  try:
    if int(num) >= 1 and linhas_organizadas[int(num)-1][0] != "":
        extras = linhas_organizadas[int(num)-1][1]
        extras = (extras[0], extras[1], "("+prioridade.upper()+")", extras[3], extras[4])
        linhas_organizadas[int(num)-1] = (linhas_organizadas[int(num)-1][0], extras)
    else:
        raise ValueError("VERIFIQUE SE A ATIVIDADE "+num+" EXISTE")
    linhas = open("todo.txt", 'w', encoding = 'utf-8-sig')
    linhas.close()
    for i in linhas_organizadas:
      adicionar(i[0], i[1])
  except Exception as e:
    print("ERRO: VERIFIQUE SE A ATIVIDADE "+num+" EXISTE")

# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos):
  try:
    if comandos[1] == ADICIONAR:
      comandos.pop(0) # remove 'agenda.py'
      comandos.pop(0) # remove 'adicionar'
      itemParaAdicionar = organizar([' '.join(comandos)])[0]
      # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
      adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
    elif comandos[1] == LISTAR:
      listar()
    elif comandos[1] == REMOVER:
      comandos.pop(0)
      comandos.pop(0)
      remover(comandos.pop(0))    
    elif comandos[1] == FAZER:
      comandos.pop(0)
      comandos.pop(0)
      fazer(comandos.pop(0))
    elif comandos[1] == PRIORIZAR:
      comandos.pop(0)
      comandos.pop(0)
      priorizar(comandos.pop(0), comandos.pop(0))
    else :
      print("Comando inválido.")
  except Exception as e:
    print(e)
    print("VERIQUE SE DIGITOU UM COMANDO POSSÍVEL")
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)
