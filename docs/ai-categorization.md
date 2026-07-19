# Categorización por IA (fallback)

## Cómo funciona

El motor de reglas (`categorization_rules`) es siempre la primera opción — es determinista, gratis, y no depende de ningún servicio externo. La IA **solo** entra en juego cuando ninguna regla coincide con una transacción (lo que antes quedaba marcado como `⚠️ REVISAR` sin más).

Orden de resolución para cada transacción nueva:
1. Regla `iban_importe` (IBAN + importe exacto coinciden)
2. Regla `iban` (solo IBAN coincide)
3. Regla `texto_contiene` (el nombre de la contraparte o el concepto del banco contiene el texto de la regla)
4. Si nada de lo anterior coincide → llamada a Claude Haiku con el contexto de la transacción y las categorías ya usadas por ese negocio
5. Si la IA tampoco puede resolverlo (o falla la llamada) → se guarda como `⚠️ REVISAR`, igual que antes

## Por qué Claude Haiku y no otra opción

Comparado en `docs/costs.md` en su momento: a este volumen (unas pocas transacciones sin regla por sincronización), el coste es marginal con cualquier proveedor — la decisión se tomó por consistencia con el resto del stack (ya se usa Claude en otros proyectos propios) y por descartar modelos gratuitos de clasificación zero-shot, que dan más falsos positivos en textos bancarios en español con matices.

## Reutilización de categorías

Antes de llamar a la IA, se cargan todas las categorías ya usadas por ese negocio (`SELECT DISTINCT categoria FROM transactions WHERE business_id = ...`) y se le pasan en el prompt, pidiéndole que reutilice una existente si encaja — esto evita que la IA genere categorías nuevas ligeramente distintas cada vez ("Alimentación" vs "Comida" vs "Supermercado") para el mismo tipo de gasto.

## Trazabilidad: columna `categorizado_por`

Cada transacción guarda si su categoría vino de una `regla` o de la `ia` (columna `categorizado_por` en `transactions`). Esto permite en el frontend (pendiente de implementar en la UI) distinguir visualmente qué categorías puso el sistema por su cuenta, para poder revisarlas y, si son correctas, convertirlas en regla fija (más rápido y sin coste en sincronizaciones futuras).

## Límite de seguridad

`MAX_LLAMADAS_IA_POR_SYNC = 50` en `sync_engine.py` — un tope duro de llamadas a la IA por cada ejecución de sincronización, para que un fallo inesperado (ej. todas las reglas dejan de coincidir por algún bug) no dispare un coste descontrolado en una sola ejecución.

## Variable de entorno requerida

`ANTHROPIC_API_KEY` — configurada en los servicios `web` y `sync_banking` de Railway.

## Limitaciones conocidas

- La IA no tiene acceso al histórico de transacciones similares más allá de la lista de nombres de categorías — no ve ejemplos concretos de transacciones ya categorizadas, solo los nombres de categoría. Si en el futuro la precisión no es suficiente, una mejora sería pasarle 2-3 ejemplos reales de transacciones ya categorizadas en esa categoría.
- Si la respuesta de la IA no es un JSON válido (raro, pero posible), se captura la excepción y se marca como `⚠️ REVISAR` — no rompe la sincronización completa.
- No hay caché entre sincronizaciones: si la misma contraparte nueva aparece varias veces antes de que se le añada una regla manual, se le llamará a la IA cada vez (coste marginal, pero es una optimización pendiente si el volumen crece mucho).