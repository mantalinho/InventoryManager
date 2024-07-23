import datetime
import json
import os

class Drink:
    def __init__(self, name, starting_quantity, current_quantity=None, sales=0):
        self.name = name
        self.starting_quantity = starting_quantity
        self.current_quantity = current_quantity if current_quantity is not None else starting_quantity
        self.sales = sales

    def sell(self, quantity):
        if quantity <= self.current_quantity:
            self.current_quantity -= quantity
            self.sales += quantity
        else:
            print(f"Insufficient stock for {self.name}.")

    def restock_needed(self):
        return self.starting_quantity - self.current_quantity

    def to_dict(self):
        return {
            'name': self.name,
            'starting_quantity': self.starting_quantity,
            'current_quantity': self.current_quantity,
            'sales': self.sales
        }

    @staticmethod
    def from_dict(data):
        return Drink(data['name'], data['starting_quantity'], data['current_quantity'], data['sales'])

class Inventory:
    def __init__(self, filename='inventory.json'):
        self.drinks = {}
        self.filename = filename
        self.load()

    def add_drink(self, name, starting_quantity):
        self.drinks[name] = Drink(name, starting_quantity)
        self.save()

    def record_sales(self, name, quantity):
        if name in self.drinks:
            self.drinks[name].sell(quantity)
            self.save()
        else:
            print(f"Drink {name} not found in inventory.")

    def generate_report(self):
        print("\nInventory Report:")
        print(f"{'Drink':<20} {'Starting Quantity':<20} {'Current Quantity':<20} {'Sales':<20} {'Restock Needed':<20}")
        for drink in self.drinks.values():
            print(f"{drink.name:<20} {drink.starting_quantity:<20} {drink.current_quantity:<20} {drink.sales:<20} {drink.restock_needed():<20}")

    def save(self):
        data = {name: drink.to_dict() for name, drink in self.drinks.items()}
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.drinks = {name: Drink.from_dict(d) for name, d in data.items()}

def main():
    inventory = Inventory()

    while True:
        print("\n1. Add Drink")
        print("2. Record Sales")
        print("3. Generate Report")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter drink name: ")
            starting_quantity = int(input("Enter starting quantity: "))
            inventory.add_drink(name, starting_quantity)

        elif choice == '2':
            name = input("Enter drink name: ")
            quantity = int(input("Enter quantity sold: "))
            inventory.record_sales(name, quantity)

        elif choice == '3':
            inventory.generate_report()

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please try again.")

def scheduled_report():
    # Check if today is the day to generate a report (e.g., Sunday)
    if datetime.datetime.today().weekday() == 6:  # Sunday
        inventory = Inventory()
        inventory.generate_report()

if __name__ == "__main__":
    main()

    # Uncomment the following line to run the scheduled report function automatically
    # scheduled_report()