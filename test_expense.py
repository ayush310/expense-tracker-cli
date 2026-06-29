import pytest
from expense import Expense, ExpenseTracker

def test_add_expense_updates_total(tmp_path):
    tracker = ExpenseTracker(filepath=tmp_path/'test.json')
    tracker.add(30.5, 'Grocery', '', '22-6-2026' )
    tracker.add(200, 'Travel', 'Cab', '30-6-2026')
    assert tracker.total() == 230.5
    
def test_negative_amount():
    with pytest.raises(ValueError):
        Expense.validate_amount(-20)
        
def test_empty_category_raises():
    with pytest.raises(ValueError):
        Expense.validate_category("   ")

def test_filter_by_category(tmp_path):
    tracker = ExpenseTracker(filepath=tmp_path/'test.json')
    tracker.add(30.5, 'Grocery', '', '22-6-2026' )
    tracker.add(200, 'Travel', 'Cab', '30-6-2026')
    tracker.add(100, 'Food', 'Cab', '10-6-2026')
    food_expense = tracker.filter_by_category('Food')
    assert len(food_expense) == 1
    assert food_expense[0].amount == 100
    
def test_load_and_save(tmp_path):
    filepath = tmp_path/'test.json'
    tracker1 = ExpenseTracker(filepath=filepath)
    tracker1.add(275, "Food", "", "25-06-2026")

    tracker2 = ExpenseTracker(filepath=filepath)  
    print(tracker2)
    assert tracker2.total() == 275
    assert len(tracker2.expenses) == 1    
    
def test_delete_expense(tmp_path):
    tracker = ExpenseTracker(filepath=tmp_path/'test.json')
    tracker.add(30.5, 'Grocery', '', '22-6-2026' )
    tracker.add(200, 'Travel', 'Cab', '30-6-2026')
    tracker.add(100, 'Food', 'Cab', '10-6-2026')
    removed = tracker.delete(1)
    assert removed.amount == 200
    assert len(tracker.expenses) == 2
    
def test_total_by_category(tmp_path):
    tracker = ExpenseTracker(filepath=tmp_path/'test.json')
    tracker.add(30.5, 'Grocery', '', '22-6-2026' )
    tracker.add(200, 'Travel', 'Cab', '30-6-2026')
    tracker.add(100, 'Food', 'Cab', '10-6-2026')
    assert tracker.total_by_category() == {'Grocery': 30.5, 'Travel': 200, 'Food': 100}

