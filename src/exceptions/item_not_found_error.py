class ItemNotFoundError(Exception):
    def __init__(self, category: str = None, season: str = None):
        # Initialize the error message based on the provided parameters
        if category and season:
            message = f"Items with category '{category}' and season '{season}' not found."
        elif category:
            message = f"Items with category '{category}' not found."
        elif season:
            message = f"Items with season '{season}' not found."
        else:
            message = "No items found in the database."

        # Initialize the base Exception class with the message
        super().__init__(message)