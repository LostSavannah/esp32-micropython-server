def normalize_command_result(data:str) -> list[str]:
    lines = data.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    return [i for i in lines if len(i) > 0]