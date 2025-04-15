import cProfile
from tests.perf_scenarios import test_add_item, test_add_item_to_db, test_list_items_from_db

def run_profile():
    # Профілюємо функції
    print("Профілювання додавання елемента")
    cProfile.run('test_add_item()', 'perf_add_item.prof')
    
    # Профілюємо запити до БД
    print("Профілювання додавання елемента до БД")
    cProfile.run('test_add_item_to_db()', 'perf_add_item_to_db.prof')
    
    print("Профілювання отримання елементів з БД")
    cProfile.run('test_list_items_from_db()', 'perf_list_items_from_db.prof')

# Запуск профілювання
run_profile()
