# Costes

Última actualización: julio 2026. Los precios de terceros cambian — verificar antes de usar esta tabla para cerrar un precio de venta.

## Coste actual (uso propio, un solo negocio)

| Herramienta | Plan | Coste/mes | Notas |
|---|---|---|---|
| Railway | Hobby | $5 | Incluye $5 de uso (Postgres + API + Cron); un solo negocio no debería superarlo |
| Vercel | Hobby | $0 | Gratis, pero **solo uso no comercial** (ver aviso abajo) |
| Enable Banking | Restricted Production | $0 | Gratis mientras solo conectes tus propias cuentas |
| Claude Haiku (categorización IA) | Pay-per-use | <$0.05 | A tu volumen actual, prácticamente cero |
| Dominio | — | $0 | Ya tienes aryannarwani.com |
| **TOTAL** | | **~$5/mes** | |

## Aviso: Vercel Hobby y uso comercial

El plan gratuito de Vercel prohíbe explícitamente el uso comercial. En el momento en que factures a un cliente por este servicio, el frontend de ese cliente desplegado en Vercel Hobby estaría técnicamente incumpliendo sus términos de servicio.

Opciones cuando llegue el primer cliente de pago:
- **Vercel Pro**: $20/mes por asiento (developer), permite uso comercial.
- **Netlify** (free tier): permite uso comercial en su capa gratuita — límites similares a Vercel Hobby (100GB bandwidth, ~125K invocaciones de función), sin la restricción de uso comercial.
- **Self-host en Railway**: servir el build estático de Vite como un servicio más de Railway, dentro del mismo coste ya existente.

## Coste al escalar a clientes de pago

| Herramienta | Qué cambia | Coste estimado |
|---|---|---|
| Railway | Un solo backend puede servir a varios negocios (ya es multi-tenant) — el coste sube con el uso real (más sync, más consultas), no de forma lineal por cliente | Probablemente sigue en Hobby ($5) hasta varias decenas de clientes activos |
| Enable Banking | Pasa de gratis a un contrato con precio por volumen (cobran por cuenta bancaria conectada al mes). No publican tarifa pública — piden cotización a través de un formulario que evalúa volumen estimado, países, y si operas con licencia propia o de un partner | Desconocido hasta pedir cotización — **hacerlo antes de cerrar precios con clientes** |
| Vercel/Netlify | Un frontend por cliente (dominio propio) o uno solo multi-tenant | $0-20/mes según plan y número de dominios |
| Claude Haiku | Escala con el número de transacciones sin categorizar, no con el número de clientes | Sigue siendo marginal salvo volumen muy alto (miles de transacciones/mes sin regla) |

## Cómo pedir cotización a Enable Banking

Antes de fijar un precio de venta por cliente, es imprescindible pedir la cotización real — su formulario pide:
1. Estimación de uso (cuentas accedidas e iniciaciones de pago, para el mes 1, 12 y 24)
2. Países donde operarás
3. Si operas con tu propia licencia AISP/PISP o necesitas un partner regulatorio
4. Datos de la empresa (para evaluación de riesgo/sanciones)

Sin este dato, cualquier precio de venta es una estimación a ciegas para el margen real por cliente.

## Plantilla para calcular margen por cliente (cuando tengas la cotización)

```
Coste mensual por cliente = 
    (coste Enable Banking por cuenta conectada)
  + (coste marginal de Railway atribuible, si el uso crece)
  + (coste marginal de Vercel/Netlify si es dominio propio)
  + (coste IA categorización, normalmente marginal)

Margen = Precio de venta mensual - Coste mensual por cliente
```
