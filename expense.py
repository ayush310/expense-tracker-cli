from dataclasses import dataclass, asdict
import json
from datetime import datetime
from pathlib import Path


@dataclass
class Expense:
    amount: float
    category:str
    description: str
    date: str
    
    @staticmethod
    def validate_amount(amt):
        if amt <= 0:
            raise ValueError('Amount must be positive')
        
    @staticmethod
    def validate_category(category):
        if not category.strip():
            raise ValueError('Category cannot be empty')
    
    @staticmethod
    def validate_date(date):
        try:
            datetime.strptime(date,'%d-%m-%Y')
        except ValueError:
            raise ValueError("Invalid Date, expected DD-MM-YYYY")


class ExpenseTracker:
    
    def __init__(self, filepath = "expenses.json"):
        self.filepath = Path(filepath)
        self.expenses : list[Expense] = []
        self.load()
        
    def add(self, amt, cat, desc, date):
        Expense.validate_amount(amt)
        Expense.validate_category(cat)
        Expense.validate_date(date)
        expense = Expense(amt, cat, desc, date)
        self.expenses.append(expense)
        self.save()
        return expense
    
    def filter_by_category(self, category):
        return [e for e in self.expenses if e.category == category]
    
    def total(self):
        return sum(e.amount for e in self.expenses)
    
    def total_by_category(self):
        totals = {}
        for e in self.expenses:
            totals[e.category] = totals.get(e.category,0) + e.amount
        
        return totals  
      
    def delete(self,id):
        if id < 0 or id >= len(self.expenses):
            raise ValueError('Invalid Index')
            
        removed = self.expenses.pop(id)
        self.save()
        return removed
    
    def save(self):
        data = [asdict(e) for e in self.expenses]
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)
            
    def load(self):
        if not self.filepath.exists():
            self.expenses = []
            return
        with open(self.filepath,'r') as f:
           data = json.load(f)
        self.expenses = [Expense(**item) for item in data]
            
            
if __name__ == '__main__':
    tracker = ExpenseTracker()
    amount = float(input("Amount: "))
    category = input("Category: ")
    description = input("Description: ")
    date = input("Date (DD-MM-YYYY): ")
    tracker.add(amount, category, description, date)
    print(f"Total spent: {tracker.total()}")
    print(f"Total Category: {tracker.total_by_category()}")
    
