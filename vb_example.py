
import sys

class DataOperation:
    def perform_operation(self, input_value):
        pass

class AdditionOperation(DataOperation):
    def perform_operation(self, input_value):
        return input_value + 10

class SubtractionOperation(DataOperation):
    def perform_operation(self, input_value):
        return input_value - 5

def update_database(operation_name, input_value, output_value):
    print(f"Updating database with operation: {operation_name}, Input: {input_value}, Output: {output_value}")

def main():
    try:
        print("Welcome to Data Operation Program")

        operation_type = input("Enter operation type (A for Addition, S for Subtraction): ").upper()
        
        if operation_type not in ["A", "S"]:
            print("Invalid operation type.")
            return

        if operation_type == "A":
            operation = AdditionOperation()
        elif operation_type == "S":
            operation = SubtractionOperation()

        input_number = int(input("Enter a number: "))
        output_number = operation.perform_operation(input_number)

        print(f"Result: {output_number}")

        update_database(operation_type, input_number, output_number)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
