class CalculationNotFoundError(Exception):
    def __init__(self, category):
        super().__init__(f"calculation under the category '{category}' not found")