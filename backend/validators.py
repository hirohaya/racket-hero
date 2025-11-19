"""
Validações robustas para entrada de dados - Racket Hero
Implementa validações em Pydantic schemas para garantir dados válidos
"""

from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict
from typing import Optional
from datetime import date
import re


class UsuarioRegisterSchema(BaseModel):
    """Schema para registro de novo usuário"""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "joao@example.com",
                "nome": "João Silva",
                "password": "SenhaForte123!",
                "tipo": "jogador"
            }
        }
    )
    
    email: EmailStr = Field(..., description="Email do usuário")
    nome: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nome completo (3-100 caracteres)"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Senha (mínimo 8 caracteres)"
    )
    tipo: str = Field(
        default="jogador",
        pattern="^(admin|jogador|organizador)$",
        description="Tipo de usuário"
    )
    
    @field_validator('nome')
    @classmethod
    def validate_nome(cls, v):
        """Validar nome: sem números, caracteres especiais"""
        if not re.match(r'^[a-zA-Zçãõáéíóú\s]+$', v):
            raise ValueError('Nome deve conter apenas letras e espaços')
        return v.title()
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validar senha: deve conter letra, número, caractere especial"""
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('Senha deve conter pelo menos uma letra')
        if not re.search(r'\d', v):
            raise ValueError('Senha deve conter pelo menos um número')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Senha deve conter pelo menos um caractere especial')
        return v


class UsuarioLoginSchema(BaseModel):
    """Schema para login"""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "joao@example.com",
                "password": "SenhaForte123!"
            }
        }
    )
    
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., description="Senha")


class EventCreateSchema(BaseModel):
    """Schema para criar evento"""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Torneio Regional",
                "date": "2025-12-20",
                "time": "14:00",
                "active": True
            }
        }
    )
    
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nome do evento"
    )
    date: str = Field(
        ...,
        description="Data no formato YYYY-MM-DD"
    )
    time: str = Field(
        ...,
        description="Hora no formato HH:MM"
    )
    active: bool = Field(default=True, description="Evento ativo?")
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        """Validar formato de data"""
        try:
            date_obj = date.fromisoformat(v)
            if date_obj < date.today():
                raise ValueError('Data não pode ser no passado')
            return v
        except ValueError:
            raise ValueError('Data deve estar no formato YYYY-MM-DD')
    
    @field_validator('time')
    @classmethod
    def validate_time(cls, v):
        """Validar formato de hora"""
        if not re.match(r'^\d{2}:\d{2}$', v):
            raise ValueError('Hora deve estar no formato HH:MM')
        
        hour, minute = map(int, v.split(':'))
        if not (0 <= hour < 24 and 0 <= minute < 60):
            raise ValueError('Hora inválida')
        return v


class PlayerCreateSchema(BaseModel):
    """Schema para criar jogador"""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "event_id": 1,
                "name": "João Silva",
                "club": "Clube A",
                "initial_elo": 1600.0
            }
        }
    )
    
    event_id: int = Field(..., gt=0, description="ID do evento")
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nome do jogador"
    )
    club: Optional[str] = Field(
        None,
        max_length=100,
        description="Clube do jogador (opcional)"
    )
    initial_elo: float = Field(
        default=1600.0,
        ge=400.0,
        le=3000.0,
        description="Elo inicial (400-3000)"
    )
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validar nome do jogador"""
        if not re.match(r'^[a-zA-Zçãõáéíóú\s]+$', v):
            raise ValueError('Nome deve conter apenas letras')
        return v.title()
    
    @field_validator('club')
    @classmethod
    def validate_club(cls, v):
        """Validar nome do clube"""
        if v and not re.match(r'^[a-zA-Zçãõáéíóú\s0-9]+$', v):
            raise ValueError('Clube deve conter apenas letras e números')
        return v.title() if v else v
    
    @field_validator('initial_elo')
    @classmethod
    def validate_elo(cls, v):
        """Validar Elo inicial"""
        if v % 1 != 0:
            raise ValueError('Elo deve ser um número inteiro')
        return float(v)


class MatchCreateSchema(BaseModel):
    """Schema para criar partida"""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "event_id": 1,
                "player_1_id": 1,
                "player_2_id": 2,
                "winner_id": 1
            }
        }
    )
    
    event_id: int = Field(..., gt=0, description="ID do evento")
    player_1_id: int = Field(..., gt=0, description="ID do jogador 1")
    player_2_id: int = Field(..., gt=0, description="ID do jogador 2")
    winner_id: Optional[int] = Field(
        None,
        gt=0,
        description="ID do vencedor (opcional)"
    )
    
    @field_validator('player_2_id')
    @classmethod
    def validate_different_players(cls, v, info):
        """Validar que os jogadores são diferentes"""
        if 'player_1_id' in info.data and v == info.data['player_1_id']:
            raise ValueError('Jogador 1 e Jogador 2 devem ser diferentes')
        return v
    
    @field_validator('winner_id', mode='after')
    @classmethod
    def validate_winner(cls, v, info):
        """Validar que vencedor é um dos jogadores ou None"""
        if v is not None:
            valid_ids = {info.data.get('player_1_id'), info.data.get('player_2_id')}
            if v not in valid_ids:
                raise ValueError('Vencedor deve ser um dos jogadores')
        return v


class MatchUpdateSchema(BaseModel):
    """Schema para atualizar partida"""
    
    event_id: int = Field(..., gt=0)
    player_1_id: int = Field(..., gt=0)
    player_2_id: int = Field(..., gt=0)
    winner_id: Optional[int] = Field(None, gt=0)
    
    @field_validator('winner_id', mode='after')
    @classmethod
    def validate_winner(cls, v, info):
        """Validar que vencedor é um dos jogadores ou None"""
        if v is not None:
            valid_ids = {info.data.get('player_1_id'), info.data.get('player_2_id')}
            if v not in valid_ids:
                raise ValueError('Vencedor deve ser um dos jogadores')
        return v


class QueryValidator:
    """Validador para parâmetros de query string"""
    
    @staticmethod
    def validate_event_id(event_id: int) -> int:
        """Validar ID do evento"""
        if event_id <= 0:
            raise ValueError('Event ID deve ser positivo')
        return event_id
    
    @staticmethod
    def validate_page(page: int = 1) -> int:
        """Validar número da página"""
        if page < 1:
            raise ValueError('Página deve ser >= 1')
        return page
    
    @staticmethod
    def validate_limit(limit: int = 100) -> int:
        """Validar limite de resultados"""
        if not (1 <= limit <= 1000):
            raise ValueError('Limite deve estar entre 1 e 1000')
        return limit
    
    @staticmethod
    def validate_search_term(term: str) -> str:
        """Validar termo de busca"""
        if len(term) < 2:
            raise ValueError('Termo de busca deve ter mínimo 2 caracteres')
        if len(term) > 100:
            raise ValueError('Termo de busca não pode exceder 100 caracteres')
        # Remover caracteres perigosos
        return re.sub(r'[<>\"\'%;()&+]', '', term)


class ValidationError(Exception):
    """Exceção customizada para erros de validação"""
    
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)


def validate_input(data: dict, schema_class) -> dict:
    """
    Validar input usando Pydantic schema
    
    Args:
        data: Dicionário com dados a validar
        schema_class: Classe Pydantic do schema
    
    Returns:
        Dicionário validado e convertido
    
    Raises:
        ValidationError: Se validação falhar
    """
    try:
        validated = schema_class(**data)
        return validated.dict()
    except Exception as e:
        raise ValidationError(str(e))


# Middleware para validação automática em FastAPI
from fastapi import HTTPException, status

async def validate_request_body(request_body: dict, schema_class):
    """
    Validar corpo da requisição
    
    Uso em FastAPI:
        @router.post("/users")
        async def create_user(data: UsuarioRegisterSchema):
            # Pydantic faz validação automaticamente
            pass
    """
    try:
        return schema_class(**request_body)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )


if __name__ == '__main__':
    # Testes de validação
    
    # Usuário válido
    try:
        usuario = UsuarioRegisterSchema(
            email="joao@test.com",
            nome="João Silva",
            password="SenhaForte123!",
            tipo="jogador"
        )
        print(f"✅ Usuário válido: {usuario}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Evento com data inválida
    try:
        evento = EventCreateSchema(
            name="Torneio",
            date="2020-01-01",  # Data no passado
            time="14:00"
        )
        print(f"✅ Evento: {evento}")
    except Exception as e:
        print(f"❌ Erro esperado: {e}")
    
    # Partida com jogadores iguais
    try:
        match = MatchCreateSchema(
            event_id=1,
            player_1_id=1,
            player_2_id=1,  # Mesmo jogador!
            winner_id=1
        )
        print(f"✅ Partida: {match}")
    except Exception as e:
        print(f"❌ Erro esperado: {e}")
