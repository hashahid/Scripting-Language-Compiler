from globals import global_scope, function_name_to_body


class SemanticError(Exception):
    """
    This is the class of the exception that is raised when a semantic error occurs.
    """


# These are the nodes of the abstract syntax tree.
class Node(object):
    """
    A base class for nodes. All other classes here subclass this.
    """

    def execute(self):
        """
        Executes this node.
        """
        raise Exception("Not implemented.")

    def evaluate(self):
        """
        Called on children of Node to evaluate that child.
        """
        raise Exception("Not implemented.")

    def location(self):
        """
        Evaluates this node for a location.
        """
        raise Exception("Not implemented.")


class IntLiteral(Node):
    """
    A node representing integer literals.
    """

    def __init__(self, value):
        self.value = int(value)

    def evaluate(self):
        return self.value

    def execute(self):
        return self.evaluate()


class StringLiteral(Node):
    """
    A node representing string literals.
    """

    def __init__(self, value):
        self.value = str(value)
        self.value = self.value[1:len(self.value) - 1]

    def evaluate(self):
        return self.value

    def execute(self):
        return self.evaluate()


class Add(Node):
    """
    A node representing addition.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not ((isinstance(left, int) and isinstance(right, int)) or (isinstance(left, str) and isinstance(right, str))):
            raise SemanticError("addition operands must both be integers or both be strings")
        return left + right

    def execute(self):
        return self.evaluate()


class And(Node):
    """
    A node representing boolean AND.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int) or not isinstance(right, int):
            raise SemanticError("\"and\" operands must be integers")
        if left == 0 or right == 0:
            return 0
        else:
            return 1

    def execute(self):
        return self.evaluate()


class Assign(Node):
    """
    A node representing the assignment statement.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def execute(self):
        if isinstance(self.left, VarIndex):
            var, index = self.left.location()
            global_scope[var][index] = self.right.execute()
        else:
            global_scope[self.left.location()] = self.right.execute()


class Block(Node):
    """
    A node representing the block statement.
    """

    def __init__(self, statement1, statement2):
        self.statement1 = statement1
        self.statement2 = statement2

    def evaluate(self):
        statements = []
        if self.statement1 is not None:
            if isinstance(self.statement1, list):
                statements.extend(self.statement1)
            else:
                statements.append(self.statement1)
        if self.statement2 is not None:
            statements.append(self.statement2)
        for statement in statements:
            if statement is not None:
                statement.execute()

    def execute(self):
        self.evaluate()


class Divide(Node):
    """
    A node representing division.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int) or not isinstance(right, int):
            raise SemanticError("division operands must be integers")
        if right == 0:
            raise SemanticError("division by zero")
        return int(left / right)

    def execute(self):
        return self.evaluate()


class GreaterThan(Node):
    """
    A node representing greater than comparison.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int) or not isinstance(right, int):
            raise SemanticError("\">\" operands must be integers")
        if left > right:
            return 1
        else:
            return 0

    def execute(self):
        return self.evaluate()


class If(Node):
    """
    A node representing the if statement.
    """

    def __init__(self, expression, statement):
        self.expression = expression
        self.statement = statement

    def evaluate(self):
        if self.expression.evaluate() == 0:
            return
        else:
            self.statement.execute()

    def execute(self):
        self.evaluate()


class IsEqual(Node):
    """
    A node representing equality comparison.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int) or not isinstance(right, int):
            raise SemanticError("\"==\" operands must be integers")
        if left == right:
            return 1
        else:
            return 0

    def execute(self):
        return self.evaluate()


class LessThan(Node):
    """
    A node representing less than comparison.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int) or not isinstance(right, int):
            raise SemanticError("\"<\" operands must be integers")
        if left < right:
            return 1
        else:
            return 0

    def execute(self):
        return self.evaluate()


class ListIndex(Node):
    """
    A node representing getting element at index of list.
    """

    def __init__(self, my_list, index):
        # The nodes representing the left and right sides of this
        # operation.
        self.list = my_list
        self.index = index

    def evaluate(self):
        my_list = self.list.evaluate()
        index = self.index.evaluate()
        if not isinstance(index, int):
            raise SemanticError("lists must be indexed by integers")
        return my_list[index]

    def execute(self):
        return self.evaluate()


class MakeEmptyList(Node):
    """
    A node representing the creation of an empty list.
    """

    def evaluate(self):
        return []

    def execute(self):
        return self.evaluate()


class MakeList(Node):
    """
    A node representing the creation of a list.
    """

    def __init__(self, element1, element2):
        # The nodes representing the left and right sides of this
        # operation.
        self.element1 = element1
        self.element2 = element2

    def evaluate(self):
        l = []
        if self.element1 is not None:
            element1 = self.element1.evaluate()
        if self.element2 is not None:
            element2 = self.element2.evaluate()
        if depth(element1) > depth(element2):
            l.extend(element1)
        else:
            l.append(element1)
        l.append(element2)
        return l

    def execute(self):
        return self.evaluate()


class MakeSingleElementList(Node):
    """
    A node representing the creation of a list with only one element.
    """

    def __init__(self, element):
        # The nodes representing the right side of this
        # operation.
        self.element = element

    def evaluate(self):
        l = []
        if self.element is not None:
            element = self.element.evaluate()
            l.append(element)
        return l

    def execute(self):
        return self.evaluate()


class Multiply(Node):
    """
    A node representing multiplication.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int) or not isinstance(right, int):
            raise SemanticError("multiplication operands must be integers")
        return left * right

    def execute(self):
        return self.evaluate()


class Not(Node):
    """
    A node representing boolean NOT.
    """

    def __init__(self, operand):
        # The node representing the right side of this
        # operation.
        self.operand = operand

    def evaluate(self):
        operand = self.operand.evaluate()
        if not isinstance(operand, int):
            raise SemanticError("\"not\" operand must be an integer")
        if operand == 0:
            return 1
        else:
            return 0

    def execute(self):
        return self.evaluate()


class Or(Node):
    """
    A node representing boolean OR.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int) or not isinstance(right, int):
            raise SemanticError("\"or\" operands must be integers")
        if left == 0 and right == 0:
            return 0
        else:
            return 1

    def execute(self):
        return self.evaluate()


class Print(Node):
    """
    A node representing the print statement.
    """

    def __init__(self, expression):
        self.expression = expression

    def execute(self):
        print(repr(self.expression.evaluate()))


class StringIndex(Node):
    """
    A node representing getting character at index of string.
    """

    def __init__(self, string, index):
        # The nodes representing the left and right sides of this
        # operation.
        self.string = string
        self.index = index

    def evaluate(self):
        string = self.string.evaluate()
        index = self.index.evaluate()
        if not isinstance(index, int):
            raise SemanticError("strings must be indexed by integers")
        return string[index]

    def execute(self):
        return self.evaluate()


class Subtract(Node):
    """
    A node representing subtraction.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int) or not isinstance(right, int):
            raise SemanticError("subtraction operands must be integers")
        return left - right

    def execute(self):
        return self.evaluate()


class Variable(Node):
    """
    A node representing access to a variable.
    """

    def __init__(self, name):
        self.name = str(name)

    def execute(self):
        return self.evaluate()

    def evaluate(self):
        if self.name not in global_scope:
            raise SemanticError("name '" + self.name + "' is not defined")
        return global_scope[self.name]

    def location(self):
        return self.name


class VarIndex(Node):
    """
    A node representing getting element at index of list.
    """

    def __init__(self, var, index):
        # The nodes representing the left and right sides of this
        # operation.
        self.var = var
        self.index = index

    def evaluate(self):
        var = self.var.evaluate()
        index = self.index.evaluate()
        if not isinstance(var, list):
            raise SemanticError()
        if not isinstance(index, int):
            raise SemanticError("variables must be indexed by integers")
        if index >= len(var) and isinstance(var, list):
            raise SemanticError("list index is out of range")
        return var[index]

    def execute(self):
        return self.evaluate()

    def location(self):
        return self.var.location(), self.index.evaluate()


class While(Node):
    """
    A node representing the while statement.
    """

    def __init__(self, expression, statement):
        self.expression = expression
        self.statement = statement

    def evaluate(self):
        while self.expression.evaluate() != 0:
            self.statement.execute()

    def execute(self):
        self.evaluate()


class Xor(Node):
    """
    A node representing xor.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int) or not isinstance(right, int):
            raise SemanticError("\"xor\" operands must be integers")
        return left ^ right

    def execute(self):
        return self.evaluate()


# ----------------------------------------------------- NEEDS WORK -----------------------------------------------------
# TODO: Update ListIndex to throw semantic error when "list index is out of range" <-- use quotes as error msg
# TODO: Update VarIndex to support string indexing in addition to list indexing, update error msgs as appropriate
# TODO: Implement >= and <= functionality
# TODO: code reorganization, comment cleanup, and better comments/docstrings
# TODO: Find a less hacky way to implement lists and blocks, hopefully support lists of lists with different depths
# TODO: if above TODO doesn't solve it, figure out why variable assignments don't work unless wrapped in curly brackets
# TODO: work on the following 2 classes and implement return statements

class FunctionBody(Node):
    """
    A node representing function bodies.
    """

    def __init__(self, name, parameter, body):
        # The nodes representing the function name, parameter, and body
        self.name = name
        self.parameter = parameter
        self.body = body

    def evaluate(self):
        print("In the FunctionBody node")
        function_name_to_body[self.name.location()] = self.body
        function_name_to_body[self.name.location()].execute()

    def execute(self):
        self.evaluate()


class IfElse(Node):
    """
    A node representing an if-else statement.
    """

    def __init__(self, condition, if_body, else_body):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

    def evaluate(self):
        if self.condition.evaluate() == 1:
            self.if_body.execute()
        else:
            self.else_body.execute()

    def execute(self):
        self.evaluate()


def depth(l):
    """
    A recursive function for returning depth of nested list. For example, depth([[2, 5], [3, 3]]) returns 2
    :param l: The list whose depth is to be evaluated
    :return: the depth of the list
    """
    if isinstance(l, list):
        return 1 + max(depth(item) for item in l)
    else:
        return 0
