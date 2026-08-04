# MIS_IDS.md — chuleta personal, NO subir a GitHub
# (añade este archivo a .gitignore si lo guardas dentro del repo)

# ============================================
# 1. BUSINESSES (tus negocios en la tabla `businesses`)
# ============================================
# Comando para ver todos:
#   SELECT id, name FROM businesses;

BUSINESS_ID_MACYS= 9c47c269-62f5-41f8-9f8b-b6b6e65d5076

# ============================================
# 2. BANK_CONNECTIONS (cada cuenta bancaria conectada)
# ============================================
# Comando para ver todas las tuyas:
#   SELECT id, business_id, bank_name, account_label FROM bank_connections WHERE business_id = 'BUSINESS_ID_ARYAN';
#
# Comando para ver las de Macy's Digital:
#   SELECT id, business_id, bank_name, account_label FROM bank_connections WHERE business_id = 'BUSINESS_ID_MACYS';

BANK_CONNECTION_ID_ARYAN_SABADELL=

BANK_CONNECTION_ID_MACYS_CUENTA_1= 1b8f9a0e-d17c-4eda-99eb-a982a6b97f6b
BANK_CONNECTION_ID_MACYS_CUENTA_1_LABEL= Account: 8278

BANK_CONNECTION_ID_MACYS_CUENTA_2= 5b6bd0a2-b349-4c65-a30f-0fddad475755
BANK_CONNECTION_ID_MACYS_CUENTA_2_LABEL= Account: 9530

# ============================================
# 3. APPLICATION_ID de Enable Banking (uno por app registrada en su Control Panel)
# ============================================
# No hay comando SQL para esto — se copia directamente del Control Panel de
# Enable Banking, en la página de cada aplicación registrada.
# También puedes verlo ya guardado en tu base de datos con:
#   SELECT DISTINCT application_id, bank_name FROM bank_connections;

APPLICATION_ID_SABADELL_BUSINESS_PROD= 2127b315-5688-4f72-993b-f1258f136a8d

# ============================================
# 4. PRIVATE_KEY_ENV_VAR (nombre de la variable de Railway con cada clave)
# ============================================
# Comando para ver qué nombre de variable usa cada conexión:
#   SELECT id, account_label, private_key_env_var FROM bank_connections;
#
# El VALOR real de cada una (el contenido de la clave .key) se mira en:
#   Railway → servicio "web" → Variables → busca el nombre de abajo

PRIVATE_KEY_ENV_VAR_BUSINESS='-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDNas8RYgzrrIyX
jVFo1op3ixWBcibmCiQFbok8YeiUqKOL0iqGA3jcnF7G2AMM8MRHATWtWvkhB/ks
I3bxV8QuFA3IVi53v+SFJYIWZrEVTWygfX2CfW4xT4xOHU752EvGLSk5eZZbWPic
edccbgWx6JwTR+YAzOQy/ktUyiseCCt/SiLgNJyb6Payidjh/MbuJwPac4geIDK6
naq0UmALKXOKeavvhy+nyE+ps/HvsTUa3w7NitaXoGbr4cMUQu+cWZ/BiiWaqig1
wb+JdYDur1E103xEkcKwDgrPa+yPOL3yvuvMSoyadD32scUuxq7mTwTex9me8Spq
6M/fk9ZJAgMBAAECggEABRpOIoRpBcG3jFw6VXxe3DFcS2bmiHhgBLKGPjXAbVDz
HxoNbF7Rtck8oXvkN4ITnh/tkWzdG3DzQ6Ft5vjjKrHc1ckuRlNB/fy8ionqhDj0
Jdh4MbGj9x2ewqH/wD0bRMUCbScUERjYtCpiqZYiFhVNKz1x/TsZwBqJDIYpJAnM
dI8XSaYbDl/OB8Ft2QOaTSZgQtTQW1rbKNNFcDsc0+1Ms/2jZyReW83qWeydnpxP
qrbJ6rlEMpZ011UCevi58MS99JqXsUXIAiIp2HFi7m2q2Z1U6TYxi70VM/SOB3Js
dF9YkkerlEcO7qlkHkMuq0KERqwVJtdhb86552z2cQKBgQD/8jgRkV9oebVGNgIZ
4yS5yGBFZQY/mKsixUka+5NJRhLEo3wa2Dr0ZowvvPkmuRtaloHZ+UiZmVWXoDi8
rRjPmcZTfPja1tDaSJvqY5CKFOgNYxnOxKmhprj7TPoRSqjxR8Qnw+IiRLdZRgBu
j75GZM0R3q/VZhIzaav334ki+wKBgQDNdd6DqxNc8VHRQ2B/FUJ1cSYhBUwTB8hS
roA8JNi2Dlig3I71m2wS+NuMxAHxEw7kGu+plXzneShOEiGBsECgFukKpBaXhfnP
gyKw4raEZzUjOnsCpId1pYm/dtizAxNGQLYOoJYKG3Su9JK1p1HamTkPHjqjhshH
A7pfhjIIiwKBgBQv1Y5FKgJCfzKvddD24mGo1TcD9c80SmMurkprhz1jQn2x60ru
vQ+juvDU9c3BEdA+SLWZfMlol6Ci6XawLGHLXiIdnD8ebFCbI3kEK1VIuti7dUCi
sEJotPRVKPAONG77WxRL1d0gEFoBNG2D9tz0fFwpdTLenxbhAchGIDnbAoGBAMKH
UPBVL3YWPaLmKhzoog3T3YfyHf7+pVozQdKwCEcG+j8D1I8SYpbr6+MxSa1YoAa0
wilMEgCPI+wXGoZRvD5WsrqSdZltDgK9ZEEZxjlCBnueSQ1NfbuTygHvomiLBtrD
NhxPSv+y0x07DxTSoJtZ6z43HsnpOQKTswfyZLjVAoGBAIyPkji52A5nP+e0JT2A
ubeG/u//7Xtcb+1D4DDoBjMMyQOba0QfoExDgA1z5+Jydv7UU/q78HpvA1U+dzMA
XSg0AuGrG8X+CNZelJJPlD21UFFVOOgNAuPOCbyVLrcZtjXZVqjb0O+AclLofaH2
S1kUAAljxTDzoeco2pCp9+dr
-----END PRIVATE KEY-----',

# Ruta local de cada archivo .key en TU PC (recuerda: cambia si cambias de ordenador)

PRIVATE_KEY_PATH_BUSINESS= 

# ============================================
# 5. BASE DE DATOS
# ============================================
# Se copia tal cual de: Railway → servicio Postgres → Variables → DATABASE_PUBLIC_URL
# (nunca la escribas a mano, siempre copiar/pegar)

DATABASE_URL= postgresql://postgres:sync2026testXYZ@kodama.proxy.rlwy.net:50752/railway

# ============================================
# 6. URLS DE LOS SERVICIOS
# ============================================

API_URL=https://web-production-a3366.up.railway.app
FRONTEND_URL= https://sync-banking-frontend.vercel.app/

# ============================================
# 7. USUARIOS DE LOGIN
# ============================================
# Comando para ver todos los usuarios (no la contraseña, esa no se puede recuperar):
#   SELECT id, business_id, email FROM users;

EMAIL_PADRE=hnarwani8@gmail.com