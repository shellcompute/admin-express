from sqlalchemy.sql.elements import Cast
from sqlalchemy.types import String
from sqlalchemy.ext.compiler import compiles
# from flask_sqlalchemy import SQLAlchemy


@compiles(Cast, "oracle")
def visit_cast(element, compiler, **kwargs):
    """
    Oracle compiler interceptor，intercept visit_cast method, to solve the problem when Oracle executing CAST function.
     The generated SQL: CAST(table.column AS VARCHAR2), is not available to execute.
     Instead, when the element is type of String, CAST is unnecessary.
    :param element: Cast object, String type Cast interceptor
    :param compiler: OracleCompiler
    """
    if isinstance(element.type, String):
        return compiler.process(element.clause, **kwargs)

    return compiler.visit_cast(element, **kwargs)
