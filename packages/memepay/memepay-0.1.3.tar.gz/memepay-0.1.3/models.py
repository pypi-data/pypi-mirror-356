"""
Модели данных для MemePay SDK
"""

from dataclasses import dataclass
from typing import Optional, Any, Dict, Union, List
from datetime import datetime


@dataclass
class ExpiresAt:
    """Дата истечения срока платежа"""
    _raw_data: Dict[str, str]
    
    def __init__(self, data: Dict[str, str]):
        self._raw_data = data or {"date": "", "time": ""}
    
    def data(self) -> str:
        """Возвращает дату"""
        date_str = self._raw_data.get("date", "")
        if date_str:
            try:
                if "T" in date_str:
                    iso_date = date_str.split("T")[0]
                    return datetime.strptime(iso_date, "%Y-%m-%d").strftime("%d.%m.%Y")
                return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d.%m.%Y")
            except ValueError:
                return date_str
        return ""
    
    def time(self) -> str:
        """Возвращает время"""
        time_str = self._raw_data.get("time", "")
        if time_str:
            try:
                return datetime.strptime(time_str, "%H:%M:%S").strftime("%H:%M:%S")
            except ValueError:
                return time_str
        return ""
    
    def __str__(self) -> str:
        """Строковое представление"""
        return f"{self.data()} {self.time()}"
    
    def get(self, key: str) -> str:
        """Получение значения по ключу (для совместимости)"""
        return self._raw_data.get(key, "")


@dataclass
class PaymentInfo:
    """Информация о платеже"""
    id: str
    amount: float
    amount_with_commission: float
    status: str
    method: str
    created_at: datetime


@dataclass
class RatesResponse:
    """Ответ на запрос курсов валют"""
    rates: Dict[str, float]
    currency: str
    last_updated: str


@dataclass
class ConvertResponse:
    """Ответ на запрос конвертации валют"""
    amount: float
    from_currency: str
    to_currency: str


@dataclass
class PaymentCreateResponse:
    """Ответ на создание платежа"""
    payment_id: str
    payment_url: str
    amount: float
    status: str
    expires_at: Union[ExpiresAt, datetime]
    created_at: datetime


@dataclass
class UserInfo:
    """Информация о пользователе"""
    name: str
    email: str
    balance: float
    created_at: datetime


@dataclass
class TransferResponse:
    """Ответ на перевод средств"""
    transaction: Dict[str, Any]
    recipient: str
    amount: float
    commission: float
    sender: str
    new_balance: float


@dataclass
class PaymentMethodDetails:
    """Детали метода оплаты"""
    min: float
    max: float
    commission: float


class PaymentMethodsResponse:
    """Ответ с доступными методами оплаты"""
    default: Dict[str, PaymentMethodDetails]
    partner: Dict[str, PaymentMethodDetails]
    
    def __init__(self, default: Dict[str, PaymentMethodDetails], partner: Dict[str, PaymentMethodDetails]):
        self.default = default
        self.partner = partner
    
    def get(self, method_id: str) -> Optional[PaymentMethodDetails]:
        """
        Получение информации о конкретном методе оплаты
        
        Args:
            method_id: ID метода оплаты
            
        Returns:
            Optional[PaymentMethodDetails]: Информация о методе оплаты или None, если метод не найден
        """
        if method_id in self.default:
            return self.default[method_id]
        if method_id in self.partner:
            return self.partner[method_id]
        return None


@dataclass
class ApiResponse:
    """Общий ответ API"""
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    error: Optional[str] = None