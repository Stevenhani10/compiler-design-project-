def evaluate_expression(expression):
    def evaluate_term():
        nonlocal index
        result = evaluate_factor()

        while index < len(expression):
            if expression[index] == '*':
                index += 1
                result *= evaluate_factor()
            elif expression[index] == '/':
                index += 1
                result /= evaluate_factor()
            else:
                break

        return result

    def evaluate_factor():
        nonlocal index
        if expression[index] == '(':
            index += 1
            result = evaluate_expression()
            index += 1  # Skip closing parenthesis
        else:
            # Skip whitespace characters
            while index < len(expression) and expression[index].isspace():
                index += 1

            # Handle negative numbers
            if expression[index] == '-':
                index += 1
                return -evaluate_factor()

            # Extract the numeric literal
            start = index
            while index < len(expression) and expression[index].isdigit():
                index += 1
            if start == index:
                raise ValueError("Invalid expression")

            result = int(expression[start:index])

        return result

    def evaluate_expression():
        nonlocal index
        result = evaluate_term()

        while index < len(expression):
            if expression[index] == '+':
                index += 1
                result += evaluate_term()
            elif expression[index] == '-':
                index += 1
                result -= evaluate_term()
            else:
                break

        return result

    index = 0
    return evaluate_expression()

# Example usage:
expression = ['(', '10', '+', '(', '20', ')', '*', '2', ')', '', '6', '/', '7']
expression_string = ' '.join(expression)
result = evaluate_expression(expression_string)
print(result)  