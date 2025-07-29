class DataFrame:
    pass

# Excelente. Vamos seguir com o passo 1: o **método `__init__`** da sua classe `DataFrame`.



##  Etapa 1: `__init__`

### Objetivo

# Inicializar a instância com um objeto que seja de um dos tipos aceitos:
# 
# * `numpy.ndarray`
# * `pandas.DataFrame`
# * `polars.DataFrame`
# 
# Se o tipo for inválido, lança `TypeError`.
# 
# ### Responsabilidades
# 
# 1. Armazenar o dado original em `self._data`
# 2. Inferir e armazenar o tipo em `self._type` (ex: `"numpy"`, `"pandas"`, `"polars"`)
# 3. Validar o tipo suportado
# 
# ---
# 
# ## 📌 Instruções
# 
# Implemente um `__init__(self, data)` com a seguinte lógica:
# 
# 1. Verifica o tipo com `isinstance(data, ...)`
# 2. Salva o `data` no atributo privado `self._data`
# 3. Salva o tipo como string em `self._type`, como `"numpy"`, `"pandas"` ou `"polars"`
# 4. Se o tipo não for aceito, lança:
# 
#    ```python
#    raise TypeError("Unsupported data type. Expected numpy.ndarray, pandas.DataFrame or polars.DataFrame.")
#    ```

