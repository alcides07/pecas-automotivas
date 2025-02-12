import pandas as pd
from celery import shared_task
from io import StringIO
from ..models import Part
from ..serializers import PartWriteSerializer
from django.db import transaction
from rest_framework.exceptions import ValidationError

@shared_task
def import_parts(file_content):
    try:
        data = pd.read_csv(StringIO(file_content))
    except Exception as e:
        return f"Erro ao ler o arquivo CSV: {str(e)}"

    required_columns = ["name", "part_number", "details", "price", "quantity"]
    if not all(column in data.columns for column in required_columns):
        raise ValidationError(f"O arquivo CSV não contém todas as colunas necessárias: {required_columns}")

    qtd_criados = 0
    qtd_atualizados = 0

    try:
        with transaction.atomic():
            for _, row in data.iterrows():
                part_row = {
                    "name": row.get("name"),
                    "part_number": row.get("part_number"),
                    "details": row.get("details"),
                    "price": float(row.get("price", 0)),
                    "quantity": int(row.get("quantity", 0)),
                }

                serializer = PartWriteSerializer(data=part_row)
                if not serializer.is_valid():
                    raise ValidationError(serializer.errors)

                part = Part.objects.filter(part_number=part_row["part_number"]).first()
                if part:
                    part.quantity += part_row["quantity"]
                    part.save()
                    qtd_atualizados += 1
                else:
                    part = Part.objects.create(**serializer.validated_data)
                    qtd_criados += 1

    except Exception as e:
        return f"Erro ao salvar as partes no banco de dados: {str(e)}"

    return {
        "message": "CSV importado com sucesso!",
        "total_linhas_processadas": len(data),
        "total_registros_criados": qtd_criados,
        "total_registros_atualizados": qtd_atualizados,
    }