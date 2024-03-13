# Lexer
class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position] if self.code else None
        self.operators = {"+", "++", "-", "/", "*"}
        self.keywords = {"if", "while", "else", "elif"}
        self.separators = {",", ";"}
        self.letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
                        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
                        "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    # move the lexer position and identify next possible tokens.
    def advance(self):
    
        self.position += 1
        if self.position < len(self.code):
            self.current_char = self.code[self.position]
        else:
            self.current_char = None
    def get_token(self):
        #First I define the types of tokens we can have
       
        currentPosition = self.code[self.position]
        
        if self.position < len(self.code):
            self.current_char = self.code[self.position]
        else:
            self.current_char = None  # End of input
        
        #Next we make sure that we skip any whitespace
        while self.position < len(self.code) and self.code[self.position] in (' '):
            self.position += 1

        #Checks to make sure we arnt at the end
        if self.position >= len(self.code):
            return None
        
        #Next we will updates the current position of where we are at after
        currentPosition = self.code[self.position]

        #If the current position is in operators then we return that as the token
        if currentPosition in self.operators:
            token = (currentPosition, "OPERATOR")
            self.position += 1  
            return token
        #Else if the position is a letter or _ then its either keyword or identifier token
        elif currentPosition in self.letters or currentPosition == "_":
            #We will want to count the starting position
            startPosition = self.position

            while self.position < len(self.code) and (self.code[self.position] in self.letters or self.code[self.position] == '_'):
                self.position += 1

            token_value = ""
            for index in range(startPosition, self.position):
                token_value += self.code[index]
            token_type = "IDENTIFIER"
            if token_value in self.keywords:
                token_type = "KEYWORD"
            return (token_value, token_type)

            
                
                

# Parser
# Input : lexer object
# Output: AST program representation.


# First and foremost, to successfully complete this project you have to understand
# the grammar of the language correctly.

# We advise(not forcing you to stick to it) you to complete the following function 
# declarations.

# Basic idea is to walk over the program by each statement and emit a AST representation
# in list. And the test_utility expects parse function to return a AST representation in list.
# Return empty list for ill-formed programs.

# A minimal(basic) working parser must have working implementation for all functions except:
# if_statment, while_loop, condition.

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.current_char = None
        #Here we will make a method that movoes to the first token
        self.advance()


    # function to parse the entire program
    def parse(self):
        ast = self.program()#Start at the program
        return ast 
        
    # move to the next token.
    def advance(self):
        #Here we go advance to the token from lexer and than update the current token as we go
        self.current_token = self.lexer.get_token()

    # parse the one or multiple statements
    def program(self):
        statement = []#List of the statement nodes
        while self.current_token is not None:#While there are still more tokens that we can check
            statement.append(self.statement())#Append the statement to the list
            self.advance()#advance to next token
        return statement
    
    # parse if, while, assignment statement.
    def statement(self):
        if self.current_token[0] == "if":#Check to see if the current token is an if statement
            self.if_statement()#if it is an if statement it will go to the if statement function
        elif self.current_token[0] == "while":#Check to see if the current token is an while loop
            self.while_loop()#if it is an if statement it will go to the while loop function
        elif self.current_token[1] == "IDENTIFIER":#Check to see if the current token is a IDENTIFIER
            self.assignment()#if it is an if statement it will go to the assignment function

    # parse assignment statements
    def assignment(self):
        print("Entered assignment method")
        if self.current_token[0] == "IDENTIFIER":#if the token is an identifier
            identifier = self.current_token[1]#Store the identifier 
            self.advance()
            if self.current_token[0] == "=":#Makes sure that the equal sign is there so we know its an expression 
                self.advance()
                arExpression = self.arithmetic_expression()#We will parse the expression and this will take us to the arithmetic_expression funtion in which will do so
                node = ("ASSIGNMENT", identifier, arExpression)#Creating the node for the assigment which will represent the right side of the arExpression

            else:    
                return False
        else:
            return False



    # parse arithmetic experssions
    def arithmetic_expression(self):
        term = self.term()#Parse the term
        
        while self.current_token is not None and self.current_token[0] == "OPERATOR": #While there are currents to ceck and the token is an operator
            operator = self.current_token[1]#store the operator
            if operator == "+" or operator == "-":#Check if plus or minus operator
                self.advance()
                continuingTerm = self.term()#Parse the term
                if operator == "+":
                    term += continuingTerm
                elif operator == "-":
                    term -= continuingTerm
            else:
                break
        return term
            
            
   
    def term(self):
        factor = self.factor()#Parsing a factor
        while self.current_token is not None  and self.current_token[0] == "OPERATOR":
            operator = self.current_token[1]#store the operator
            if operator == "/" or operator == "*":
                self.advance()
                continuingFactor = self.factor()#Parse the term
                if operator == "*":
                    factor *= continuingFactor
                elif operator == "/":
                    factor /= continuingFactor
            else: 
                break
        return factor



    def factor(self):
        if self.current_char.isdigit() or self.current_char == '.':
  
            numberStringForm = ''
            while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
                numberStringForm += self.current_char
                self.advance() 

            if '.' in numberStringForm:
                number_value = float(numberStringForm)
            else:
                number_value = int(numberStringForm)
            return number_value

        elif self.current_token[0] == "IDENTIFIER":
    
            value = self.current_token[1]  
            self.advance()  
            return value

        elif self.current_token[0] == "(":
            self.advance()  
            expr_value = self.arithmetic_expression()
            if self.current_token[0] != ")":
                raise Exception("Expected ')' after expression")
            self.advance()  
            return expr_value

        else:
            raise Exception(f"Unexpected token: {self.current_token}")




    # parse if statement, you can handle then and else part here.
    # you also have to check for condition.
    def if_statement(self):
        condition = self.condition()#Parse the condition
        trueBlock = self.parse()#Parse true blocks

        elifStatement = []


        while self.current_token == "elif":
            self.advance()
            elifCondition = self.condition()#Parse the condition
            elifParse = self.parse()#Barse elif block
            elifStatement.append((elifCondition,elifParse))

        elseBlock = None
        if self.current_token == "else":
            self.advance()
            elseBlock = self.parse()#Parse the condition

        ifNode = ("IF_STATEMENT", condition, trueBlock, elifStatement, elseBlock)
        return ifNode

    # implement while statment, check for condition
    # possibly make a call to statement?
    def while_loop(self):
        condition = self.condition()#Parse condition

        loop = self.parse() #Parse loop

        whileNode = ("WHILE", condition, loop)#While node

        return whileNode


    def condition(self):
        leftSide =  self.current_token
        self.advance()

        operator =  self.current_token
        self.advance()

        rightSide = self.current_token
        self.advance()

        if operator == "==":
            return leftSide == rightSide
        elif operator == "!=":
            return leftSide != rightSide
        elif operator == "<":
            return leftSide < rightSide
        elif operator == "<=":
            return leftSide <= rightSide
        elif operator == ">":
            return leftSide > rightSide
        elif operator == ">=":
            return leftSide >= rightSide
        else:
            return False
        
