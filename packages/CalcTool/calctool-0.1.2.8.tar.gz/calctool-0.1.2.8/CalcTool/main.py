from typing import *
from decimal import *
from fractions import Fraction
import re, math, heapq

def sort(arr: List[Any], key: Callable[[Any], Any] = lambda x: x, reverse: bool = False) -> None:
	"""使用内省排序对列表进行原地排序"""
	if len(arr) <= 1:
		return  # 已经有序或为空
	
	# 比较函数 - 使用 lambda 避免类型变量问题
	compare = lambda a, b: key(a) > key(b) if reverse else key(a) < key(b)
	
	# 计算最大递归深度
	max_depth = 2 * math.log2(len(arr)) if len(arr) > 0 else 0
	
	# 内省排序主循环
	def introsort(start: int, end: int, depth: float) -> None:
		while start < end:
			# 小规模数据使用插入排序
			if end - start <= 16:
				for i in range(start + 1, end + 1):
					current = arr[i]
					j = i - 1
					while j >= start and compare(current, arr[j]):
						arr[j + 1] = arr[j]
						j -= 1
					arr[j + 1] = current
				return
			
			# 递归深度过大时使用堆排序
			if depth <= 0:
				heap_size = end - start + 1
				
				# 构建堆
				for i in range(heap_size // 2 - 1, -1, -1):
					heapify(start, heap_size, i)
				
				# 一个个交换元素
				for i in range(heap_size - 1, 0, -1):
					arr[start], arr[start + i] = arr[start + i], arr[start]
					heapify(start, i, 0)
				return
			
			# 否则使用快速排序
			mid = (start + end) // 2
			a, b, c = start, mid, end
			
			# 三数取中法
			if compare(arr[b], arr[a]):
				arr[a], arr[b] = arr[b], arr[a]
			if compare(arr[c], arr[b]):
				arr[b], arr[c] = arr[c], arr[b]
			if compare(arr[b], arr[a]):
				arr[a], arr[b] = arr[b], arr[a]
			
			# 将基准值放到开头
			arr[start], arr[mid] = arr[mid], arr[start]
			pivot = arr[start]
			
			# 分区过程
			left = start + 1
			right = end
			
			while True:
				while left <= right and compare(arr[left], pivot):
					left += 1
				while left <= right and compare(pivot, arr[right]):
					right -= 1
				if left > right:
					break
				arr[left], arr[right] = arr[right], arr[left]
				left += 1
				right -= 1
			
			# 将基准值放到正确位置
			arr[start], arr[right] = arr[right], arr[start]
			pivot_index = right
			
			# 尾递归优化
			if pivot_index - start < end - pivot_index:
				introsort(start, pivot_index - 1, depth - 1)
				start = pivot_index + 1
			else:
				introsort(pivot_index + 1, end, depth - 1)
				end = pivot_index - 1
	
	# 堆排序辅助函数
	def heapify(start: int, heap_size: int, i: int) -> None:
		largest = i
		left = 2 * i + 1
		right = 2 * i + 2
		
		if left < heap_size and compare(arr[start + largest], arr[start + left]):
			largest = left
		
		if right < heap_size and compare(arr[start + largest], arr[start + right]):
			largest = right
		
		if largest != i:
			arr[start + i], arr[start + largest] = arr[start + largest], arr[start + i]
			heapify(start, heap_size, largest)
	
	# 启动内省排序
	introsort(0, len(arr) - 1, max_depth)

def log(n, m, precision=50):
    """
    精确计算以 m 为底 n 的对数 logₘ(n)
    
    参数:
    m (int/float/Decimal): 对数的底数 (必须大于 0 且不等于 1)
    n (int/float/Decimal): 真数 (必须大于 0)
    precision (int): 计算精度 (默认为 50 位小数)
    
    返回:
    Decimal: 高精度对数结果
    """
    # 检查输入是否有效
    if m <= 0 or m == 1:
        raise ValueError("The base must be greater than 0 and not equal to 1")
    if n <= 0:
        raise ValueError("The argument must be greater than 0")
    
    # 设置计算精度
    getcontext().prec = precision
    
    # 转换为 Decimal 类型进行高精度计算
    m_dec = Decimal(str(m))
    n_dec = Decimal(str(n))
    
    # 使用换底公式计算对数: logₘ(n) = ln(n) / ln(m)
    result = n_dec.ln() / m_dec.ln()
    
    # 检查结果是否非常接近整数
    int_result = result.to_integral_value(rounding=ROUND_HALF_UP)
    if abs(result - int_result) < Decimal('1e-10'):
        return int_result
    
    return result

def calculate_latex(latex_expr, precision=10):
    """
    计算LaTeX数学表达式的值
    
    参数:
    latex_expr (str): LaTeX格式的数学表达式
    precision (int): 结果的精度，默认为10位有效数字
    
    返回:
    str: 计算结果的字符串表示
    """
    class Token:
        def __init__(self, type, value, position):
            self.type = type
            self.value = value
            self.position = position
    
    class Lexer:
        def __init__(self, text):
            self.text = text
            self.position = 0
            self.current_char = self.text[self.position] if self.text else None
            self.TOKEN_TYPES = {
                'NUMBER': r'\d+(\.\d+)?',
                'PLUS': r'\+',
                'MINUS': r'-',
                'MULTIPLY': r'\*',
                'DIVIDE': r'/',
                'POWER': r'\^',
                'LPAREN': r'\(',
                'RPAREN': r'\)',
                'LBRACE': r'\{',
                'RBRACE': r'\}',
                'LBRACKET': r'\[',
                'RBRACKET': r'\]',
                'COMMA': r',',
                'VARIABLE': r'[a-zA-Z]+',
                'COMMAND': r'\\[a-zA-Z]+',
                'SYMBOL': r'\\[^\s{a-zA-Z]+',
                'WHITESPACE': r'\s+'
            }
            self.token_patterns = [(k, re.compile(v)) for k, v in self.TOKEN_TYPES.items()]
        
        def advance(self):
            self.position += 1
            if self.position >= len(self.text):
                self.current_char = None
            else:
                self.current_char = self.text[self.position]
        
        def skip_whitespace(self):
            while self.current_char is not None and self.current_char.isspace():
                self.advance()
        
        def get_next_token(self):
            while self.current_char is not None:
                if self.current_char.isspace():
                    self.skip_whitespace()
                    continue
                
                for token_type, pattern in self.token_patterns:
                    if token_type == 'WHITESPACE':
                        continue
                        
                    match = pattern.match(self.text, self.position)
                    if match:
                        value = match.group(0)
                        token = Token(token_type, value, self.position)
                        self.position = match.end()
                        self.current_char = self.text[self.position] if self.position < len(self.text) else None
                        return token
                
                raise SyntaxError(f"Unparsed characters '{self.current_char}' at position {self.position}")
            
            return Token('EOF', None, self.position)
        
        def tokenize(self):
            tokens = []
            token = self.get_next_token()
            while token.type != 'EOF':
                tokens.append(token)
                token = self.get_next_token()
            tokens.append(token)
            return tokens
    
    class ASTNode:
        def evaluate(self, context):
            raise NotImplementedError
    
    class NumberNode(ASTNode):
        def __init__(self, value):
            self.value = value
        
        def evaluate(self, context):
            return self.value
    
    class VariableNode(ASTNode):
        def __init__(self, name):
            self.name = name
        
        def evaluate(self, context):
            if self.name in context.variables:
                return context.variables[self.name]
            elif self.name in context.constants:
                return context.constants[self.name]
            else:
                raise NameError(f"Undefined variable '{self.name}'")
    
    class BinaryOpNode(ASTNode):
        def __init__(self, left, op, right):
            self.left = left
            self.op = op
            self.right = right
        
        def evaluate(self, context):
            left_val = self.left.evaluate(context)
            right_val = self.right.evaluate(context)
            
            if isinstance(left_val, Fraction) and not isinstance(right_val, Fraction):
                right_val = Fraction(str(right_val))
            elif isinstance(right_val, Fraction) and not isinstance(left_val, Fraction):
                left_val = Fraction(str(left_val))
            
            if self.op == '+':
                return left_val + right_val
            elif self.op == '-':
                return left_val - right_val
            elif self.op == '*':
                return left_val * right_val
            elif self.op == '/':
                if right_val == 0:
                    raise ZeroDivisionError("Divisor cannot be zero")
                return left_val / right_val
            elif self.op == '^':
                if isinstance(left_val, Fraction) and isinstance(right_val, Fraction):
                    return float(left_val) ** float(right_val)
                return left_val ** right_val
            else:
                raise NameError(f"Unknown operator '{self.op}'")
    
    class UnaryOpNode(ASTNode):
        def __init__(self, op, expr):
            self.op = op
            self.expr = expr
        
        def evaluate(self, context):
            expr_val = self.expr.evaluate(context)
            
            if self.op == '+':
                return +expr_val
            elif self.op == '-':
                return -expr_val
            else:
                raise NameError(f"Unknown unary operator '{self.op}'")
    
    class FunctionCallNode(ASTNode):
        def __init__(self, name, args):
            self.name = name
            self.args = args
        
        def evaluate(self, context):
            if self.name in context.functions:
                func = context.functions[self.name]
                args = [arg.evaluate(context) for arg in self.args]
                
                processed_args = []
                for arg in args:
                    if isinstance(arg, Fraction):
                        processed_args.append(float(arg))
                    else:
                        processed_args.append(arg)
                
                return func(*processed_args)
            else:
                raise NameError(f"Undefined function '{self.name}'")
    
    class FractionNode(ASTNode):
        def __init__(self, numerator, denominator):
            self.numerator = numerator
            self.denominator = denominator
        
        def evaluate(self, context):
            num = self.numerator.evaluate(context)
            den = self.denominator.evaluate(context)
            
            if den == 0:
                raise ZeroDivisionError("The denominator cannot be zero")
            
            if not isinstance(num, Fraction):
                num = Fraction(str(num))
            if not isinstance(den, Fraction):
                den = Fraction(str(den))
            
            return num / den
    
    class SqrtNode(ASTNode):
        def __init__(self, expr, index=None):
            self.expr = expr
            self.index = index
        
        def evaluate(self, context):
            value = self.expr.evaluate(context)
            
            if self.index is None:
                if value < 0:
                    raise SyntaxError("Cannot calculate the square root of a negative number")
                return math.sqrt(float(value))
            else:
                index_val = self.index.evaluate(context)
                if index_val == 0:
                    raise SyntaxError("The exponent cannot be zero")
                if value < 0 and index_val % 2 == 0:
                    raise SyntaxError("Negative numbers cannot open even powers")
                return float(value) ** (1 / float(index_val))
    
    class Context:
        def __init__(self):
            self.variables = {}
            self.constants = {
                'pi': math.pi,
                'e': math.e,
                'inf': float('inf'),
                'nan': float('nan')
            }
            self.functions = {
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'cot': lambda x: 1/math.tan(x),
                'sec': lambda x: 1/math.cos(x),
                'csc': lambda x: 1/math.sin(x),
                'arcsin': math.asin,
                'arccos': math.acos,
                'arctan': math.atan,
                'ln': math.log,
                'log': math.log10,
                'exp': math.exp,
                'sqrt': math.sqrt,
                'abs': abs,
                'ceil': math.ceil,
                'floor': math.floor,
                'round': round,
                'fact': lambda x: math.factorial(int(x))
            }
    
    class Parser:
        def __init__(self, tokens):
            self.tokens = tokens
            self.position = 0
            self.current_token = self.tokens[self.position]
        
        def eat(self, token_type):
            if self.current_token.type == token_type:
                self.position += 1
                if self.position < len(self.tokens):
                    self.current_token = self.tokens[self.position]
                else:
                    self.current_token = Token('EOF', None, len(self.tokens))
            else:
                raise SyntaxError(f"Expect '{token_type}', but get '{self.current_token.type}'")
        
        def factor(self):
            token = self.current_token
            
            if token.type == 'NUMBER':
                self.eat('NUMBER')
                try:
                    return NumberNode(Fraction(str(token.value)))
                except InvalidOperation:
                    return NumberNode(float(token.value))
            
            elif token.type == 'VARIABLE':
                self.eat('VARIABLE')
                return VariableNode(token.value)
            
            elif token.type == 'LPAREN':
                self.eat('LPAREN')
                result = self.expr()
                self.eat('RPAREN')
                return result
            
            elif token.type == 'COMMAND':
                command = token.value[1:]
                self.eat('COMMAND')
                
                if command == 'frac':
                    self.eat('LBRACE')
                    numerator = self.expr()
                    self.eat('RBRACE')
                    
                    self.eat('LBRACE')
                    denominator = self.expr()
                    self.eat('RBRACE')
                    
                    return FractionNode(numerator, denominator)
                
                elif command == 'sqrt':
                    if self.current_token.type == 'LBRACKET':
                        self.eat('LBRACKET')
                        index = self.expr()
                        self.eat('RBRACKET')
                        
                        self.eat('LBRACE')
                        expr = self.expr()
                        self.eat('RBRACE')
                        
                        return SqrtNode(expr, index)
                    else:
                        self.eat('LBRACE')
                        expr = self.expr()
                        self.eat('RBRACE')
                        
                        return SqrtNode(expr)
                
                elif command in {'sin', 'cos', 'tan', 'cot', 'sec', 'csc', 
                                 'arcsin', 'arccos', 'arctan', 
                                 'ln', 'log', 'exp', 'sqrt', 'abs', 'ceil', 'floor', 'round', 'fact'}:
                    self.eat('LBRACE')
                    arg = self.expr()
                    self.eat('RBRACE')
                    
                    return FunctionCallNode(command, [arg])
                
                else:
                    if command in {'pi', 'e', 'inf', 'nan'}:
                        return VariableNode(command)
                    raise NameError(f"Unknown command '{command}'")
            
            elif token.type == 'SYMBOL':
                symbol = token.value[1:]
                self.eat('SYMBOL')
                
                if symbol in {'pi', 'e'}:
                    return VariableNode(symbol)
                else:
                    raise NameError(f"Unknown symbol '\\{symbol}'")
            
            elif token.type == 'MINUS':
                self.eat('MINUS')
                return UnaryOpNode('-', self.factor())
            
            elif token.type == 'PLUS':
                self.eat('PLUS')
                return UnaryOpNode('+', self.factor())
            
            else:
                raise SyntaxError(f"Unwanted tag '{token.type}'")
        
        def power(self):
            result = self.factor()
            
            while self.current_token.type == 'POWER':
                token = self.current_token
                self.eat('POWER')
                result = BinaryOpNode(result, token.value, self.factor())
            
            return result
        
        def term(self):
            result = self.power()
            
            while self.current_token.type in ('MULTIPLY', 'DIVIDE'):
                token = self.current_token
                if token.type == 'MULTIPLY':
                    self.eat('MULTIPLY')
                elif token.type == 'DIVIDE':
                    self.eat('DIVIDE')
                
                result = BinaryOpNode(result, token.value, self.power())
            
            return result
        
        def expr(self):
            result = self.term()
            
            while self.current_token.type in ('PLUS', 'MINUS'):
                token = self.current_token
                if token.type == 'PLUS':
                    self.eat('PLUS')
                elif token.type == 'MINUS':
                    self.eat('MINUS')
                
                result = BinaryOpNode(result, token.value, self.term())
            
            return result
        
        def parse(self):
            result = self.expr()
            if self.current_token.type != 'EOF':
                raise SyntaxError(f"Unwanted tag '{self.current_token.type}'")
            return result
    
    class Evaluator:
        def __init__(self, context):
            self.context = context
        
        def evaluate(self, ast):
            return ast.evaluate(self.context)
    
    def format_result(result):
        if isinstance(result, Fraction):
            if result.denominator == 1:
                return str(result.numerator)
            else:
                return f"{result.numerator}/{result.denominator}"
        elif isinstance(result, float):
            if result.is_integer():
                return str(int(result))
            else:
                return f"{result:.{precision}g}"
        else:
            return str(result)
    
    latex_expr = latex_expr.replace("(",       "{")\
                           .replace(")",       "}")\
                           .replace("[",       "{")\
                           .replace("]",       "}")\
                           .replace("\\times", "*")\
                           .replace("\\div",   "/")
    lexer = Lexer(latex_expr)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    context = Context()
    evaluator = Evaluator(context)
    result = evaluator.evaluate(ast)

    return format_result(result)