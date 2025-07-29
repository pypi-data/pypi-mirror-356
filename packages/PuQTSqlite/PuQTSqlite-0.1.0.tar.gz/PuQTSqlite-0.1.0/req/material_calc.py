def calc_material(prod_coeff, mat_defect, qty, param1, param2):
    """
    prod_coeff: коэффициент типа продукции (float)
    mat_defect: процент брака материала (float, например 0.01)
    qty: количество продукции (int)
    param1, param2: параметры продукции (float)
    Возвращает: int (количество материала) или -1 при ошибке
    """
    if qty <= 0 or param1 <= 0 or param2 <= 0:
        return -1
    try:
        base = param1 * param2 * prod_coeff * qty
        result = int(base * (1 + mat_defect) + 0.9999)  # округление вверх
        return result
    except Exception:
        return -1 