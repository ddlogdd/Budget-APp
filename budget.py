def create_spend_chart(categories):
  s = "Percentage spent by category\n"

  total = 0
  cats = {}
  for cat in categories:
    cat_total = 0
    for item in cat.ledger:
      amount = item["amount"]
      if amount < 0:
        total += abs(amount)
        cat_total += abs(amount)

    cats[cat.name] = cat_total

  cats = {
    k: (v / total) * 100
    for k, v in cats.items()
  }

  dash_width = len(cats) * 3 + 1
  spaces = dash_width - 1
  for n in range(100, -1, -10):
    s += f"{n:>3}| "
    bar_row = []
    for val in cats.values():
      row_val = [' '] * 3
      if val >= n:
        row_val[0] = "o"
      bar_row += row_val
    s += f"{''.join(bar_row)}{' ' * (spaces - len(bar_row))}\n"
    
  s += f"{' ' * 4}{'-' * dash_width}\n"

  cat_names = [list(name) for name in cats]
  while any(cat_names):
    s += f"{' ' * 4}"
    for name in cat_names:
      s += f" {' ' if not name else name.pop(0)} "
    s += " \n"
 
  s = s.strip() + '  '

  
  return s

class   Category:
  def __init__(self, name):
    self.name = name
    self.ledger = []
    self.total = 0

  def deposit(self, amount, description = ""):
    self.total = self.total + amount
    self.ledger.append({"amount":amount, "description":description})

  
  def withdraw(self, amount, description = ""):
    if self.check_funds(amount):
      self.total = self.total - amount
      self.ledger.append({"amount":-(amount), "description":description})
      return True
    else:
      return False
  
  def get_balance(self):
    return self.total

  def transfer(self, amount, category):
    if self.check_funds(amount):
      self.withdraw(amount,f"Transfer to {category.name}")
      category.deposit(amount, f"Transfer from {self.name}")
      return True
    else:
      return False

  def check_funds(self, amount):
    return amount <= self.total


  def get_withdrawals(self):
    total = 0
    for item in self.ledger:
      if item["amount"]<0:
        total+= item["amount"]
    return total



  
  def __repr__(self):
    s = f"{self.name:*^30}\n"
    acc = 0

    for item in self.ledger:
      s += f"{item['description'][:23]:<23}{item['amount']:>7.2f}\n"
      acc += item["amount"]

    s += f"Total: {self.total:.2f}"
    return s