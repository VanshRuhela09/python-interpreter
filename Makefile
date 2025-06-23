# Detect OS
ifeq ($(OS),Windows_NT)
    # Windows settings
    OUTPUT := main.exe
else
    # Unix-like settings (Linux, macOS, etc.)
    OUTPUT := main
endif

# Set the compiler and compiler flags
CC := g++
CFLAGS := -std=c++20

# Add DEBUG macro to CFLAGS
ifdef DEBUG
CFLAGS += -DDEBUG -Wall -Wextra -g
CFLAGS += -Wno-unused-variable -Wno-unused-parameter -Wno-reorder
endif

SRCS = ./src/bin/main.cpp \
       ./src/libs/interpreter/interpreter.cpp \
       ./src/libs/lexer/lexer.cpp \
       ./src/libs/value/pyStr.cpp \
       ./src/libs/value/pyFloat.cpp \
       ./src/libs/value/pyInstance.cpp \
       ./src/libs/value/pyClass.cpp \
       ./src/libs/value/pyNone.cpp \
       ./src/libs/value/pyFunction.cpp \
       ./src/libs/value/pyObject.cpp \
       ./src/libs/value/pyInt.cpp \
       ./src/libs/value/pyBool.cpp \
       ./src/libs/value/pyBuiltin.cpp \
       ./src/libs/scope/scope.cpp \
       ./src/libs/parser/parser.cpp \
       ./src/libs/ast/ast.cpp \
       ./src/libs/gc/gc.cpp

# Build rule
build: $(OUTPUT)

# Linking rule
$(OUTPUT):
	$(CC) $(CFLAGS) $(SRCS) -o $(OUTPUT)

# Test rule with optional TEST variable
# Usage: make test TEST=<test_name>
test:
	chmod +x test.sh
	./test.sh $(TEST)

# Clean rule
clean:
ifeq ($(OS),Windows_NT)
	@powershell -Command "Remove-Item -Force -ErrorAction SilentlyContinue $(OUTPUT)"
else
	@rm -f $(OUTPUT)
endif


