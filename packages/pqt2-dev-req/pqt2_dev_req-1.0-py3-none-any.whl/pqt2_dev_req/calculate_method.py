class ProductionCalculatorVM:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def calculate_product_quantity(self, product_type_id, material_type_id,
                                raw_material_quantity, param1, param2):
        
        if not all(isinstance(arg, (int, float)) for arg in [product_type_id, material_type_id, 
                                                          raw_material_quantity, param1, param2]):
            return -1
            
        if raw_material_quantity < 0 or param1 <= 0 or param2 <= 0:
            return -1

        product_data = self.db_manager.execute_query(
            "SELECT type_coefficient FROM Product_type WHERE id = ?",
            (product_type_id,), 
            fetch_one=True
        )
        if not product_data:
            return -1
        type_coef = product_data['type_coefficient']

        material_data = self.db_manager.execute_query(
            "SELECT loss_percentage FROM Material_type WHERE id = ?",
            (material_type_id,),
            fetch_one=True
        )
        if not material_data:
            return -1
        loss_pct = material_data['loss_percentage'] / 100.0

        base_usage = param1 * param2 * type_coef
        
        if loss_pct >= 1.0:
            return 0
            
        usage_with_loss = base_usage / (1.0 - loss_pct)
        
        if usage_with_loss == 0:
            return 0
            
        return int(raw_material_quantity / usage_with_loss)



class ProductionCalculatorVS:
    def __init__(self, db_connection):
        self.db_connection = db_connection
    
    def calculate_production(self, product_type_id, material_type_id, material_qty, param1, param2):
        try:
            if (not isinstance(material_qty, int) or material_qty <= 0:
                return -1
                
            if (not isinstance(param1, (int, float)) or param1 <= 0:
                return -1
                
            if (not isinstance(param2, (int, float)) or param2 <= 0:
                return -1
            
            product_coeff = self._get_product_coefficient(product_type_id)
            if product_coeff is None:
                return -1
                
            loss_percent = self._get_material_loss_percent(material_type_id)
            if loss_percent is None:
                return -1
            
            material_per_unit = param1 * param2 * product_coeff
            if material_per_unit <= 0:
                return -1
                
            effective_material = material_qty * (1 - loss_percent / 100)
            if effective_material <= 0:
                return 0
                
            production_count = int(effective_material / material_per_unit)
            
            return max(0, production_count)
            
        except Exception:
            return -1
    
    def _get_product_coefficient(self, product_type_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT type_coefficient FROM Product_type WHERE id = ?",
                (product_type_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception:
            return None
    
    def _get_material_loss_percent(self, material_type_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT loss_percentage FROM Material_type WHERE id = ?",
                (material_type_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception:
            return None