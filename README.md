# Workapp — La forma inteligente de conseguir trabajo / The smart way to get a job

🌐 **Úsala en el navegador (sin instalar nada): https://maurux01.github.io/workapp/**
(ofertas remotas en vivo, análisis de CV en tu navegador, ES/EN)

💾 **Descargar para Windows (sin saber de GitHub ni Python):
https://github.com/Maurux01/workapp/releases/latest**
baja `Workapp.exe`, doble clic y listo. Si Windows SmartScreen avisa,
clic en "Más información" → "Ejecutar de todas formas".

Busca ofertas reales en 9 fuentes (LinkedIn, Jooble, RemoteOK, Remotive,
Arbeitnow, Indeed, Computrabajo), analiza tu CV en PDF, mide compatibilidad
por skills, marca posible fraude y guarda todo en Supabase.
Ubicación por defecto: Colombia. Interfaz 100% en español o 100% en inglés.

## Abrir la app

- **Escritorio (sin terminal):** doble clic en `Workapp.pyw`.
- **Escritorio (instala deps primero):** doble clic en `Workapp.bat`.
- **Web:** `python main_web.py` → abre sola el navegador en
  http://localhost:5000 (déjala corriendo, cierra con CTRL+C).

## Instalación manual

```bash
pip install -r requirements.txt
cp .env.example .env   # el .env real NUNCA se sube a git
python main_desktop.py
```

## Uso

1. Sube tu CV en PDF → extrae email, teléfono, skills y experiencia.
2. Busca por palabra clave + ubicación, con checkboxes de jornada
   (tiempo completo, medio tiempo, freelance, pasantía) y modalidad
   (remoto, presencial, híbrido).
3. Cada oferta pasa detector anti-fraude y anti-fantasma: bloquea empresas
   como `varesdev`, carnadas de "banco de talentos" y reposts de +60 días.
   Agrega más con `BLOCKED_COMPANIES=otra1,otra2` en tu `.env`.
4. Cambia ES/EN en cualquier momento: toda la interfaz cambia de idioma.

## Supabase

1. Crea un proyecto en https://supabase.com y corre `supabase/schema.sql`
   en el SQL Editor (crea la tabla `jobs` + políticas RLS).
2. Copia `SUPABASE_URL` y `SUPABASE_KEY` (anon key) a tu `.env` local.
3. Listo: cada búsqueda guarda/actualiza ofertas automáticamente
   (upsert por `url`). Sin keys, la app funciona igual con caché local.

> ⚠️ Nunca subas tu `.env` a git. Solo `.env.example` vive en el repo.

## Notas

- LinkedIn (API guest), RemoteOK, Remotive y Arbeitnow (APIs abiertas):
  fuentes estables. Jooble/Indeed/Computrabajo/OCC a veces bloquean
  con 403/500 → la app sigue con las demás + datos de muestra.
- El CV web se guarda en el servidor (no en la cookie): soporta PDFs grandes.
- PDFs de prueba van en `data/CVs/`, caché en `data/cache/`.
