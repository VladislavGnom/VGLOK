def unificate_chat_id(chat_id_1, chat_id_2):
    unificated_chat_id = map(str, sorted([chat_id_1, chat_id_2]))
    return ''.join(unificated_chat_id)