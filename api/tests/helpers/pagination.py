def validated_pagination(data):
    if not data:
        raise ValueError("Os dados estão vazios.")

    required_keys = ["results", "count", "previous", "next"]
    for key in required_keys:
        if key not in data:
            raise KeyError(f"A chave '{key}' está faltando no dicionário 'data'.")

        count_pagination = data["count"]
        len_results = len(data["results"])
        
        if len_results != count_pagination:
            raise ValueError("A quantidade de resultados não corresponde ao 'count'.")

        if len_results == 1:
            if data["previous"] is not None or data["next"] is not None:
                raise ValueError("Para um único resultado, 'previous' e 'next' devem ser None.")
            
        return True
