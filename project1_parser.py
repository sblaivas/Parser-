class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.currentCharachter = self.code[self.position] if self.code else None #Set current charachter to the current position and 
        #if the code is empty than return None

        #definie operater, keyword, separators, and letters
        self.operators = {"+", "-", "/", "*", "=", "==", ">", "<", ">=", "<="}
        self.keywords = {"if", "while", "else", "elif","then"}
        self.separators = {",", ";", "(", ")"}
        self.letters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")#Letters is uppercase and lowercase letters

    def advance(self):#helper function to advance the position by oe
        self.position += 1#move the position
        if self.position < len(self.code):#checks to make sure the position is within bound
            self.currentCharachter = self.code[self.position]#if it is update the current charachrter to the position
        else:
            self.currentCharachter = None #otherwise if it is outside set it to none

    def checkNext(self):#helper function to check the next character without moving foward to see what comes next 
        checkNext_pos = self.position + 1#gets the position of the next charachter
        if checkNext_pos < len(self.code):#makes sure the charachter is within bounds
            return self.code[checkNext_pos]#returns the charachters position if it is in bound
        else:
            return None#otherwise if its out of bounds return none
    # move the lexer position and identify next possible tokens.
    def get_token(self):
        while self.currentCharachter is not None and self.currentCharachter.isspace():#skips any white space until a charachter is found
            self.advance()

        if self.currentCharachter is None:#checks to see if the end of the code has been reached and returns nOne if it is
            return None

        if self.currentCharachter.isdigit() or (self.currentCharachter == '.' and self.checkNext().isdigit()):#checks if the next charachter is a number
            stringofNumbers = '' #creates a emptry string to collect numbers 
            while self.currentCharachter is not None and (self.currentCharachter.isdigit() or self.currentCharachter == '.'):#keep going until
                #the end of the code has been reached and makes sure the charachter is a degit or a period which showing its a number or a decimal
                stringofNumbers += self.currentCharachter#ppends to the string of numbers
                self.advance()
            return (stringofNumbers, "NUMBER") #Returns the string of Numbers and tags it as "NUMBER"

        if self.currentCharachter.isalpha() or self.currentCharachter == "_":#checks if the character is a idenifier or a keyword
            stringOfID = ''
            while self.currentCharachter is not None and (self.currentCharachter.isalnum() or self.currentCharachter == '_'):
                #makes sure the current charachter is not at the end and checks if all the charachters are alphanumeric or has a underscore
                stringOfID += self.currentCharachter #if it does then it appends it to the string of identifieds and keywords
                self.advance()
            token_type = "KEYWORD" if stringOfID in self.keywords else "IDENTIFIER" #we check if the stringOFID is in the keywords or identifier 
            #and assign it as the token type
            return (stringOfID, token_type)#returns the stringOFID and the token type

        if self.currentCharachter in self.operators:#checks if the current character is in operators
            op = self.currentCharachter#sets op(operetator) to the current charachter
            if op + self.checkNext() in self.operators: #checks if the current and next character is a operator
                op += self.checkNext()#if it is then we append it to op
                self.advance()
            self.advance()
            return (op, "OPERATOR") #returns the operator and assigns t as "OPERATOR"

        if self.currentCharachter in self.separators:#checks if the current charachter is in seperator
            sep = self.currentCharachter#sets seperator to the current charachter
            self.advance()
            return (sep, "SEPARATOR")#returns the seprator and assigns it as "SEPARATOR"

        self.advance()  # Handle unknown characters by skipping them
        return None
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
        self.advance()  
    # function to parse the entire program
    def parse(self):
        ast = self.program() #calls program to recrsivly start the parsing process which will be assigned to Abstract Syntax Tree 
        return ast
    # move to the next token.
    def advance(self):
        self.current_token = self.lexer.get_token()#gets the next token from the code
    # parse the one or multiple statements
    def program(self):
        statements = []#collects the parsed statemens
        while self.current_token and self.current_token[0] not in {'end', 'else', 'elif'}:#while more tokens to be parsed and not end of block
            statement = self.statement()#parse the statement
            if statement:#checks if the statement has been parsed
                statements.append(statement)#append to statement
        return statements
    # parse if, while, assignment statement.
    def statement(self):
        if self.current_token[0] == 'if': #check if the current token is an if statement
            result = self.if_statement() #parse the if statement
        elif self.current_token[0] == 'while':#check if the current token is an while statement
            result = self.while_loop() #parse the while loop
        elif self.current_token[1] == 'IDENTIFIER':#check if the current token is an identifier statement
            result = self.assignment() #parse the assigment
        else:
            self.advance()
            result = None #sets to none if no statements have been parsed
        return result
    # parse assignment statements   
    def assignment(self):
        identifier = self.current_token[0] #sets the current token to identifier
        self.advance()
        if self.current_token and self.current_token[0] == "=": #makes sure the token is not none and if its an equal sign as = will follow
            self.advance()
            expression = self.arithmetic_expression()#parse the arithmetic expression
            return ('=', identifier, expression)
 
    # parse arithmetic experssions     
    def arithmetic_expression(self):
        leftOperand = self.term()#parse the term

        #while theres tokens to proccess and the current token is an operator and is either plus or -
        while self.current_token and self.current_token[1] == "OPERATOR" and self.current_token[0] in {"+", "-"}: 
            operator = self.current_token[0]#assigns + or - to the operator 
            self.advance()
            rightOperand = self.term()#parse the term
            leftOperand = (operator, leftOperand, rightOperand)#assigns the operator and the left and right operand back to the left operand
        return leftOperand
    
    def term(self):
        leftOperand = self.factor() #parses the factor
        while self.current_token and self.current_token[0] in {"*", "/"}: #while there tokens to procces and the current toek is * or /
            operator = self.current_token[0] #assigns or * or /
            self.advance()
            rightOperand = self.factor() #parses the right side of the factor and assinngs it to right operand
            leftOperand = (operator, leftOperand, rightOperand)#parses the right side of the factor and assinngs it to right operand
        return leftOperand

    def factor(self):
        currentToken = self.current_token#current token
        if currentToken is None:#if no more token to parse return false
            return False
        if currentToken[1] == "NUMBER": #checks if the current token is a number
            if '.' in currentToken[0]:#check if theres a decimal
                value = float(currentToken[0])  #if it is then converts it to a float
            else:
                value = int(currentToken[0])  # other wise we conevert it to a int
            self.advance()
            return value
        elif currentToken[1] == "IDENTIFIER":#checks if the current token is an identifier
            identifier = currentToken[0]#gets the name of the identifier
            self.advance()
            return identifier

        elif currentToken[0] == "(":#checks if the current token is (
            self.advance()
            expression = self.arithmetic_expression()#if it is ( then it parses the expression inside the ()
            if self.current_token[0] != ")":#checks to make sure there is a ) and if not returns false
                return False
            self.advance()
            return expression

    # parse if statement, you can handle then and else part here.
    # you also have to check for condition.
    def if_statement(self):
        self.advance()  
        condition = self.condition()#parse the condition
        trueBlock = self.program()#parses the true block

        if len(trueBlock) == 1:#checks to see if there is only 1 statement
            trueBlock = trueBlock[0]#chagnes the true block from being a list with one item to have that being the item iteself

        elseBlock = None #none unles theres an else in the block
        if self.current_token and self.current_token[0] == 'else':#looks for the else token
            self.advance()
            elseBlock = self.program()#parses the else block
            if len(elseBlock) == 1:#checks if the else block is only 1 statement
                elseBlock = elseBlock[0]##chagnes the else block from being a list with one item to have that being the item iteself

        if elseBlock is not None:#checks for an else block
            return ('if','else', condition, trueBlock, elseBlock)#returns thhe truckblock  elseblock condition  'if' and 'else' and represnets a node
        else:
            return ('if', condition, trueBlock)#reutrns if condition and trueblock and represnets a node

    # implement while statment, check for condition
    # possibly make a call to statement?
    def while_loop(self):
        self.advance()  
        condition = self.condition()#parses the condition
        body = self.program()#parses the body of the while loop
        whileNode = ('while', condition, body)#rthe node contains while condition and body
        return whileNode

    def condition(self):
        leftOperand = self.arithmetic_expression()#parses the left side of the operand
        if self.current_token and self.current_token[1] == "OPERATOR":#checks if the token exists and if its an operator
            operator = self.current_token[0]#assigns the operator
            self.advance()
            rightOperand = self.arithmetic_expression()#parses the right side of the operand
            condition = (operator, leftOperand, rightOperand)#encloses the entire expression
            return condition


