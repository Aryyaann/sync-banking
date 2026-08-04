import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
from sync_engine import engine, categorizar_con_ia
from sqlalchemy import text

BUSINESS_ID = "5b6bd0a2-b349-4c65-a30f-0fddad475755"



def main():
    with engine.begin() as conn:
        pendientes = conn.execute(text("""
            SELECT id, iban_contraparte, importe, contraparte, concepto_banco, tipo
            FROM transactions
            WHERE business_id = :bid AND concepto_detallado IS NULL
        """), {"bid": BUSINESS_ID}).mappings().all()

        print(f"Movimientos pendientes de categorizar: {len(pendientes)}")

        reglas = conn.execute(text("""
            SELECT rule_type, criterio, concepto_detallado, categoria
            FROM categorization_rules WHERE business_id = :bid
        """), {"bid": BUSINESS_ID}).mappings().all()

        def aplicar_reglas(iban, importe, texto):
            for rg in reglas:
                if rg["rule_type"] == "iban_importe":
                    try:
                        iban_r, importe_r = rg["criterio"].split("|")
                    except ValueError:
                        continue
                    if iban == iban_r.strip() and f"{importe:.2f}" == f"{float(importe_r):.2f}":
                        return rg["concepto_detallado"], rg["categoria"]
            for rg in reglas:
                if rg["rule_type"] == "iban" and iban == rg["criterio"].strip():
                    return rg["concepto_detallado"], rg["categoria"]
            for rg in reglas:
                if rg["rule_type"] == "texto_contiene" and rg["criterio"].upper() in texto:
                    return rg["concepto_detallado"], rg["categoria"]
            return "⚠️ REVISAR", None

        categorias_existentes = [row[0] for row in conn.execute(text("""
            SELECT DISTINCT categoria FROM transactions WHERE business_id = :bid AND categoria IS NOT NULL
        """), {"bid": BUSINESS_ID}).fetchall()]

        MAX_LLAMADAS_IA = 200
        llamadas_ia = 0

        for i, p in enumerate(pendientes):
            iban = p["iban_contraparte"] or ""
            texto = f"{p['contraparte'] or ''} {p['concepto_banco'] or ''}".upper()

            concepto_detallado, categoria = aplicar_reglas(iban, p["importe"], texto)
            fuente = "regla"

            if concepto_detallado == "⚠️ REVISAR" and llamadas_ia < MAX_LLAMADAS_IA:
                concepto_ia, categoria_ia = categorizar_con_ia(
                    p["contraparte"], p["concepto_banco"], p["importe"], p["tipo"], categorias_existentes
                )
                llamadas_ia += 1
                if concepto_ia != "⚠️ REVISAR":
                    concepto_detallado, categoria = concepto_ia, categoria_ia
                    fuente = "ia"
                    if categoria and categoria not in categorias_existentes:
                        categorias_existentes.append(categoria)
                else:
                    fuente = None
            elif concepto_detallado == "⚠️ REVISAR":
                fuente = None

            conn.execute(text("""
                UPDATE transactions SET concepto_detallado = :cd, categoria = :cat, categorizado_por = :fuente
                WHERE id = :id
            """), {"cd": concepto_detallado, "cat": categoria, "fuente": fuente, "id": p["id"]})

            if (i + 1) % 20 == 0:
                print(f"  {i + 1}/{len(pendientes)} procesados...")

        print(f"\n✅ Categorización completa. {llamadas_ia} llamadas a IA usadas.")


if __name__ == "__main__":
    main()