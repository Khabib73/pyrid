import ast

type FuncNode = ast.FunctionDef | ast.AsyncFunctionDef
type FuncClassNode = FuncNode | ast.ClassDef
