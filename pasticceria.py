from abc import ABC, abstractmethod
import time

# Classe astratta con ingredienti di base
class ModelloTorta(ABC):
    def __init__(self, nome, peso, ingredienti_aggiuntivi):
        self.nome = nome
        self.peso = peso
        self.ingredienti = ["farina", "zucchero", "uova"] + ingredienti_aggiuntivi

    @abstractmethod
    def calcola_prezzo(self, peso):
        pass

# Sottoclasse per una Torta al cioccolato
class TortaCioccolato(ModelloTorta):
    def __init__(self, peso):
        super().__init__("Torta al Cioccolato", peso, ["cioccolato"])
        self.base_price = 15  # Prezzo base per la torta al cioccolato

    def calcola_prezzo(self, peso):
        prezzo = self.base_price * peso  # Il prezzo dipende dal peso
        return prezzo

# Sottoclasse per una Torta alla frutta
class TortaFrutta(ModelloTorta):
    def __init__(self, peso):
        super().__init__("Torta alla Frutta", peso, ["frutta"])
        self.base_price = 12  # Prezzo base per la torta alla frutta

    def calcola_prezzo(self, peso):
        prezzo = self.base_price * peso  # Il prezzo dipende dal peso
        return prezzo

# Sottoclasse per una Torta di mele
class TortaMela(ModelloTorta):
    def __init__(self, peso):
        super().__init__("Torta di Mela", peso, ["mele"])
        self.base_price = 10  # Prezzo base per la torta di mela

    def calcola_prezzo(self, peso):
        prezzo = self.base_price * peso  # Il prezzo dipende dal peso
        return prezzo
    
# Classe pasticceria con gestione ingredienti e saldo
class Pasticceria():
    def __init__(self):
        self.__inventario = {}
        self.__saldo = 10  # saldo iniziale della pasticceria
        self.__ingredienti = {
            "farina": 100,   # quantità in kg
            "zucchero": 50,  # quantità in kg
            "uova": 30,      # quantità in unità
            "cioccolato": 20,
            "frutta": 25,
            "mele": 15
        }

    def get_saldo(self):
        return self.__saldo

    def registra_vendita(self, torta):
        guadagno = torta.calcola_prezzo(torta.peso)
        self.__saldo += guadagno
        print(f"🍰 La pasticceria ha guadagnato €{guadagno:.2f}. Saldo attuale: €{self.__saldo:.2f} 🏦\n")

    def rifornisci_ingredienti(self, ingrediente, quantita):
        if ingrediente in self.__ingredienti:
            self.__ingredienti[ingrediente] += quantita
            # Ogni rifornimento di ingredienti costa 1 euro dalla pasticceria
            self.__saldo -= 1
            print(f"✔️ {quantita} kg di {ingrediente} sono stati aggiunti all'inventario. Costo: €1.")
            print(f"Saldo rimanente della pasticceria: €{self.__saldo:.2f}\n")
        else:
            print(f"❌ Ingrediente {ingrediente} non trovato.\n")

    def verifica_ingredienti(self, torta):
        for ingrediente in torta.ingredienti:
            if ingrediente in self.__ingredienti and self.__ingredienti[ingrediente] > 0:
                pass  # Ingrediente disponibile
            else:
                print(f"❌ Ingredienti insufficienti: {ingrediente}!")
                return False
        return True

    def crea_torta(self, peso, nome):
        nome = nome.lower()
        time.sleep(2)
        match nome:
            case "tortafrutta":
                torta = TortaFrutta(peso)
            case "tortamela":
                torta = TortaMela(peso)
            case "tortacioccolato":
                torta = TortaCioccolato(peso)
            case _:
                print("❌ Torta non valida.\n")
                return None
        
        if self.verifica_ingredienti(torta):
            # Consuma ingredienti per la torta
            for ingrediente in torta.ingredienti:
                if ingrediente in self.__ingredienti:
                    self.__ingredienti[ingrediente] -= 1  # Consuma 1 kg o 1 unità di ingrediente
                    print(f"✔️ Ingrediente {ingrediente} consumato. Quantità rimanente: {self.__ingredienti[ingrediente]}")

            self.__inventario[nome] = torta
            print(f"🎂 {torta.nome} da {peso}kg è stata aggiunta all'inventario.")
            self.mostra_inventario()
            return torta
        else:
            print("❌ Impossibile preparare la torta, ingredienti insufficienti.\n")
            return None

    def ordina_torta(self, peso, nome):
        nome = nome.lower()
        inventario = self.__inventario

        if nome in inventario and inventario[nome].peso == peso:
            print(f"✅ Torta {nome.capitalize()} trovata in inventario. Viene consegnata.")
            torta = inventario.pop(nome)
            return torta
        else:
            print(f"⏳ Torta non presente, la stiamo preparando su ordinazione...")
            # Tempo di preparazione simulato (2 secondi)
            time.sleep(2)
            return self.crea_torta(peso, nome)

    def mostra_inventario(self):
        print("\n--- INVENTARIO RIMANENTE ---")
        for ingrediente, quantita in self.__ingredienti.items():
            print(f"{ingrediente.capitalize()}: {quantita} unità")
        print()

# Classe Cliente
class Cliente():
    def __init__(self, nome, budget):
        self.nome = nome
        self.__budget = budget

    def get_budget(self):
        return self.__budget

    def set_budget(self, budget):
        self.__budget = budget

    def prenota_torta(self, pasticceria):
        peso = float(input("🔹 Inserisci il peso (in Kg) della torta: "))
        nome_torta = input("🔸 Inserisci il nome della torta: ")

        # Tempo di preparazione simulato (2 secondi)
        time.sleep(2)

        torta = pasticceria.ordina_torta(peso, nome_torta)
        if not torta:
            print("❌ Errore nell'ordinazione della torta.\n")
            return

        prezzo = torta.calcola_prezzo(torta.peso)
        print(f"💰 Prezzo della torta: €{prezzo:.2f}")

        if self.__budget >= prezzo:
            self.__budget -= prezzo
            pasticceria.registra_vendita(torta)
            print(f"🎉 Torta acquistata con successo! Budget residuo: €{self.__budget:.2f}\n")
        else:
            print("❌ Budget insufficiente per completare l'acquisto.\n")

# Funzione principale con menù
def main():
    pasticceria = Pasticceria()
    cliente = Cliente("Maurizio", 50)

    while True:
        print("\n--- MENU ---")
        print("1. Modalità pasticceria")
        print("2. Modalità cliente")
        print("3. Mostra saldo pasticceria")
        print("4. Esci")
        scelta = input("Scegli un'opzione: ")

        if scelta == "1":
            while True:
                print("\n--- MODALITÀ PASTICCERIA ---")
                print("1. Aggiungi una torta all'inventario")
                print("2. Rifornisci ingredienti")
                print("3. Torna al menu principale")
                scelta_pasticceria = input("Scegli un'opzione: ")

                if scelta_pasticceria == "1":
                    nome = input("🔹 Inserisci il nome della torta da aggiungere: ")
                    try:
                        peso = float(input("🔸 Inserisci il peso (in Kg): "))
                        pasticceria.crea_torta(peso, nome)
                    except ValueError:
                        print("❌ Peso non valido.\n")
                elif scelta_pasticceria == "2":
                    ingrediente = input("🔹 Inserisci il nome dell'ingrediente da rifornire: ")
                    try:
                        quantita = int(input("🔸 Inserisci la quantità da aggiungere: "))
                        pasticceria.rifornisci_ingredienti(ingrediente, quantita)
                    except ValueError:
                        print("❌ Quantità non valida.\n")
                elif scelta_pasticceria == "3":
                    break
                else:
                    print("❌ Scelta non valida.\n")
        
        elif scelta == "2":
            while True:
                print("\n--- MODALITÀ CLIENTE ---")
                print("1. Ordina una torta")
                print("2. Visualizza budget disponibile")
                print("3. Torna al menu principale")
                scelta_cliente = input("Scegli un'opzione: ")

                if scelta_cliente == "1":
                    cliente.prenota_torta(pasticceria)
                elif scelta_cliente == "2":
                    print(f"💵 Il tuo budget residuo è: €{cliente.get_budget():.2f}\n")
                elif scelta_cliente == "3":
                    break
                else:
                    print("❌ Scelta non valida.\n")

        elif scelta == "3":
            print(f"💰 Il saldo totale della pasticceria è: €{pasticceria.get_saldo():.2f}\n")

        elif scelta == "4":
            print("👋 Arrivederci!\n")
            break

        else:
            print("❌ Scelta non valida.\n")

if __name__ == "__main__":
    main()

