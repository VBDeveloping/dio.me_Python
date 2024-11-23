class bicicleta:
    def __init__(self,cor,modelo, marca,ano,valor):
        self.cor = cor
        self.modelo = modelo
        self.marca = marca
        self.ano =ano
        self.valor = valor

    def buzinar (self):
        print("bom bom")
    def parar (self):
        print("Parando a bicicleta...")
        print("Bicicleta parada")
    def correr (self):
        print("Shum Shum")

    #def __str__(self):
     #   return f"bicicleta: cor= {self.cor}, modelo= {self.modelo}, ano= {self.ano}, valor= {self.valor}"
    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"

b1 = bicicleta("Azul", "Speed", "Caloi", 2024, 1200)
#b1.buzinar()
#b1.parar()
#b1.correr()

print(b1)