from app import get_db


def get_categories():
    c = get_db().cursor()
    c.execute("SELECT id, name FROM categories")
    return c.fetchall()


def get_subcategories(category_id=0):
    c = get_db().cursor()
    query = "SELECT id, name FROM subcategories"
    if category_id > 0:
        c.execute(query + " WHERE category_id = ?", (category_id,))
    else:
        c.execute(query)
    return c.fetchall()


def _row_to_item(row):
    try:
        item = dict(zip(
            ["id", "title", "description", "price", "image", "category", "subcategory"],
            row)
        )
    except:
        item = None

    return item


def get_items(*, title=None, category_id=0, subcategory_id=0, order=0):
    filters = []
    parameters = []

    # filters & parameters
    if title:
        filters.append("i.title LIKE ?")
        parameters.append("%" + title + "%")
    if category_id:
        filters.append("i.category_id = ?")
        parameters.append(category_id)
    if subcategory_id:
        filters.append("i.subcategory_id = ?")
        parameters.append(subcategory_id)

    query = """SELECT
                    i.id, i.title, i.description, i.price, i.image, c.name, s.name
                    FROM
                    items AS i
                    INNER JOIN categories AS c ON i.category_id = c.id
                    INNER JOIN subcategories AS s ON i.subcategory_id = s.id
    """

    if filters:
        query += " WHERE "
        query += " AND ".join(filters)

    # order by clause
    if order == 1:
        query += " ORDER BY i.price DESC"
    elif order == 2:
        query += " ORDER BY i.price"
    else:
        query += " ORDER BY i.id DESC"

    c = get_db().cursor()
    items_iter = c.execute(query, parameters)
    items = []
    for row in items_iter:
        if item := _row_to_item(row):  # python3.8
            items.append(item)
    return items


def get_item(item_id):
    c = get_db().cursor()
    c.execute("""SELECT
                   i.id, i.title, i.description, i.price, i.image, c.name, s.name
                   FROM
                   items AS i
                   INNER JOIN categories AS c ON i.category_id = c.id
                   INNER JOIN subcategories AS s ON i.subcategory_id = s.id
                   WHERE i.id = ?""", (item_id,))
    row = c.fetchone()
    return _row_to_item(row)


def get_item_no_categories(item_id):  # とりあえず
    c = get_db().cursor()
    c.execute(
        "SELECT id, title, description, price, image FROM items WHERE id = ?",
        (item_id,)
    )
    row = c.fetchone()
    return _row_to_item(row)


def create_item(*, title, description, price, image, category_id, subcategory_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("""INSERT INTO items
                (title, description, price, image, category_id, subcategory_id)
                VALUES(?,?,?,?,?,?)""",
              (title, description, price, image, category_id, subcategory_id,))
    conn.commit()


def update_item(item_id, *, title, description, price, image):
    conn = get_db()
    c = conn.cursor()
    c.execute("""UPDATE items
            SET title = ?, description = ?, price = ?, image = ?
            WHERE id = ?""", (title, description, price, image, item_id,))
    conn.commit()


def delete_item(item_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()


def get_comments(item_id):
    c = get_db().cursor()
    comments_from_db = c.execute("""SELECT content FROM comments
                WHERE item_id = ? ORDER BY id DESC""", (item_id,))
    comments = []
    for row in comments_from_db:
        comment = {"content": row[0]}
        comments.append(comment)
    return comments


def create_comment(item_id, *, content):
    conn = get_db()
    c = conn.cursor()
    c.execute("""INSERT INTO comments (content, item_id)
                 VALUES (?,?)""", (content, item_id,))
    conn.commit()
