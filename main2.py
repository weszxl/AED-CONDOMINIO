import mysql.connector
from classes2 import Apartamento, Torre

def menu():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sua_senha",
        database="TorreDB"
    )
    torre = Torre(10, db_connection)

    while True:
        print("\nMenu:")
        print("1. Inserir Apartamento")
        print("2. Liberar uma Vaga")
        print("3. Exibir Apartamentos com Vaga")
        print("4. Exibir Fila de Espera")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            id_apt = int(input("ID do Apartamento: "))
            numero = input("Número do Apartamento: ")
            if len(torre.apartamentos_com_vaga) < torre.total_vagas:
                apt = Apartamento(id_apt, numero)
            else:
                apt = Apartamento(id_apt, numero)
            torre.cadastrar_apartamento(apt)

        elif opcao == "2":
            numero_vaga = int(input("Número da Vaga a ser liberada: "))
            torre.liberar_vaga(numero_vaga)

        elif opcao == "3":
            torre.imprimir_apartamentos_com_vaga()

        elif opcao == "4":
            torre.imprimir_fila_de_espera()

        elif opcao == "5":
            db_connection.close()
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()



