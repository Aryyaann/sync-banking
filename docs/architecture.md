# Arquitectura — decisiones de diseño

## Por qué esta combinación de servicios

- **Railway para backend + Postgres + cron**: todo en un mismo sitio, deploy con git push, capa barata para empezar (~$5/mes), sin gestionar servidores. Permite tener varios "servicios" (API, cron) sobre el mismo repo con configuración independiente.
- **Vercel para el frontend**: detecta Vite automáticamente, deploy instantáneo. Ver aviso en `docs/costs.md` sobre el límite de uso comercial en el plan gratuito.
- **Enable Banking como agregador Open Banking**: acceder directamente a la API PSD2 de cada banco requeriría licencia AISP propia (Banco de España) y certificados eIDAS — inviable para un proyecto de este tamaño. Un agregador ya licenciado resuelve esto. Se descartó GoCardless (Bank Account Data) por no aceptar clientes nuevos desde mediados de 2025.
- **PostgreSQL en vez de Excel como fuente de verdad**: necesario en cuanto hay más de un negocio — cada uno necesita sus propias cuentas, reglas y movimientos aislados. El Excel se mantiene como formato de exportación bajo demanda, no como almacenamiento primario.

## Modelo de datos — multi-tenant desde el diseño inicial

Todas las tablas cuelgan de `business_id`. Ninguna consulta de la API filtra por otro criterio que no sea el `business_id` extraído del JWT de sesión del usuario autenticado — esto es lo que garantiza que un negocio nunca pueda ver los datos de otro, incluso si conociera el ID interno de otro negocio.

```
businesses ← users
businesses ← bank_connections ← transactions
businesses ← categorization_rules
```

Índice único `(business_id, referencia_unica)` en `transactions`: es lo que reemplaza toda la lógica manual de "comparar con lo que ya existe" que tenía la versión basada en Excel — la propia base de datos rechaza duplicados con `ON CONFLICT ... DO NOTHING`.

## Por qué claves privadas por variable de entorno, no en archivo

Cada aplicación registrada en Enable Banking (una por banco/cliente) tiene su propio par de clave RSA. En vez de guardar archivos `.key` en el servidor (que complicaría el despliegue y el control de versiones), cada conexión bancaria en la tabla `bank_connections` guarda el **nombre** de la variable de entorno donde vive su clave (`private_key_env_var`), y esa variable se configura como secret en Railway. Esto permite añadir bancos/clientes nuevos sin tocar código, solo añadiendo una variable de entorno y una fila en la base de datos.

## Por qué autenticación JWT propia y no un proveedor externo (Auth0, Clerk, etc.)

Para el volumen actual (unos pocos negocios), un proveedor externo de auth añade coste y una dependencia más sin necesidad real — bcrypt + PyJWT cubren lo esencial (contraseñas hasheadas, sesión con expiración) con control total y coste cero. Revisar esta decisión solo si el número de usuarios/negocios crece mucho o se necesitan features avanzadas (SSO, 2FA gestionado, etc.).

## Por qué el motor de reglas es código, no configuración declarativa en la base de datos únicamente

Las reglas sí viven en base de datos (`categorization_rules`), pero el **orden de prioridad** (iban_importe > iban > texto_contiene) y la lógica de matching están en Python, no en SQL — se consideró más simple de mantener y depurar que mover esa lógica a triggers o funciones de Postgres, dado el volumen de datos (no hay presión de rendimiento que lo justifique).

## Decisiones pendientes de revisar si el proyecto escala mucho más

- Migrar de Restricted Production a Production sin restricción en Enable Banking (requiere contrato, KYB, y probablemente una licencia AISP propia o un partner regulatorio) si se factura a muchos clientes.
- Añadir caché de categorización IA para evitar llamadas repetidas a la misma contraparte nueva.
- Evaluar mover el frontend fuera de Vercel Hobby en cuanto haya el primer cliente de pago (ver `docs/costs.md`).
- Sustituir el polling del frontend (cada 30-60s) por websockets si el volumen de usuarios simultáneos lo justifica alguna vez — de momento es innecesario dado el ritmo real de actualización de datos bancarios.