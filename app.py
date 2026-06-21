from datebase import init_db, get_all_recipes, add_recipes, delete_recipes, update_recipes, get_recipes, get_sort_soup, get_sort_salad, get_sort_desserts
from flask import Flask, request, render_template, redirect


app = Flask(__name__)
init_db()


@app.route('/')
def index():
    """
    Просмотр всех рецептов
    """
    recipes = get_all_recipes()
    return render_template(
        'index.html', recipes=recipes,
    )


@app.route('/detail/<int:item_id>', methods=['GET'])
def get_recipe(item_id):
    """
    Просмотр одного рецепта
    """
    recipe = get_recipes(item_id)
    return render_template('detail.html', recipe=recipe)


@app.route('/add', methods=['POST'])
def add_recipe():
    """
    Добавление рецептов
    """
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    ingredients = request.form.get("ingredients", "").strip()
    cooking = request.form.get("cooking", "").strip()
    time = request.form.get("time", "").strip()
    if name and category and ingredients and cooking and time:
        add_recipes(name, category, ingredients, cooking, time)
    return redirect("/")


@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_recipe(item_id):
    """
    Обновление рецептов
    """
    if request.method == 'POST':
        name = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        ingredients = request.form.get("ingredients", "").strip()
        cooking = request.form.get("cooking", "").strip()
        time = request.form.get("time", "").strip()
        update_recipes(name, category, ingredients, cooking, time, item_id)
        return redirect('/')
    return render_template('edit.html', recipe=item_id)


@app.route('/delete/<int:item_id>')
def delete_recipe(item_id):
    """
    Удаление рецептов
    """
    delete_recipes(item_id)
    return redirect("/")


@app.route('/search')
def search():
    """
    Поиск по названию
    """
    recipes = get_all_recipes()
    query = request.args.get('q', '').strip().lower()
    if query:
        filtered_recipes = [recipe for recipe in recipes if query in recipe['name'].lower()]
    else:
        filtered_recipes = recipes
    return render_template('index.html', recipes=filtered_recipes, search_query=query)


@app.route('/sort/soup')
def sort_by_soup():
    """
    Фильтрация супов
    """
    sort_recipes = get_sort_soup()
    return render_template('index.html', recipes=sort_recipes)


@app.route('/sort/salad')
def sort_by_salad():
    """
    Фильтрация салатов
    """
    sort_recipes = get_sort_salad()
    return render_template('index.html', recipes=sort_recipes)


@app.route('/sort/desserts')
def sort_by_desserts():
    """
    Фильтрация десертов
    """
    sort_recipes = get_sort_desserts()
    return render_template('index.html', recipes=sort_recipes)


if __name__ == '__main__':
    app.run(debug=True)