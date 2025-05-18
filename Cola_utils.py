import json
import os
from Queue import Queue
import uuid

cola_file = "Queue.json"
colas_virtuales = {}  # clave: empresa_id, valor: dict con cola_id -> Queue()

def load_colas():
    global colas_virtuales
    if os.path.exists(cola_file):
        with open(cola_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            for empresa_id, colas in raw_data.items():
                colas_virtuales[empresa_id] = {}
                for cola_id, turnos in colas.items():
                    q = Queue()
                    for turno in turnos:
                        q.push(turno)
                    colas_virtuales[empresa_id][cola_id] = q
    else:
        colas_virtuales = {}

def save_colas():
    data = {}
    for empresa_id, subcolas in colas_virtuales.items():
        data[empresa_id] = {}
        for cola_id, cola in subcolas.items():
            turnos = []
            current = cola.front
            while current:
                turnos.append(current.data)
                current = current.next
            data[empresa_id][cola_id] = turnos

    with open(cola_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def iniciar_cola(empresa_id, cola_id):
    if empresa_id not in colas_virtuales:
        colas_virtuales[empresa_id] = {}
    if cola_id not in colas_virtuales[empresa_id]:
        colas_virtuales[empresa_id][cola_id] = Queue()
        save_colas()

def agregar_turno(empresa_id, cola_id, turno_obj):
    iniciar_cola(empresa_id, cola_id)
    turno_obj["id"] = str(uuid.uuid4())
    colas_virtuales[empresa_id][cola_id].push(turno_obj)
    save_colas()
    return turno_obj

def siguiente_turno(empresa_id, cola_id):
    if empresa_id in colas_virtuales and cola_id in colas_virtuales[empresa_id]:
        if not colas_virtuales[empresa_id][cola_id].is_empty():
            turno = colas_virtuales[empresa_id][cola_id].pop()
            save_colas()
            return turno
    return None

def obtener_turnos(empresa_id, cola_id):
    if empresa_id not in colas_virtuales or cola_id not in colas_virtuales[empresa_id]:
        return []
    turnos = []
    current = colas_virtuales[empresa_id][cola_id].front
    while current:
        turnos.append(current.data)
        current = current.next
    return turnos

def eliminar_cola(empresa_id, cola_id):
    if empresa_id in colas_virtuales and cola_id in colas_virtuales[empresa_id]:
        del colas_virtuales[empresa_id][cola_id]
        save_colas()
        return True
    return False
