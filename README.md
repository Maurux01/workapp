# Workapp — La forma inteligente de conseguir trabajo / The smart way to get a job

Busca ofertas reales (LinkedIn, Jooble, RemoteOK, Indeed, Computrabajo),
analiza tu CV en PDF, mide compatibilidad por skills, marca posible fraude
y guarda todo en Supabase. Ubicación por defecto: Colombia.

## Instalación rápida (Windows)

```bat
install.bat
 rem o:  python install_wizard.py
```

Manual:

```bash
pip install -r requirements.txt
cp .env.example .env
python main_desktop.py   # escritorio / desktop
python main_web.py       # web en http://localhost:5000
```

## Uso

1. Sube tu CV en PDF → extrae email, teléfono, skills y experiencia.
2. Busca por palabra clave + ubicación → scraping real con caché de 24h.
3. Cada oferta pasa detector anti-fraude y, si hay CV, recibe % de match.
4. ES/EN disponible en desktop y web.

## Supabase

1. Crea un proyecto en https://supabase.com y corre `supabase/schema.sql`
   en el SQL Editor (crea la tabla `jobs` + políticas RLS).
2. Copia `SUPABASE_URL` y `SUPABASE_KEY` (anon key) a tu `.env` local.
3. Listo: cada búsqueda guarda/actualiza ofertas automáticamente
   (upsert por `url`). Sin keys, la app funciona igual con caché local.

> ⚠️ Nunca subas tu `.env` a git. Solo `.env.example` vive en el repo.

## Notas

- LinkedIn usa su API pública guest (sin login) y RemoteOK su API abierta:
  son las fuentes más estables. Jooble/Indeed/Computrabajo a veces
  bloquean con 403/500 → la app sigue con las demás + datos de muestra.
- PDFs de prueba van en `data/CVs/`, caché en `data/cache/`.
