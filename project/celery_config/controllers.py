import psycopg2
import os
from dotenv import load_dotenv
import json

def obtener_proximos_partidos():
    load_dotenv()
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        
        cursor = connection.cursor()
        cursor.execute('SELECT fixture_id, league_id, league_round, home_team_id, away_team_id, odds FROM fixtures WHERE date > NOW();')        
        records = cursor.fetchall()

        cursor.close()
        connection.close()
        print("Conexión a PostgreSQL cerrada")
        for i in range(len(records)):
            keys = ['id', 'league_id', 'league_round', 'home_team_id', 'away_team_id', 'odds']
            records[i] = dict(zip(keys, records[i]))
        return records

    except (Exception, psycopg2.Error) as error:
        print("Error al conectarse a la base de datos:", error)

def obtener_requests(id_usuario):
    load_dotenv()
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        
        cursor = connection.cursor()
        cursor.execute(f'SELECT user_id, fixture_id, quantity, result  FROM requests WHERE user_id = \'{id_usuario}\' AND group_id = \'19\';')        
        records = cursor.fetchall()

        errores = []
        for i in range(len(records)):
            try:
                records[i] = list(records[i])
                fixture_id = records[i][1]
                cursor.execute(f'SELECT league_id, league_round, home_team_id, away_team_id, odds, goals_home, goals_away FROM fixtures WHERE fixture_id = "{fixture_id}" AND date < NOW() + INTERVAL "3 hours";')
                fixture = list(cursor.fetchall()[0])
                result = ver_ganador(fixture[-2], fixture[-1])
                fixture = fixture[:-2] + [result]
                records[i] += fixture
            except:
                errores.append(i)

        errores = sorted(errores, reverse=True)
        for error in errores:
            print("No se ha encontrado:", records.pop(error))

        cursor.close()
        connection.close()
        print("Conexión a PostgreSQL cerrada")

    except (Exception, psycopg2.Error) as error:
        texto = f"Error al conectarse a la base de datos: {error}"
        return texto

    for i in range(len(records)):
        keys = ['user_id', 'fixture_id', 'quantity', 'result', 'league_id', 'league_round', 'home_team_id', 'away_team_id', 'odds', 'fixture_result']
        records[i] = dict(zip(keys, records[i]))

    return records

def ver_ganador(goals_home, goals_away):
    if goals_home > goals_away:
        return "home"
    elif goals_home < goals_away:
        return "away"
    else:
        return "---"

def aciertos_por_team(requests):
    aciertos = {}
    for request in requests:
        print(request)
        if request['result'] == request['fixture_result']:
            if request['home_team_id'] not in aciertos:
                aciertos[request['home_team_id']] = 0
            if request['away_team_id'] not in aciertos:
                aciertos[request['away_team_id']] = 0
            aciertos[request['home_team_id']] += 1 * request['quantity']
            aciertos[request['away_team_id']] += 1 * request['quantity']
    return aciertos

def ponderador_por_fixtures(id_usuario):
    fixtures = obtener_proximos_partidos()
    requests = obtener_requests(id_usuario)
    aciertos = aciertos_por_team(requests)
    ponderador = {}
    for fixture in fixtures:
        round = int(fixture['league_round'].split(" ")[-1])
        sum_odds = 0
        if fixture['home_team_id'] in aciertos:
            for odd in fixture['odds']:
                if odd['value'] == 'Home':
                    sum_odds += float(odd['odd'])

            ponderador[fixture['home_team_id']] = aciertos[fixture['home_team_id']] * round / sum_odds

        if fixture['away_team_id'] in aciertos:
            for odd in fixture['odds']:
                if odd['value'] == 'Away':
                    sum_odds += float(odd['odd'])

            ponderador[fixture['away_team_id']] = aciertos[fixture['away_team_id']] * round / sum_odds
    return ponderador

def mejores_3(id_usuario):
    ponderadores = ponderador_por_fixtures(id_usuario)
    mejores = sorted(ponderadores.items(), key=lambda x: x[1], reverse=True)[:3]
    mejores_ids = [mejor[0] for mejor in mejores]
    return mejores_ids

if __name__ == "__main__":
    id_usuario = "5c392bd4-4859-4f9f-a7b8-6ae3b8673a55"
    requests = obtener_requests(id_usuario)
    for request in requests:
        break
        print(f"User ID: {request['user_id']}")
        print(f"Fixture ID: {request['fixture_id']}")
        print(f"Quantity: {request['quantity']}")
        print(f"Result: {request['result']}")
        print(f"League ID: {request['league_id']}")
        print(f"League Round: {request['league_round']}")
        print(f"Home Team ID: {request['home_team_id']}")
        print(f"Away Team ID: {request['away_team_id']}")
        print(f"Odds Values: {request['odds']}")
        print(f"Fixture Result: {request['fixture_result']}")
        print("------------------------")

    proximos_partidos = obtener_proximos_partidos()
    for partido in proximos_partidos:
        break
        print("ID:", partido['id'])
        print("League ID:", partido['league_id'])
        print("League Round:", partido['league_round'])
        print("Home Team ID:", partido['home_team_id'])
        print("Away Team ID:", partido['away_team_id'])
        print("Odds Values:", partido['odds'])
        print("------------------------")
    
    aciertos = aciertos_por_team(requests)
    for acierto in aciertos.keys():
        break
        print("Team ID:", acierto)
        print("Aciertos:", aciertos[acierto])
        print("------------------------")

    ponderadores = ponderador_por_fixtures(id_usuario)
    for ponderador in ponderadores.keys():
        break
        print("Team ID:", ponderador)
        print("Ponderador:", ponderadores[ponderador])
        print("------------------------")

    mejores = mejores_3(id_usuario)
    #print(mejores)