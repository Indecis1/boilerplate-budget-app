import math


class Category:

  def __init__(self, name):
    self.name = name
    self.ledger = []

  def deposit(self, amount: float, description: str = "") -> None:
    self.ledger.append({
        "amount": float(amount),
        "description": description
    })

  def withdraw(self, amount: float, description: str = "") -> bool:
    if self.check_funds(amount):
        self.ledger.append({
            "amount": float(-amount),
            "description": description
        })
        return True
    else:
        return False

  def get_balance(self) -> float:
    balance = 0
    for transaction in self.ledger:
        balance += transaction["amount"]
    return balance

  def transfer(self, amount: float, category) -> bool:
    if self.check_funds(amount):
        description_destination = "Transfer to " + category.name
        description_origin = "Transfer from " + self.name
        self.withdraw(float(amount), description_destination)
        category.deposit(float(amount), description_origin)
        return True
    else:
        return False

  def check_funds(self, amount: float) -> bool:
    if amount > self.get_balance():
        return False
    else:
        return True

  def total_withdrawals(self):
    balance = 0
    for transaction in self.ledger:
        if transaction["amount"] < 0:
            balance += transaction["amount"]
    return -balance

  def __str__(self):
    lines = ""
    asterisk = "*" * ((30 - len(self.name)) // 2)
    lines += asterisk + self.name + asterisk + "\n"
    for transaction in self.ledger:
        amount = "%.2f"%transaction["amount"]
        line = transaction["description"][:23]
        line += " " * (30 - len(line) - len(amount[:7]))
        line += amount[:7] + "\n"
        lines += line
    lines += "Total: " + str(self.get_balance())
    return lines


def round_down(x):
  return int(math.floor(x / 10.0)) * 10


def create_spend_chart(categories):
  result = ""
  names = [" " * 5] * max([len(category.name) for category in categories])
  lines = [
      "100| ", " 90| ", " 80| ", " 70| ", " 60| ", " 50| ", " 40| ", " 30| ", " 20| ", " 10| ", "  0| "
  ]
  total = 0
  for category in categories:
      total += category.total_withdrawals()
  for category in categories:
      percentage = round_down((category.total_withdrawals() / total) * 100)
      start = len(lines) - int(percentage / 10) - 1
      end = len(lines)
      for i in range(start, end):
          lines[i] += "o  "
      for i in range(start):
          lines[i] += " " * 3
      for i, name in enumerate(category.name):
          names[i] += category.name[i] + " " * 2
      for i in range(len(category.name), len(names)):
          names[i] += " " * 3
  result += "Percentage spent by category\n"
  result += "\n".join(lines) + "\n"
  result += " " * 4 + "-" * (len(lines[0]) - 4) + "\n"
  result += "\n".join(names)
  return result
