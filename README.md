API de Totais do iFood
Descrição
Esta API permite aos usuários obter um resumo dos gastos no iFood, incluindo o total gasto, métodos de pagamento utilizados e os principais restaurantes com base nas ordens concluídas. O projeto é baseado no Flask e interage com a API do iFood.

Funcionalidades
Obter Total Gasto no iFood: Recebe um token Bearer e retorna o total gasto, métodos de pagamento utilizados e os principais restaurantes por gasto e pedidos.
Tecnologias Utilizadas
Python
Flask
Flask-CORS
Requests
Dateutil

Uso
Execute a aplicação:
python app.py

Faça uma requisição POST para http://127.0.0.1:5000/get_total_ifood com o seguinte payload JSON:
{
  "token": "SEU_TOKEN_BEARER"
}

Exemplo de resposta:

{
  "total_spent": "1234.56",
  "currency": "BRL",
  "time_period": {
    "start_date": "01/01/2023",
    "end_date": "31/12/2023",
    "years": 0,
    "months": 11,
    "days": 30
  },
  "top_restaurants_by_spending": [
    {
      "name": "Restaurante A",
      "orders": 10,
      "total_spent": "456.78"
    },
    {
      "name": "Restaurante B",
      "orders": 5,
      "total_spent": "234.56"
    },
    {
      "name": "Restaurante C",
      "orders": 3,
      "total_spent": "123.45"
    }
  ],
  "top_restaurants_by_orders": [
    {
      "name": "Restaurante A",
      "orders": 10,
      "total_spent": "456.78"
    },
    {
      "name": "Restaurante B",
      "orders": 5,
      "total_spent": "234.56"
    },
    {
      "name": "Restaurante C",
      "orders": 3,
      "total_spent": "123.45"
    }
  ],
  "payment_methods": {
    "Crédito": 1000,
    "Débito": 234.56
  }
}
