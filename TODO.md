# TODO: Bugs and Issues in TinyPy

This document tracks identified bugs, issues, and potential improvements in the TinyPy interpreter codebase.

## Critical Bugs

### 1. String Parsing Vulnerability (tokenizer.py:214-219)
**Location**: `tokenizer.py:214-219`
**Issue**: String parsing doesn't handle unterminated strings or escape sequences
- If a string is not properly closed (missing closing quote), the tokenizer will advance to EOF without error handling
- No support for escape sequences like `\n`, `\"`, `\\`
- Potential infinite loop if EOF is reached while parsing a string

**Fix**: Add proper error handling for unterminated strings and implement escape sequence support

### 2. Invalid Indent Assertion Error (tokenizer.py:133)
**Location**: `tokenizer.py:133`
**Issue**: Hard assertion instead of proper error handling
- `assert rem == 0, "Invalid indent"` will crash the interpreter with AssertionError
- Should use proper exception handling with line number information

**Fix**: Replace with proper exception: `raise SyntaxError(f"line {self.line}: Invalid indentation")`

### 3. CallExpr Attribute Error (parser.py:558)
**Location**: `parser.py:558`
**Issue**: Accessing `.name` attribute on expressions that may not have it
- `expr = CallExpr(expr.name, arguments)` assumes `expr` has a `name` attribute
- Will crash if `expr` is not a `Var` node (e.g., function calls returning functions)

**Fix**: Handle different expression types properly or ensure only valid callables are used

### 4. Incomplete Number Parsing (tokenizer.py:227-230)
**Location**: `tokenizer.py:227-230`  
**Issue**: Decimal number parsing doesn't handle edge cases
- Numbers ending with decimal point (e.g., "5.") are not handled
- No validation for multiple decimal points (e.g., "5.5.5")

**Fix**: Add proper validation for decimal number format

## Parser Issues

### 5. Inconsistent Error Handling (parser.py:287)
**Location**: `parser.py:287`
**Issue**: SyntaxError doesn't include line number information
- Error messages don't provide context about where the error occurred
- Makes debugging difficult for users

**Fix**: Include token line numbers in all error messages

### 6. Factor/Term Precedence Bug (parser.py:334)
**Location**: `parser.py:334`
**Issue**: In `term()` method, right operand calls `factor()` instead of `term()`
- Should be left-associative: `a - b - c` should be `(a - b) - c`
- Currently right-associative which is incorrect

**Fix**: Change `right = self.factor()` to `right = self.term()` in line 334

### 7. Backtracking in var_stmt (parser.py:435)
**Location**: `parser.py:435`
**Issue**: Manual position manipulation instead of proper lookahead
- `self.position -= 1` is fragile and error-prone
- Comments indicate awareness that backtracking is problematic

**Fix**: Implement proper lookahead or restructure parsing logic

### 8. Missing elif Support
**Location**: `parser.py` (if_stmt method)
**Issue**: Parser defines `ELIF` token but doesn't implement elif parsing
- Only handles if/else, not elif chains
- Tokenizer recognizes "elif" but parser ignores it

**Fix**: Implement elif parsing in `if_stmt()` method

## Interpreter Issues

### 9. Type Coercion Bug (interpreter.py:56-58)
**Location**: `interpreter.py:56-58`
**Issue**: String coercion logic is overly broad and incorrect
- Converts both operands to strings if either is a string
- Prevents proper type errors and numeric operations
- Comment indicates awareness this is a "FIXME"

**Fix**: Implement proper type checking and coercion rules

### 10. Variable Redefinition Inconsistency (interpreter.py:97-98)
**Location**: `interpreter.py:97-98` vs `interpreter.py:116-117`
**Issue**: Inconsistent handling of undefined variables
- `visit_var_stmt` prevents redefinition of existing variables
- `visit_assign_stmt` prevents assignment to undefined variables
- Python allows both reassignment and dynamic variable creation

**Fix**: Align behavior with Python semantics or document the intended behavior

### 11. Function Scope Issues (interpreter.py:150-160)
**Location**: `interpreter.py:150-160`
**Issue**: Naive scope handling
- Simple copy/restore of entire variable scope
- No support for nested scopes or closures
- No handling of global variables

**Fix**: Implement proper lexical scoping with scope chains

## Whitespace and Formatting Issues

### 12. Inconsistent Whitespace Handling (tokenizer.py:120-145)
**Location**: `tokenizer.py:120-145`
**Issue**: Comments mention "whitespace handling has bugs"
- Complex logic for handling indentation
- May not handle mixed tabs/spaces correctly
- EOF handling for indentation might be incorrect

**Fix**: Simplify and test whitespace handling thoroughly

### 13. Missing Comma Support (tokenizer.py)
**Location**: Tokenizer defines COMMA but limited usage in parser
**Issue**: COMMA token is defined but not used in all contexts where commas are valid
- Function calls support comma-separated arguments
- But other contexts (like tuple literals) don't exist yet

**Fix**: Implement complete comma support or document limitations

## Error Handling Framework

### 14. No Systematic Error Handling
**Location**: Throughout codebase
**Issue**: Error handling is inconsistent across components
- Mix of exceptions, assertions, and print statements
- No line number reporting in many errors  
- No error recovery mechanisms

**Fix**: Implement consistent error handling framework with proper error types and reporting

## Missing Features (Mentioned in Comments/TODOs)

### 15. Print as Statement vs Function (CLAUDE.md)
**Issue**: Print is currently implemented as a statement but should be a function
**Fix**: Refactor print to be a callable function

### 16. No Type Checking (interpreter.py:111)
**Issue**: Comment indicates "there's no type checking"
**Fix**: Implement basic type checking for variable assignments and function calls

## Test Coverage Gaps

### 17. Limited Error Case Testing
**Issue**: Tests focus on happy path scenarios
- No tests for syntax errors, runtime errors, or edge cases
- No tests for malformed input

**Fix**: Add comprehensive error testing

### 18. No Integration Testing
**Issue**: Limited testing of complete programs
- Tests are mostly unit tests for individual components
- `test.sh` provides some integration testing but could be expanded

**Fix**: Add more comprehensive integration tests

## Documentation and Code Quality

### 19. Incomplete Documentation
**Issue**: Many methods and classes lack documentation
- No docstrings explaining complex parsing logic
- Limited comments for non-obvious code

**Fix**: Add comprehensive documentation

### 20. Magic Numbers and Constants
**Location**: `tokenizer.py:82` (`INDENT_SPACES = 4`)
**Issue**: Hard-coded constants that could be configurable
**Fix**: Consider making indentation configurable or clearly document the constraint