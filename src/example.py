class Example:
    # deve receber os parâmetros nomeados necessários e o barramento utilizado (seja SPI, Serial ou I2C)
    def __init__(self, spi_bus):
        self.spi_bus = spi_bus

    # método **OPCIONAL** da classe que realiza a inicialização do sensor
    def setup(self):
        pass

    # método **OBRIGATÓRIO** da classe que realiza leituras do sensor
    def read(self):
        # raw: os valores puros que foram lidos do sensor que se está trabalhando
        # value: representa o valor após conversão de unidades para ser apresentado diretamente ao usuário final
        # unit: unidade de medida
        return { 'raw': {}, 'value': 0.0, 'unit': '' }
