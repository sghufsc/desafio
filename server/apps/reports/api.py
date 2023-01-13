"""
API Relatórios

Sobre-escrita das chamadas base da API

"""
import os
import uuid
from datetime import datetime
from pytz import timezone
import pandas
from server.driver import db
from server.api import BaseApi
from .models import Report


class ReportApi(BaseApi):
    """
    API relatórios

    """
    model = Report
    collection = "reports"
    methods = ["list", "retrieve", "create"]

    def create(self, data):
        """
        API para criação de relatórios

        """

        report_id = uuid.uuid4()
        group_id = data["group_id"]
        start_at = data["start_at"]
        end_at = data["end_at"]

        # Obtendo sensores do grupo
        sensors = db().sensors.find({"group_id": group_id})
        sensors_ids = [sensor["_id"]
                       for sensor in sensors]  # Lista de IDs dos sensores

        if not sensors:
            return f"Nenhum sensor do grupo {group_id} foi encontrado", 404

        # Criando escopo de busca no banco
        query_filter = {
            "$and": [
                {"parent_id": {"$in": sensors_ids}},
                {"timestamp": {"$gte": start_at, "$lt": end_at}}
            ]
        }

        # Obtendo leituras
        query_docs = db().reads.find(query_filter)

        # Cada documento do db deverá ser uma linha na tabela
        lines = []
        for doc in query_docs:
            timestamp = datetime.fromtimestamp(doc["timestamp"])
            timestamp = timestamp.strftime('%d-%m-%y %H:%M:%S')

            data = [
                timestamp,
                doc["parent_id"],
                doc["value"],
                doc["reliable"]
            ]

            lines.append(list(pandas.Series(data)))

        # Definindo tabela
        report = pandas.DataFrame(lines, columns=["Carimbo data/hora",
                                                  "Identificador do sensor",
                                                  "Valor da leitura",
                                                  "Confiabilidade da leitura"],)

        # Definindo pasta em que os relatórios serão salvos
        folder_dir = os.path.join(os.getcwd(),
                                  "bucket",
                                  "reports",
                                  report_id)

        # Caso a pasta não exista, é necessário criá-la
        os.makedirs(folder_dir, exist_ok=True)

        # Obtendo hora atual para nomear arquivo
        local_time = datetime.now().astimezone(timezone('America/Sao_Paulo'))
        timestamp = local_time.strftime('%d-%m-%y')
        file_path = os.path.join(
            folder_dir, f"Relatorio-{group_id}-{timestamp}")

        # Transformando dataframe em arquivo .csv e salvando na pasta
        report.to_csv(f"{file_path}.csv")

        # Adicionando arquivos no objeto do db
        files = [
            f"/api/files/reports/{report_id}/Relatorio-{group_id}-{timestamp}.csv"]
        doc_data = dict(_id=report_id, files=files)
        
        db().reports.insert_one(doc_data)
