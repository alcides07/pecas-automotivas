import pandas as pd
from celery import shared_task
from io import StringIO
from ..models import Part
from ..serializers import PartWriteSerializer
from django.db import transaction

@shared_task
def import_parts(file_content):
    def validate_columns(data):
        required_columns = ["name", "part_number", "details", "price", "quantity"]
        missing_columns = [column for column in required_columns if column not in data.columns]
        if missing_columns:
            raise ValueError(f"O arquivo CSV não contém todas as colunas necessárias. Colunas faltando: {missing_columns}")

    def process_row(row):
        part_row = {
            "name": row["name"],
            "part_number": row["part_number"],
            "details": row["details"],
            "price": row["price"],
            "quantity": row["quantity"],
        }
        return part_row

    try:
        data = pd.read_csv(StringIO(file_content))
    except Exception as e:
        return f"Erro ao ler o arquivo CSV: {str(e)}"

    try:
        validate_columns(data)
    except ValueError as e:
        return {"error": str(e)}

    qtd_criados = 0
    qtd_atualizados = 0

    with transaction.atomic():
        for index, row in data.iterrows():
            try:
                part_row = process_row(row)
            except (ValueError, KeyError) as e:
                return {"error": f"Erro ao processar linha: {str(e)}"}

            part = Part.objects.filter(part_number=part_row["part_number"]).first()
            if part:
                part.quantity += part_row["quantity"]
                part.save()
                qtd_atualizados += 1

            else:
                serializer = PartWriteSerializer(data=part_row)
                if not serializer.is_valid():
                    line_index = index + 2 if isinstance(index, int) else index
                    return {"error": f"Erro na linha {line_index}: {serializer.errors}"}
                part = Part.objects.create(**serializer.validated_data)
                qtd_criados += 1

    return {
        "message": "CSV importado com sucesso.",
        "total_linhas_processadas": len(data),
        "total_registros_criados": qtd_criados,
        "total_registros_atualizados": qtd_atualizados,
    }