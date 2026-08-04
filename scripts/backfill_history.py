import jwt as pyjwt
import requests
from datetime import datetime, date, timedelta
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from sync_engine import generar_jwt, engine
from sqlalchemy import text
import uuid

BANK_CONNECTION_ID = "1b8f9a0e-d17c-4eda-99eb-a982a6b97f6b"  # una cuenta cada vez

with engine.begin() as conn:
    conexion = conn.execute(text("""
        SELECT business_id, application_id, account_uid, private_key_env_var
        FROM bank_connections WHERE id = :id
    """), {"id": BANK_CONNECTION_ID}).mappings().first()

    headers = {"Authorization": f"Bearer {generar_jwt(conexion['application_id'], conexion['private_key_env_var'])}"}

    continuation_key = None
    total_traidas = 0
    pagina = 1

    while True:
        params = {
            "date_from": (date.today() - timedelta(days=1095)).isoformat(),  # 3 años hacia atrás, ajusta si quieres
            "date_to": date.today().isoformat(),
            "strategy": "longest",
        }
        if continuation_key:
            params["continuation_key"] = continuation_key

        r = requests.get(
            f"https://api.enablebanking.com/accounts/{conexion['account_uid']}/transactions",
            headers=headers, params=params, timeout=30,
        )

        if r.status_code == 429:
            print("Límite diario alcanzado, para aquí y continúa mañana.")
            break
        if r.status_code != 200:
            print(f"Error {r.status_code}: {r.text}")
            break

        data = r.json()
        transacciones = data.get("transactions", [])
        continuation_key = data.get("continuation_key")

        for t in transacciones:
            ref_unica = f"{t.get('entry_reference')}_{t.get('booking_date')}_{t['transaction_amount']['amount']}"
            iban = ((t.get("creditor_account") or {}).get("iban") or (t.get("debtor_account") or {}).get("iban") or "")
            conn.execute(text("""
                INSERT INTO transactions
                (id, business_id, bank_connection_id, referencia_unica, fecha, importe, moneda,
                 tipo, contraparte, iban_contraparte, concepto_banco, concepto_detallado, categoria, referencia)
                VALUES (:id, :bid, :bcid, :ref, :fecha, :importe, :moneda, :tipo, :contraparte,
                        :iban, :concepto_banco, '', NULL, :referencia)
                ON CONFLICT (business_id, referencia_unica) DO NOTHING
            """), {
                "id": str(uuid.uuid4()), "bid": conexion["business_id"], "bcid": BANK_CONNECTION_ID,
                "ref": ref_unica, "fecha": t.get("booking_date"),
                "importe": float(t["transaction_amount"]["amount"]),
                "moneda": t["transaction_amount"]["currency"],
                "tipo": "Entrada" if t.get("credit_debit_indicator") == "CRDT" else "Salida",
                "contraparte": (t.get("creditor") or {}).get("name") or (t.get("debtor") or {}).get("name"),
                "iban": iban, "concepto_banco": " | ".join(t.get("remittance_information") or []),
                "referencia": t.get("reference_number"),
            })

        total_traidas += len(transacciones)
        print(f"Página {pagina}: {len(transacciones)} movimientos (total acumulado: {total_traidas})")
        pagina += 1

        if not continuation_key:
            print(f"\n✅ Backfill completo. Total: {total_traidas} movimientos.")
            break