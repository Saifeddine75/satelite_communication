# Detecting the OS and setting platform-specific variables
VENV = .venv
ifeq ($(OS),Windows_NT)
    VENV_PKG_DIR = Scripts
    BIN = $(VENV)/$(VENV_PKG_DIR)
    EXT = .exe
    RMDIR_CMD = rmdir /s /q
    CLEAN_CACHE = for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
    DEL_CMD = del /s /q
else
    VENV_PKG_DIR = bin
    BIN = $(VENV)/$(VENV_PKG_DIR)
    EXT =
    RMDIR_CMD = rm -rf
    DEL_CMD = rm -f
endif

PYTHON   = $(BIN)/python$(EXT)
UVICORN  = $(BIN)/uvicorn$(EXT)
PYTEST   = $(BIN)/pytest$(EXT)
