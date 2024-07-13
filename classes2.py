class Apartamento:
    def __init__(self, id, numero, vaga=None):
        self.id = id
        self.numero = numero
        self.vaga = vaga
        self.proximo = None

    def cadastrar(self):
        print(f"Apartamento {self.numero} inserido.")

    def imprimir(self):
        print(f"Apartamento ID: {self.id}, Número: {self.numero}, Vaga: {self.vaga}")

## Gerenciador da fila de espera
    # Adicionar apartamentos na fila / Redistribuir as vagas


#class FilaDeEspera:
#    def __init__(self):
#        self.fila = []
#
#    def adicionar_apartamento(self, apartamento):
#        self.fila.append(apartamento)
#        print(f"Apartamento {apartamento.numero} está na fila de espera.")
#
#    def retirar_apartamento(self, numero_vaga):
#        if self.fila:
#            apt = self.fila.pop(0)
#            apt.vaga = numero_vaga
#            print(f"Apartamento {apt.numero} recebeu a vaga {numero_vaga}.")
#            return apt
#        else:
#            print("A fila está vazia.")
#            return None
#
#    def print_apartamentos(self):
#        print("Fila de Espera:")
#        for apt in self.fila:
#            print(f"Apartamento {apt.numero}")


class FilaDeEspera:
    def __init__(self):
        self.inicio = None
        self.fim = None

    def adicionar_apartamento(self, apartamento):
        if not self.inicio: 
            self.inicio = apartamento
            self.fim = apartamento
        else:
            self.fim.proximo = apartamento
            self.fim = apartamento
        print(f"Apartamento {apartamento.numero} foi para a lista de espera.")

    def retirar_apartamento(self, numero_vaga):
        if self.inicio:
            apt = self.inicio
            self.inicio = self.inicio.proximo
            if not self.inicio: 
                self.fim = None
            apt.vaga = numero_vaga
            print(f"Apartamento {apt.numero} recebeu a vaga {numero_vaga}.")
            return apt
        else:
            print("A fila está vazia.")
            return None

    def imprimir(self):
        print("Fila de Espera:")
        apt = self.inicio
        while apt:
            print(f"Apartamento {apt.numero}")
            apt = apt.proximo


## Gerencia os aparatamentos inseridos
    # Insere apartamentos
class Torre:
    def __init__(self, total_vagas, db_connection):
        self.total_vagas = total_vagas
        self.apartamentos_com_vaga = self.carregar_apartamentos_com_vaga(db_connection)
        self.fila_de_espera = FilaDeEspera()
        self.apartamentos_cadastrados = len(self.apartamentos_com_vaga)
        self.db_connection = db_connection

    def carregar_apartamentos_com_vaga(self, db_connection):
        cursor = db_connection.cursor()
        cursor.execute("SELECT id, numero, vaga FROM apartamentos")
        apartamentos = []
        for (id, numero, vaga) in cursor:
            apartamentos.append(Apartamento(id, numero, vaga))
        cursor.close()
        return sorted(apartamentos, key=lambda x: x.vaga)

    def cadastrar_apartamento(self, apt):
        self.apartamentos_cadastrados += 1
        if self.apartamentos_cadastrados <= self.total_vagas:
            apt.vaga = self.apartamentos_cadastrados  
            self.apartamentos_com_vaga.append(apt)
            self.apartamentos_com_vaga.sort(key=lambda x: x.vaga)
            print(f"Apartamento {apt.numero} cadastrado com vaga {apt.vaga}.")
            self.salvar_apartamento_no_banco(apt)
        else:
            self.fila_de_espera.adicionar_apartamento(apt)

    def salvar_apartamento_no_banco(self, apt):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO apartamentos (id, numero, vaga) VALUES (%s, %s, %s)", (apt.id, apt.numero, apt.vaga))
        self.db_connection.commit()
        cursor.close()

    def liberar_vaga(self, numero_vaga):
        for i, apt in enumerate(self.apartamentos_com_vaga):
            if apt.vaga == numero_vaga:
                apt.vaga = None
                self.apartamentos_com_vaga.pop(i)
                self.fila_de_espera.adicionar_apartamento(apt)
                novo_apt = self.fila_de_espera.retirar_apartamento(numero_vaga)
                if novo_apt:
                    self.apartamentos_com_vaga.append(novo_apt)
                    self.apartamentos_com_vaga.sort(key=lambda x: x.vaga)
                    self.salvar_apartamento_no_banco(novo_apt)
                break

    def imprimir_apartamentos_com_vaga(self):
        print("Apartamentos com Vaga:")
        for apt in self.apartamentos_com_vaga:
            apt.imprimir()

    def imprimir_fila_de_espera(self):
        self.fila_de_espera.imprimir()



