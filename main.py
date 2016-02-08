import sys
import tpg

from nodes import *


# This is the TPG Parser that is responsible for turning the language into
# an abstract syntax tree.
class Parser(tpg.Parser):
    """
    token int "\d+" IntLiteral;
    token str "\\"([^\\"])*\\"" StringLiteral;
    token variable "[A-Za-z][A-Za-z0-9]*" Variable;
    separator space "\s";

    START/a -> (statement/a)*
    ;

    statement/a -> "\{" (statement/a (statement/b $ a = Block(a, b) $ )* )* "\}"
    | expression/l "=(?!=)" expression/r ";" $ a = Assign(l, r) $
    | "print" "\(" expression/e "\)" ";" $ a = Print(e) $
    | "if" "\(" expression/c "\)" statement/s "else" statement/t $ a = IfElse(c, s, t) $
    | "if" "\(" expression/e "\)" statement/s $ a = If(e, s) $
    | "while" "\(" expression/e "\)" statement/s $ a = While(e, s) $
    | expression/n "\(" expression/p "\)" statement/b $ a = FunctionBody(n, p, b) $
    ;

    expression/a -> boolean/a
    ;

    boolean/a -> ("not") boolean/a $ a = Not(a) $ | comparison/a
    ( "and" comparison/b $ a = And(a, b) $
    | "or" comparison/b $ a = Or(a, b) $
    )*;

    comparison/a -> bitwiseexpr/a
    ( "\<" bitwiseexpr/b $ a = LessThan(a, b) $
    | ">" bitwiseexpr/b $ a = GreaterThan(a, b) $
    | "\=\=" bitwiseexpr/b $ a = IsEqual(a, b) $
    )* ;

    bitwiseexpr/a -> addsub/a
    ( "xor" addsub/b $ a = Xor(a, b) $
    )* ;

    addsub/a -> muldiv/a
    ( "\+" muldiv/b $ a = Add(a, b) $
    | "-"  muldiv/b $ a = Subtract(a, b) $
    )* ;

    muldiv/a -> parens/a
    ( "\*" parens/b $ a = Multiply(a, b) $
    | "/"  parens/b $ a = Divide(a, b) $
    )* ;

    parens/a -> "\(" expression/a "\)" | literal/a
    ;

    literal/a -> int/a | stringindexing/a | listindexing/a | varindexing/a
    | variable/a;

    stringindexing/a -> str/a
    ( "\[" boolean/b "\]" $ a = StringIndex(a, b) $
    )*;

    listindexing/a -> list/a
    ( "\[" boolean/b "\]" $ a = ListIndex(a, b) $
    )*;

    list/a -> "\[" "\]" $ a = MakeEmptyList() $
    | "\[" (expression/a) "\]" $ a = MakeSingleElementList(a) $
    | "\[" (expression/a ("," expression/b $ a = MakeList(a, b) $ )*) "\]"
    ;

    varindexing/a -> variable/a
    ( "\[" boolean/b "\]" $ a = VarIndex(a, b) $
    )*;
    """

parse = Parser()

try:
    f = open(sys.argv[1], "r")
except(IndexError, IOError):
    f = open("sample inputs/test.txt", "r")

code = f.read()

try:
    node = parse(code)
    print(repr(node))
    node.execute()

# If an exception is thrown, print the appropriate error.
except (tpg.Error, MySyntaxError):
    print("SYNTAX ERROR")
    # Uncomment the next line to re-raise the syntax error,
    # displaying where it occurs. Comment it for submission.
    # raise

except SemanticError:
    print("SEMANTIC ERROR")
    # Uncomment the next line to re-raise the semantic error,
    # displaying where it occurs. Comment it for submission.
    # raise

f.close()
