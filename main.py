from tkinter import *
import mysql.connector as mysql

db_connection = mysql.connect(
    host="localhost",
    user="root",
    passwd="1234",
    database="imc",
    auth_plugin='mysql_native_password'
)
db_handle = db_connection.cursor()


class Application:
    def __init__(self, master=None):

        # Instâncias

        self.paciente = Frame(master)
        self.paciente.pack()

        self.endereco = Frame(master)
        self.endereco.pack()

        self.altura = Frame(master)
        self.altura.pack()

        self.peso = Frame(master)
        self.peso.pack()

        self.resultado = Frame(master)
        self.resultado.pack()

        self.ultimos_pacientes = Frame(master)
        self.ultimos_pacientes.pack()

        self.calcular = Frame(master)
        self.calcular.pack(side=LEFT)

        self.reiniciar = Frame(master)
        self.reiniciar.pack(side=LEFT)

        self.sair = Frame(master)
        self.sair.pack(side=LEFT)

        # Labels e Inputs

        self.pacienteLabel = Label(self.paciente, text="Nome do Paciente:", width=16)
        self.pacienteLabel.pack(side=LEFT, pady=10)
        self.pacienteInput = Entry(self.paciente, width=50)
        self.pacienteInput.pack(side=LEFT)

        self.enderecoLabel = Label(self.endereco, text="Endereço Completo:", width=16)
        self.enderecoLabel.pack(side=LEFT)
        self.enderecoInput = Entry(self.endereco, width=50)
        self.enderecoInput.pack(side=LEFT)

        self.alturaLabel = Label(self.altura, text="Altura (cm/ex: 1.85):", width=16)
        self.alturaLabel.pack(side=LEFT, pady=10)
        self.alturaInput = Entry(self.altura, width=50)
        self.alturaInput.pack(side=LEFT)

        self.pesoLabel = Label(self.peso, text="Peso (Kg/ex: 90):", width=16)
        self.pesoLabel.pack(side=LEFT)
        self.pesoInput = Entry(self.peso, width=50)
        self.pesoInput.pack(side=LEFT)

        self.imcValor = Label(self.resultado, text="Resultado",  borderwidth=2, relief="groove", padx=190, pady=30)
        self.imcValor.pack(pady=10)

        self.ultimosPacientesLabel = Label(self.ultimos_pacientes, text="Últimos pacientes",  borderwidth=2, relief="groove", padx=190, pady=30)
        self.ultimosPacientesLabel.pack(pady=10)

        db_handle.execute("SELECT * FROM imc")
        pacientes_resultado = db_handle.fetchall()

        pacientes_array = []

        for resultado in pacientes_resultado:
            pacientes_array.append(resultado[1])
        if not pacientes_array:
            self.ultimosPacientesLabel["text"] = "Últimos pacientes (necessário reiniciar o programa)"
        else:
            pacientes_array.insert(0, "Últimos pacientes \n")
            self.ultimosPacientesLabel["text"] = "\n".join(pacientes_array)

        # Ações

        self.calcular = Button(self.calcular, text="Calcular", width=12, command=self.calcular_f)
        self.calcular.pack(padx=40, pady=15)

        self.reiniciar = Button(self.reiniciar, text="Reiniciar", width=12, command=self.reiniciar_f)
        self.reiniciar.pack(padx=40)

        self.sair = Button(self.sair, text="Sair", width=12, command=self.sair_f)
        self.sair.pack(padx=40)

    # Funções

    def calcular_f(self):
        paciente = self.pacienteInput.get()
        endereco = self.enderecoInput.get()
        peso = self.pesoInput.get()
        altura = self.alturaInput.get()
        imc = float(peso) / float(altura) ** 2
        imcconv = "%.4f" % imc
        classificacao = ""

        if peso:
            if imc < 16:
                classificacao = "Magreza grave"
            elif imc < 17:
                classificacao = "Magreza moderada"
            elif imc < 18.5:
                classificacao = "Magreza leve"
            elif imc < 25:
                classificacao = "Saudável"
            elif imc < 30:
                classificacao = "Sobrepeso"
            elif imc < 35:
                classificacao = "Obesidade Grau I"
            elif imc < 40:
                classificacao = "Obesidade Grau II (severa)"
            else:
                classificacao = "Obesidade Grau III (mórbida)"

        db_handle.execute("INSERT INTO imc(paciente, endereco, altura, peso) VALUES('" + paciente + "', '" + endereco + "', " + altura + ", " + peso + ")")
        db_connection.commit()

        resp = "Paciente " + paciente + "\n\nEndereço: " + endereco + "\n\nIMC: " + imcconv + "\n\n Classificação: " + classificacao
        self.imcValor["text"] = resp

    def reiniciar_f(self):
        self.pacienteInput.delete(0, "end")
        self.enderecoInput.delete(0, "end")
        self.alturaInput.delete(0, "end")
        self.pesoInput.delete(0, "end")
        self.imcValor["text"] = "Resultado"
        self.pacienteInput.focus()

    @staticmethod
    def sair_f():
        pyImc.destroy()


pyImc = Tk()
Application(pyImc)
pyImc.resizable(False, False)
pyImc.title("Cálculo de IMC - Índice de Massa Corporal")
pyImc.mainloop()
