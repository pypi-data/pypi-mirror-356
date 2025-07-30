def get_all_materials(conn):
    sql = """SELECT m.*, mt.material_type as type_name
             FROM Materials m
             JOIN Material_type mt ON m.material_type_id = mt.id"""
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

def get_material_types(conn):
    sql = "SELECT id, material_type FROM Material_type"
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

def get_material_by_id(conn, material_id):
    sql = """SELECT m.*, mt.material_type as type_name
             FROM Materials m
             JOIN Material_type mt ON m.material_type_id = mt.id
             WHERE m.id = ?"""
    cur = conn.cursor()
    cur.execute(sql, (material_id,))
    return cur.fetchone()

def insert_material(conn, material_data):
    sql = """INSERT INTO Materials 
             (material_name, material_type_id, unit_price, stock_quantity, 
              min_quantity, package_quantity, unit_of_measure)
             VALUES (?, ?, ?, ?, ?, ?, ?)"""
    cur = conn.cursor()
    cur.execute(sql, (
        material_data['material_name'],
        material_data['material_type_id'],
        material_data['unit_price'],
        material_data['stock_quantity'],
        material_data['min_quantity'],
        material_data['package_quantity'],
        material_data['unit_of_measure']
    ))
    conn.commit()

def update_material(conn, material_data):
    sql = """UPDATE Materials SET
             material_name = ?,
             material_type_id = ?,
             unit_price = ?,
             stock_quantity = ?,
             min_quantity = ?,
             package_quantity = ?,
             unit_of_measure = ?
             WHERE id = ?"""
    cur = conn.cursor()
    cur.execute(sql, (
        material_data['material_name'],
        material_data['material_type_id'],
        material_data['unit_price'],
        material_data['stock_quantity'],
        material_data['min_quantity'],
        material_data['package_quantity'],
        material_data['unit_of_measure'],
        material_data['id']
    ))
    conn.commit()

def get_suppliers_for_material(conn, material_id):
    sql = """SELECT s.* 
             FROM Suppliers s
             JOIN Material_suppliers ms ON s.id = ms.supplier_id
             WHERE ms.material_id = ?
             ORDER BY s.rating DESC NULLS LAST, s.supplier_name"""
    cur = conn.cursor()
    cur.execute(sql, (material_id,))
    return cur.fetchall()

def get_product_types(conn):
    sql = "SELECT id, product_type, type_coefficient FROM Product_type"
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

def calculate_product_count(conn, product_type_id, material_type_id, 
                          material_qty, param1, param2):
    try:
        # Получаем данные о типах
        cur = conn.cursor()
        
        # Проверяем существование типов
        cur.execute("SELECT 1 FROM Product_type WHERE id = ?", (product_type_id,))
        if not cur.fetchone():
            return -1
            
        cur.execute("SELECT 1 FROM Material_type WHERE id = ?", (material_type_id,))
        if not cur.fetchone():
            return -1
        
        # Получаем коэффициенты
        cur.execute("SELECT type_coefficient FROM Product_type WHERE id = ?", 
                   (product_type_id,))
        product_coeff = cur.fetchone()[0]
        
        cur.execute("SELECT loss_percentage FROM Material_type WHERE id = ?", 
                   (material_type_id,))
        loss_percent = cur.fetchone()[0]
        
        # Расчет с учетом потерь
        material_per_unit = param1 * param2 * product_coeff
        effective_material = material_qty * (1 - loss_percent / 100)
        product_count = int(effective_material / material_per_unit)
        
        return product_count if product_count > 0 else 0
        
    except Exception:
        return -1