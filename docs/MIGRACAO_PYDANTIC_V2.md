# Guia de Migração Pydantic V1 → V2

## Status Atual

**Versão:** Pydantic V1 (com V2 instalado)  
**Warnings:** 15 de Pydantic (deprecation)  
**Ação:** Gradual migration com fallback para V1

## O Que Precisa Ser Migrado

### 1. Backend - schemas/auth.py

```python
# ❌ V1 Style
class Config:
    from_attributes = True

@validator('nova_senha')
def validate_nova_senha(cls, v):
    ...

# ✅ V2 Style
from pydantic import ConfigDict, field_validator

model_config = ConfigDict(from_attributes=True)

@field_validator('nova_senha')
@classmethod
def validate_nova_senha(cls, v):
    ...
```

### 2. Backend - schemas/matches.py

Similar ao auth.py, substituir:
- `class Config:` por `model_config = ConfigDict(...)`
- `@validator` por `@field_validator`

### 3. Backend - models/

Se houver models com configurações Pydantic.

## Passo a Passo de Migração

1. **Instalar Pydantic V2:**
   ```bash
   pip install --upgrade pydantic
   ```

2. **Atualizar imports em schemas/auth.py:**
   ```python
   from pydantic import BaseModel, ConfigDict, field_validator
   ```

3. **Converter Config class para ConfigDict:**
   ```python
   # Antes
   class ResetPasswordRequest(BaseModel):
       class Config:
           from_attributes = True
   
   # Depois
   class ResetPasswordRequest(BaseModel):
       model_config = ConfigDict(from_attributes=True)
   ```

4. **Converter @validator para @field_validator:**
   ```python
   # Antes
   @validator('campo')
   def validate_campo(cls, v):
       return v
   
   # Depois
   @field_validator('campo')
   @classmethod
   def validate_campo(cls, v):
       return v
   ```

5. **Testar:**
   ```bash
   pytest tests/test_api.py -v
   ```

## Referências

- [Pydantic V2 Migration Guide](https://docs.pydantic.dev/latest/concepts/migration/)
- [Field Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [Config Dict](https://docs.pydantic.dev/latest/concepts/config/)

## Timeline

- **Hoje:** Tarefa 1-5 (Health check, Docker, CI/CD, datetime fix)
- **Amanhã:** Pydantic V2 migration (2-3 horas)
- **Resultado:** 0 warnings de deprecation, V2 100% compatível

## Próximo Passo

Após completar Pydantic V2:
1. Rodar testes completos
2. Validar no Playwright
3. Commitar para git
4. Começar próxima task (CI/CD validation)
