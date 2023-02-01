from django.shortcuts import render
import heapq

# Create your views here.

def index(request):

    return render(request, 'home.html')

def rota(request):

    if request.GET.get('inicial') and request.GET.get('final'):

        inicio = request.GET.get('inicial')
        fim = request.GET.get('final')
        
        distancias = {
            'Catalão': {'Anhanguera': 61.9, 'Marzagão': 114.7, 'Ipameri': 75.1},
            'Anhanguera': {'Marzagão': 81},
            'Marzagão': {'Morrinhos': 96.1, 'Buriti Alegre': 63.6},
            'Ipameri': {'Marzagão': 97.9},
            'Buriti Alegre': {'Panamá': 55.5, 'Goiatuba': 45},
            'Morrinhos': {'Buriti Alegre': 56.3},
            'Panamá': {'Goiatuba': 26.8},
            'Goiatuba': {'Turvelândia': 120},
            'Turvelândia': {},
        }

        distancia, caminho = caminho_mais_curto(distancias, inicio, fim)
    
        if distancia is not None:

            trajeto = ''
            for item in caminho:
                if caminho[-1]==item:
                    trajeto = trajeto + item
                else:
                    trajeto = trajeto + item + ' ---> '

            distancia = 'A distância mais curta entre ' + inicio + ' e ' + fim + ' é de ' + str(distancia) + 'km.'
            caminho = 'O trajeto a ser feito é: ' + trajeto

            context = {
                'distancia': distancia,
                'caminho': caminho,
            }
            return render(request, 'rota.html', context=context)
        else:
            nao_encontrado = 'Não foi possível encontrar um caminho entre ' + inicio + " e " + fim + "."

            context = {
                'nao_encontrado': nao_encontrado,
            }
            return render(request, 'rota.html', context=context)

    return render(request, 'rota.html')

def caminho_mais_curto(distancias, inicio, fim):
    # Inicializa a lista de prioridades com o valor 0, o ponto inicial e um caminho vazio
    prioridade = [(0, inicio, [])]
    # Inicializa o conjunto de pontos já visitados
    visitado = set()
    # Enquanto a lista de prioridades não estiver vazia
    while prioridade:
        # Pega o elemento com menor valor (distância) da lista de prioridades
        (custo, atual, caminho) = heapq.heappop(prioridade)
        # Se o ponto atual já foi visitado, passa para o próximo da lista
        if atual in visitado:
            continue
        # Adiciona o ponto atual aos pontos visitados
        visitado.add(atual)
        # Adiciona o ponto atual ao caminho
        caminho = caminho + [atual]
        # Se chegou no ponto final, retorna a distância total e o caminho
        if atual == fim:
            return (custo, caminho)
        # Para cada vizinho do ponto atual
        for (vizinha, distancia) in distancias[atual].items():
            # Se o vizinho já foi visitado, pula para o próximo
            if vizinha in visitado:
                continue
            # Adiciona o vizinho à lista de prioridades com a distância atualizada e o caminho atual
            heapq.heappush(prioridade, (custo + distancia, vizinha, caminho))

    # Se não encontrou o ponto final, retorna None
    return None, None