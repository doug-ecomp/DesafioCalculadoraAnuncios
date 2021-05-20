import unittest
from typing import Union

MAX_COMPARTILHAMENTOS = 4
VISUALIZACOES_POR_REAL = 30
VISUALIZACOES_POR_COMPARTILHAMENTO = 40
MULTIPLICADOR_CLIQUES = 12
DIVISOR_CLIQUES = 100
MULTIPLICADOR_COMPARTILHAMENTOS = 3
DIVISOR_COMPARTILHAMENTOS = 20
DIGITOS_APROXIMACAO = 2


def visualizacao_inicial(investimento: Union[int, float], proporcional: bool = False) -> Union[int, float]:
    """Calcula a quantiddde de visualizações inicial de acordo com o investimento.

    Dois tipos de cálculos estão disponívels: proporcional e truncado.
    No cálculo proporcional, o resultado final é aproximado, caso necessário, para até duas casas decimais.
    No cáclulo truncado, valores fracionados tem sua parte decimal desconsiderada, sem causar nenhuma aproximação.
    O cálculo truncado é a opção padrão (caso o valor do parâmetro não seja passado).

    :param investimento: Valor intestido em reais.
    :param proporcional: Tipo de cálculo. True para proporcional e False para truncado.
    :return: A quantidade inicial de visualizações gerada pelo anúncio original.
    """
    if proporcional:
        return round(VISUALIZACOES_POR_REAL * investimento, DIGITOS_APROXIMACAO)
    else:
        return VISUALIZACOES_POR_REAL * (investimento // 1)


def cliques(qtd_visualizacoes: Union[int, float], proporcional: bool = False) -> Union[int, float]:
    """Calcula a quatidade de cliques de acordo com o número de visualizações do anúncio.

    Dois tipos de cálculos estão disponívels: proporcional e truncado.
    No cálculo proporcional, o resultado final é aproximado, caso necessário, para até duas casas decimais.
    No cáclulo truncado, valores fracionados tem sua parte decimal desconsiderada, sem causar nenhuma aproximação.
    O cálculo truncado é a opção padrão (caso o valor do parâmetro não seja passado).

    :param qtd_visualizacoes:  Quantidade de visualicações.
    :param proporcional: Tipo de cálculo. True para proporcional e False para truncado.
    :return: Quantidade de cliques gerados pela quantidade de visualizações.
    """
    if proporcional:
        # qtd_visualizacoes = round(qtd_visualizacoes, DIGITOS_APROXIMACAO)
        return round(MULTIPLICADOR_CLIQUES * (qtd_visualizacoes / DIVISOR_CLIQUES), DIGITOS_APROXIMACAO)
    else:
        return MULTIPLICADOR_CLIQUES * ((qtd_visualizacoes // 1) // DIVISOR_CLIQUES)


def compartilhamentos(qtd_cliques: Union[int, float], proporcional: bool = False) -> Union[int, float]:
    """Calcula a quatidade de compartilhamentos de acordo com a quantidade de cliques do anúncio.

    Dois tipos de cálculos estão disponívels: proporcional e truncado.
    No cálculo proporcional, o resultado final é aproximado, caso necessário, para até duas casas decimais.
    No cáclulo truncado, valores fracionados tem sua parte decimal desconsiderada, sem causar nenhuma aproximação.
    O cálculo truncado é a opção padrão (caso o valor do parâmetro não seja passado).

    :param qtd_cliques: Quatidade de cliques.
    :param proporcional: Tipo de cálculo. True para proporcional e False para truncado.
    :return: Quantidade de compartilhamentos gerados pela quantidade de cliques.
    """

    if proporcional:
        # qtd_cliques = round(qtd_cliques, DIGITOS_APROXIMACAO)
        return round(MULTIPLICADOR_COMPARTILHAMENTOS * (qtd_cliques / DIVISOR_COMPARTILHAMENTOS), DIGITOS_APROXIMACAO)
    else:
        return MULTIPLICADOR_COMPARTILHAMENTOS * ((qtd_cliques // 1) // DIVISOR_COMPARTILHAMENTOS)


def novas_visualizacoes(qtd_visualizacoes: Union[int, float], proporcional: bool = False) -> Union[int, float]:
    """Calcula a quantidade de novas visualizações geradas pelo dado número de visualizações que o aúncio possui.

    Dois tipos de cálculos estão disponívels: proporcional e truncado.
    No cálculo proporcional, o resultado final é aproximado, caso necessário, para até duas casas decimais.
    No cáclulo truncado, valores fracionados tem sua parte decimal desconsiderada, sem causar nenhuma aproximação.
    O cálculo truncado é a opção padrão (caso o valor do parâmetro não seja passado).

    :param qtd_visualizacoes: Quantidade de visualizações que o anúncio possui.
    :param proporcional: Tipo de cálculo. True para proporcional e False para truncado.
    :return: A quantidade de novas visualizações geradas.
    """

    qtd_cliques = cliques(qtd_visualizacoes, proporcional)

    qtd_compartilhamentos = compartilhamentos(qtd_cliques, proporcional)

    return round(qtd_compartilhamentos * VISUALIZACOES_POR_COMPARTILHAMENTO, DIGITOS_APROXIMACAO)


def visualizacao_total(investimento: Union[int, float], proporcional: bool = False) -> Union[int, float]:
    """Calcula a quantidade máxima de visualizações de um anúncio de acordo com o investimento e os compartilhamentos.

    Dois tipos de cálculos estão disponívels: proporcional e truncado.
    No cálculo proporcional, o resultado final é aproximado, caso necessário, para até duas casas decimais.
    No cáclulo truncado, valores fracionados tem sua parte decimal desconsiderada, sem causar nenhuma aproximação.
    O cálculo truncado é a opção padrão (caso o valor do parâmetro não seja passado).

    :param investimento: Valor investido em reais.
    :param proporcional: Tipo de cálculo. True para proporcional e False para truncado.
    :return: Quantidade máxima de visualizações do anúncio.
    """

    lista_visualizacoes = [visualizacao_inicial(investimento, proporcional)]
    for _ in range(MAX_COMPARTILHAMENTOS):
        visualizacoes = novas_visualizacoes(lista_visualizacoes[-1], proporcional)
        if visualizacoes > 0:
            lista_visualizacoes.append(visualizacoes)
        else:
            break

    return sum(lista_visualizacoes)


if __name__ == '__main__':
    investimento = int(input('Digite o valor que será investido: '))
    tipo_calculo = input('Deseja que o cálculo seja proporcional ou truncado? (p|t): ')

    proporcional = True if tipo_calculo == 'p' else False

    total_visualizacoes = visualizacao_total(investimento, proporcional)

    print(f'Seu investimento foi de R$ {investimento}. O máximo de visualizações é {total_visualizacoes}')


class TestCalculadora(unittest.TestCase):
    """Classe dos testes unitários da calculadora de visualizações máxima de um anúncio.
    Cada função que compõe a calculadora tem dois métodos nessa classe, um para o cálculo proporcional e o outro para o cálculo truncado"""

    def test_visualizacao_inicial_truncado(self):
        proporcional = False
        lista_valores = [(405, 12150), (399, 11970), (10.5, 300), (216.1, 6480)]
        for entrada, saida in lista_valores:
            result = visualizacao_inicial(entrada, proporcional)
            self.assertEqual(result, saida)

    def test_visualizacao_inicial_proporcional(self):
        proporcional = True
        lista_valores = [(111.11, 3333.30), (500.675, 15020.25), (10.5, 315), (216.1, 6483)]
        for entrada, saida in lista_valores:
            result = visualizacao_inicial(entrada, proporcional)
            self.assertEqual(result, saida)

    def test_cliques_truncado(self):
        proporcional = False
        lista_valores = [(3000, 360), (9210, 1104), (25, 0), (7250.5, 864)]
        for entrada, saida in lista_valores:
            result = cliques(entrada, proporcional)
            self.assertEqual(result, saida)

    def test_cliques_proporcional(self):
        proporcional = True
        lista_valores = [(50.5549, 6.07), (9210, 1105.20), (25, 3), (7250.5, 870.06)]
        for entrada, saida in lista_valores:
            result = cliques(entrada, proporcional)
            self.assertEqual(result, saida)

    def test_compartilhamentos_truncado(self):
        proporcional = False
        lista_valores = [(768, 114), (384, 57), (19, 0), (111.11, 15)]
        for entrada, saida in lista_valores:
            result = compartilhamentos(entrada, proporcional)
            self.assertEqual(result, saida)

    def test_compartilhamentos_proporcional(self):
        proporcional = True
        lista_valores = [(777.96, 116.69), (290.4, 43.56), (19, 2.85), (111.11, 16.67)]
        for entrada, saida in lista_valores:
            result = compartilhamentos(entrada, proporcional)
            self.assertEqual(result, saida)

    def test_novas_visualizacoes_truncado(self):
        proporcional = False
        lista_valores = [(3000, 2160), (2160, 1440), (1440, 960), (960, 600)]
        for entrada, saida in lista_valores:
            result = novas_visualizacoes(entrada, proporcional)
            self.assertEqual(result, saida)

    def test_novas_visualizacoes_proporcional(self):
        proporcional = True
        lista_valores = [(2420.40, 1742.80), (85.5345, 61.60), (178.29, 128.40), (30, 21.60)]
        for entrada, saida in lista_valores:
            result = novas_visualizacoes(entrada, proporcional)
            self.assertEqual(result, saida)

    def test_visualizacao_total_truncado(self):
        proporcional = False
        lista_valores = [(100, 8160), (6542, 564780), (664, 56880), (233, 19470)]
        for entrada, saida in lista_valores:
            result = visualizacao_total(entrada, proporcional)
            self.assertEqual(result, saida)

    def test_visualizacao_total_proporcional(self):
        proporcional = True
        lista_valores = [(82.24, 7106.80), (30, 2592.40), (1, 86.40), (33.333, 2880.39)]
        for entrada, saida in lista_valores:
            result = visualizacao_total(entrada, proporcional)
            self.assertEqual(result, saida)
