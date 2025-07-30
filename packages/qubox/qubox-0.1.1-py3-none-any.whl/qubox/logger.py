import os

class Logger:
    def __init__(self):
        # Dictionary to hold logs; each key stores a list of messages.
        self.logs = {}

    def log(self, message, key=None):
        """
        Adds a log message under the given key.
        
        Args:
            message (str): The log message to store.
            key (str): The key specifying where the log message should be stored.
        """
        if key:
            if key not in self.logs:
                self.logs[key] = []
            self.logs[key].append(message)

        print(message)
        #print(f"Logged message under key '{key}'.")

    def view_log(self, key):
        """
        Prints all log messages corresponding to the given key.
        
        Args:
            key (str): The log key for which messages are to be displayed.
        """
        if key not in self.logs:
            print(f"No logs available for key: '{key}'")
            return
        
        print(f"Logs for key '{key}':")
        for idx, message in enumerate(self.logs[key], start=1):
            print(f"{idx}. {message}")

    def save_log(self, key, path):
        """
        Saves log messages corresponding to the given key into a file.
        
        Args:
            key (str): The log key whose messages will be saved.
            path (str): The file path where the log should be saved.
        """
        if key not in self.logs:
            print(f"No logs available for key: '{key}'")
            return

        try:
            with open(path, "w") as file:
                for message in self.logs[key]:
                    file.write(message + "\n")
            print(f"Logs for key '{key}' have been saved to {os.path.abspath(path)}")
        except Exception as e:
            print(f"Failed to save logs for key '{key}' due to error: {e}")

# Example usage:
if __name__ == "__main__":
    logger = Logger()
    
    # Logging messages under different keys.
    logger.log("This is an info message.", "info")
    logger.log("This is a warning message.", "warning")
    logger.log("Another info message.", "info")
    
    # Viewing logs.
    logger.view_log("info")
    logger.view_log("warning")
    
    # Saving logs to file.
    logger.save_log("info", "info_logs.txt")
    logger.save_log("warning", "warning_logs.txt")
