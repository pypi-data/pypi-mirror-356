import sqlite3, datemath, random, datetime

server: str = None
server_last_error: str = None
Numdata: str = ('778623', '777777')

def available_value(article: str) -> int:
    return 6

def virus_detected() -> str:
    return "mnt-206-pc02"

def virus_status() -> str:
    return 'обезврежен'

def connect(_server: str) -> None:
    global server
    server = _server
    db = sqlite3.connect(f'{_server}.db')
    with open(f"{_server}.db", 'w') as _:pass  
    db.execute(f'CREATE TABLE IF NOT EXISTS {_server}(username text, password text, login_time text, isVIP text, tgID text)')
    [try_connect_to(*i) for i in [("GorelovIV", "BadName478!", '0', True), ("Testov5ll", "123456!", '0')]]

def try_connect_to(user_name: str, password: str, login_time: str, admin_rights: bool = False, tg_id: str = "0") -> None:
    db = sqlite3.connect(f'{server}.db')  
    cursor =  db.cursor()
    cursor.execute("INSERT INTO data (username, password, login_time, isVIP, tgID) VALUES(?, ?, ?, ?, ?)", [user_name, password, login_time, "1" if admin_rights else "0", tg_id])
    db.commit()

def request_from_server(param: str, param_name: str, to_return: str):
    db = sqlite3.connect(f'{server}.db')  
    cursor =  db.cursor()
    return cursor.execute(f"SELECT {to_return} FROM data WHERE {param_name} = ?", [param]).fetchone()

def request_to_server(param: str, param_name: str, to_change: str, to_change_name: str) -> None:
    db = sqlite3.connect(f'{server}.db')  
    cursor =  db.cursor()
    cursor.execute(f"UPDATE {server} SET {to_change_name} =  '{to_change}' WHERE {param_name} = (?)",(param, ))
    db.commit()

def request_4_structure(struct: str) -> list:
    return sqlite3.connect(f'{server}.db').cursor().execute(f"SELECT {struct} FROM {server}").fetchall()

def kaspersky_check() -> str:
    global server_last_error
    server_last_error = datemath.datemath("now+10S+3H").strftime("%H:%M:%S")
    return 'Вредоностных активностей не обнаружено.'

def errors(isCriticalRequest: bool = False) -> list:
    return [f'🚨 КРИТИЧЕСКАЯ ПРОБЛЕМА \nХост: c.citrix, 23.210.126.114\nТриггер: CPU load > 90% в течение 15 минут\nВремя: {datemath.datemath("now-3d").strftime("%d/%m/%Y %H:%M:%S")}', f'✅ ПРОБЛЕМА УСТРАНЕНА\nХост: c.citrix, 23.210.126.114\nТриггер: CPU load > 90% в течение 15 минут\nВремя восстановления: {datemath.datemath(f"now-3d+2h+15m+{random.randint(0, 59)}s").strftime("%d/%m/%Y %H:%M:%S")}\nДлительность проблемы: 2 часа 15 минут', f'🚨 КРИТИЧЕСКАЯ ПРОБЛЕМА \nХост: SKUD, 172.28.16.146\nТриггер: недоступен более 5 минут\nВремя: {datemath.datemath("now-1d+2h").strftime("%d/%m/%Y %H:%M:%S")}', f'✅ ПРОБЛЕМА УСТРАНЕНА \nХост: SKUD, 172.28.16.146\nТриггер: недоступен более 5 минут\nВремя восстановления: {datemath.datemath(f"now-1d+2h+47m+{random.randint(0, 59)}s").strftime("%d/%m/%Y %H:%M:%S")}\nДлительность проблемы: 47 минут.'] if isCriticalRequest else [f'⚠️ ПРЕДУПРЕЖДЕНИЕ\nХост: spb.bank16\nТриггер: Использование RAM > 80%\nВремя: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', f'⚠️ ПРЕДУПРЕЖДЕНИЕ\nХост: spb.bank_1c3\nТриггер: Использование RAM > 80%\nВремя: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', f'⚠️ ПРЕДУПРЕЖДЕНИЕ\nХост: print_serv\nТриггер: Потеря пакетов > 5% за 10 минут.\nВремя: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'], "минут."

def LSE() -> str:
    return server_last_error

def is_valid_article(article: str) -> bool:
    return True if article == '778623' else False

def get_data_by_article(article: str) -> str:
    match article:
        case "778623":
            return "1️⃣ `Силикагель 60 (0.040-0.063 мм) для колоночной хроматографии (230-400 mesh ASTM)`\
                     \n2️⃣`Наличие: 5 (ск. Кузьмолово)`\
                        \n3️⃣`Производитель : \"Химмед\"`"
        case "777777":
            return f'ℹ️ Статус: `На ремонте.`\nℹ️ Поставщик: `ООО "АЛАРМ"`\nℹ️ Ожидаемая дата: `{datemath.datemath("now+5d").strftime("%d-%m-%Y")}`'
    return "❌ Ничего не найдено."