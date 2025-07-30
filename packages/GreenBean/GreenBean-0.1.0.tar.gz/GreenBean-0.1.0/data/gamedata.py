import os
import json

class GreenBean:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            self.data = {}
            self.save_data()
        else:
            self.data = self.load_data()

    def save_data(self):
        """
        Save game data to a file in JSON format.
        """
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    def load_data(self):
        """
        Load game data from a JSON file.
        
        :return: Dictionary containing game data
        """
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("The file contains invalid JSON. Replacing it with an empty dictionary.")
            self.save_data()
            return {}

    def add_data(self, new_key, new_value):
        """
        Add a new key-value pair to the game data.
        
        :param new_key: Key for the new data entry
        :param new_value: Value for the new data entry
        """
        if new_key in self.data:
            print(f"Key '{new_key}' already exists. Overwriting...")
        self.data[new_key] = new_value
        self.save_data()
        print(f"Data added for key: {new_key}")

    def remove_data(self, key_to_remove):
        """
        Remove a key-value pair from the game data.
        
        :param key_to_remove: Key to remove from the data
        """
        if key_to_remove in self.data:
            del self.data[key_to_remove]
            self.save_data()
            print(f"Data removed for key: {key_to_remove}")
        else:
            print(f"Key '{key_to_remove}' not found.")

# Example usage:
if __name__ == "__main__":
    filename = "game_data.json"
    game_manager = GreenBean(filename)
    
    # Load existing data
    print("Current game data:", game_manager.data)
    
    # Add new data
    game_manager.add_data("score", 100)
    print("Game data after adding score:", game_manager.data)
    
    # Remove data
    game_manager.remove_data("score")
    print("Game data after removing score:", game_manager.data)