import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Data:
    def __init__(self):
        # Configuração inicial dos cabeçalhos e variáveis
        self.headers = {
            "authorization": ""
        }
        self.datas = []
        self.time = {"inicio": "", "final": ""}
        self.base_url = "https://marketplace.ifood.com.br/v4/customers/me/orders"

    def getJsonData(self):
        # Coleta os dados das ordens do usuário a partir da API do iFood.
        print("Coletando Dados...")
        try:
            i = 0
            while True:
                # Faz uma requisição GET para a API com a página {i}
                resp = requests.get(f'{self.base_url}?page={i}&size=25', headers=self.headers, verify=False)
                if resp.status_code != 200:
                    return {"Error":"Wrong Bearer Token."},resp.status_code  # Levanta uma exceção se a resposta não for 200
                page_data = resp.json()  
                self.datas.extend(page_data)
                # Se o número de ordens retornadas for menor que 25, significa que não há mais dados
                if len(page_data) < 25:
                    break
                i += 1
            print("Dados coletados!")
            return 200
        except Exception as e:
            return {"Error": str(e)}, resp.status_code

    def getTotalSpent(self):
        # Calcula o total gasto, métodos de pagamento usados e os principais restaurantes.
        if not self.datas:
            return {"error": "No data"}, 404

        payments_methods = {}
        restaurantes = {}
        coin = self.datas[0]["payments"]["total"]["currency"]

        # Processa cada ordem coletada
        for i, order in enumerate(self.datas):
            if order["lastStatus"] == "CONCLUDED":
                method_name = order["payments"]["methods"][0]["method"]["name"]
                payment_value = round(order["payments"]["total"]["value"] / 100, 2)
                restaurante = order["merchant"]["name"]

                # Atualiza os dados dos restaurantes
                if restaurante not in restaurantes:
                    restaurantes[restaurante] = {"total_gasto": payment_value, "quantidade_pedidos": 1}
                else:
                    restaurantes[restaurante]["total_gasto"] += payment_value
                    restaurantes[restaurante]["quantidade_pedidos"] += 1

                # Define as datas de início e fim das ordens
                if i == 0:
                    self.time["final"] = order["createdAt"].split("T")[0]
                if i == len(self.datas) - 1:
                    self.time["inicio"] = order["createdAt"].split("T")[0]

                # Atualiza os métodos de pagamento
                if method_name not in payments_methods:
                    payments_methods[method_name] = payment_value 
                else:
                    payments_methods[method_name] = round(payments_methods[method_name] + payment_value, 2)

        total_spent = round(sum(payments_methods.values()), 2)

        # Ordena e seleciona os top 3 restaurantes por gasto e pedidos
        top_restaurantes_por_gasto = sorted(restaurantes.items(), key=lambda item: item[1]["total_gasto"], reverse=True)[:3]
        top_restaurantes_por_pedidos = sorted(restaurantes.items(), key=lambda item: item[1]["quantidade_pedidos"], reverse=True)[:3]

        # Converte as datas para o formato brasileiro
        inicio_formato_br = datetime.strptime(self.time["inicio"], "%Y-%m-%d").strftime("%d/%m/%Y")
        final_formato_br = datetime.strptime(self.time["final"], "%Y-%m-%d").strftime("%d/%m/%Y")

        # Calcula a diferença entre as datas usando relativedelta
        data_inicio = datetime.strptime(self.time["inicio"], "%Y-%m-%d")
        data_final = datetime.strptime(self.time["final"], "%Y-%m-%d")
        diferenca = relativedelta(data_final, data_inicio)
        meses = diferenca.months
        dias = diferenca.days
        anos = diferenca.years

        # Exibe o resumo dos gastos e dos principais restaurantes
        result = {
            "total_spent": f"{total_spent:.2f}",
            "currency": coin,
            "time_period": {
                "start_date": inicio_formato_br,
                "end_date": final_formato_br,
                "years": anos,
                "months": meses,
                "days": dias
            },
            "top_restaurants_by_spending": [
                {"name": nome, "orders": dados["quantidade_pedidos"], "total_spent": f"{dados['total_gasto']:.2f}"}
                for nome, dados in top_restaurantes_por_gasto
            ],
            "top_restaurants_by_orders": [
                {"name": nome, "orders": dados["quantidade_pedidos"], "total_spent": f"{dados['total_gasto']:.2f}"}
                for nome, dados in top_restaurantes_por_pedidos
            ],
            "payment_methods": payments_methods
        }
        
        return result, 200
    
    def get_total_ifood(self):
        status = self.getJsonData()
        if status != 200:
            return status
        return self.getTotalSpent()
