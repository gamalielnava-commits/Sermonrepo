# ▶ Sermon Pro

**De la predicación (o cualquier video largo de YouTube) a clips virales 9:16 en 1 clic.**

Pegás el link, la IA detecta los 8-10 momentos más virales, los recorta a vertical con subtítulos automáticos, y te permite subirlos directamente a TikTok, Instagram Reels y YouTube Shorts.

Basado en [mutonby/openshorts](https://github.com/mutonby/openshorts) (MIT). Re-brandeado, re-diseñado y configurado para despliegue en Railway.

---

## 🚀 Guía de despliegue — sin saber programar

### Paso 1 · Crear cuenta en Railway (si todavía no)

1. Andá a https://railway.com y hacé clic en **"Login"**.
2. Elegí **"Login with GitHub"** y autorizá Railway.

### Paso 2 · Deploy desde este repo

1. En Railway, clic en **"New Project"** → **"Deploy from GitHub repo"**.
2. Buscá **`sermonrepo`** y seleccionalo.
3. Railway va a detectar el `Dockerfile` y empezar a compilar solo.
4. **El primer build tarda 5-10 minutos** (descarga modelos de IA). Tomate un café ☕.

### Paso 3 · Pegar las claves (variables de entorno)

En tu proyecto de Railway:

1. Clic en la pestaña **"Variables"**.
2. Clic en **"+ New Variable"** y pegá cada una:

| Variable | Obligatoria | Dónde conseguirla |
|---|---|---|
| `GEMINI_API_KEY` | ✅ Sí | https://aistudio.google.com/apikey (gratis, tocá "Create API key") |
| `UPLOAD_POST_API_KEY` | Opcional | https://www.upload-post.com (10 uploads/mes gratis) |
| `AWS_ACCESS_KEY_ID` | Recomendada | [Guía AWS abajo](#crear-s3-gratis) |
| `AWS_SECRET_ACCESS_KEY` | Recomendada | AWS IAM |
| `AWS_REGION` | Recomendada | Por ej. `us-east-1` |
| `AWS_S3_BUCKET` | Recomendada | El nombre de tu bucket |
| `AWS_S3_PUBLIC_BUCKET` | Opcional | Bucket público (puede ser el mismo) |
| `YTDLP_PROXY` | **Recomendada en Railway** | [Guía Webshare abajo](#fix-youtube-429) — sin esto YouTube bloquea las descargas |
| `MAX_CONCURRENT_JOBS` | Opcional | `1` está bien para empezar |

> 💡 Con solo `GEMINI_API_KEY` ya podés arrancar la web. Para que funcione el botón "Generar clips virales" desde Railway vas a necesitar también `YTDLP_PROXY` (ver sección abajo).

### Paso 4 · Obtener tu URL pública

1. En Railway: pestaña **"Settings"** → sección **"Networking"** → **"Generate Domain"**.
2. Te da un link tipo `https://sermonrepo-production-xxxx.up.railway.app`.
3. Abrilo en el navegador → **¡Ya está!**

### Paso 5 · Usar Sermon Pro

1. Entrá a tu URL pública.
2. Hacé clic en **"Empezar ahora"** o **"▶ Generar clips virales"**.
3. Pegá un link de YouTube.
4. Esperá (los primeros minutos descarga modelos, después va mucho más rápido).
5. Elegí los clips que más te gustan → botones de TikTok / Reels / Shorts para publicar.

---

<a id="fix-youtube-429"></a>

## 🌐 Fix YouTube 429 — Proxy residencial (obligatorio en Railway)

**El problema**: Railway (y cualquier nube) usa IPs de datacenter. YouTube las bloquea con `HTTP 429 / Unavailable` porque sabe que no son usuarios reales. Vas a ver este error al generar clips:

```
❌ FATAL ERROR: YOUTUBE DOWNLOAD FAILED
REASON: YouTube has blocked the download request (Error 429/Unavailable)
```

**La solución pro** (la que usan OpusClip, Submagic y Munch): pasar el tráfico por un **proxy residencial** que parece un usuario de casa. **Transparente para tus clientes finales** — ellos solo pegan el link de YouTube y anda.

### Opción 1 · Webshare.io (gratis para empezar)

1. Registrate gratis en 👉 https://www.webshare.io (sign-up con Google, 30 segundos).
2. Una vez adentro, en la sidebar: **"Proxy"** → **"List"**.
3. Vas a ver una tabla con proxies. Elegí **UNA** fila y copiá los 4 valores:
   - Username (ej: `abcdef-rotate`)
   - Password (ej: `xyz789`)
   - Host (ej: `p.webshare.io`)
   - Port (ej: `80`)
4. Armá la URL con este formato: **`http://USUARIO:PASSWORD@HOST:PUERTO`**
   - Ejemplo: `http://abcdef-rotate:xyz789@p.webshare.io:80`
5. En Railway → tu proyecto → **"Variables"** → **"+ New Variable"**:
   - Name: `YTDLP_PROXY`
   - Value: tu URL completa del paso 4
   - **Save** → Railway re-deploya solo en ~1 min.
6. Volvé a la web de Sermon Pro y reintentá con un link de YouTube. ✅

**Plan gratuito de Webshare**: 10 proxies rotativos + 1 GB de tráfico mensual. Alcanza para ~20-50 clips de sermones cortos. Cuando escale, el plan "Residential Starter" cuesta ~$2.99/mes.

### Opción 2 · Otros proveedores

Si Webshare no te convence, cualquiera de estos funciona igual — todos usan el mismo formato `http://user:pass@host:port`:

- [SmartProxy](https://smartproxy.com) — desde $8.50/mes.
- [Bright Data](https://brightdata.com) — más caro pero top de la gama.
- [Oxylabs](https://oxylabs.io) — enterprise.

### Opción 3 · Sin proxy (modo personal, no SaaS)

Si es solo para uso tuyo, alternativa avanzada: exportá las cookies de tu sesión de YouTube con la extensión **"Get cookies.txt LOCALLY"** y pegalas en Railway como `YOUTUBE_COOKIES`. Las cookies expiran cada ~1-2 meses y necesitás re-exportarlas. **No recomendado para producción/comercial.**

### Opción 4 · Fallback universal · Subir archivo local

Si por alguna razón ningún proxy funciona, tus usuarios **siempre** pueden usar el botón **"Subir video"** en la app y procesar un archivo MP4/MP3 local. Eso no pasa por YouTube → cero bloqueos.

---

<a id="crear-s3-gratis"></a>

## 📦 Crear bucket de AWS S3 (gratis 12 meses, 5 GB)

> Hacés esto una sola vez. Es necesario si querés que los clips se guarden en la nube.

1. Andá a https://aws.amazon.com/free y hacé clic en **"Create a Free Account"**.
2. Completá: email, contraseña, datos de tarjeta (no cobra si te mantenés dentro del tier gratis).
3. Una vez adentro, buscá **"S3"** en la barra de arriba y entrá.
4. **"Create bucket"**:
   - Bucket name: `sermonpro-<tu-nombre>-clips` (debe ser único en el mundo).
   - Region: `us-east-1` (o la más cercana).
   - Dejá lo demás por default → **"Create bucket"**.
5. Ahora creá las llaves de acceso:
   - Buscá **"IAM"** en la barra de arriba.
   - **"Users"** → **"Create user"** → nombre: `sermonpro-user` → **Next**.
   - **"Attach policies directly"** → buscá y marcá **`AmazonS3FullAccess`** → **Next** → **Create user**.
   - Clic en el usuario creado → pestaña **"Security credentials"** → **"Create access key"**.
   - Tipo: **"Application running outside AWS"** → **Next** → **Create**.
   - **¡Copiá ambos valores!** (Access key y Secret access key — el secret solo se muestra una vez).
6. Pegá esos valores en Railway como `AWS_ACCESS_KEY_ID` y `AWS_SECRET_ACCESS_KEY`.

---

## 🧯 Problemas comunes

| Síntoma | Solución |
|---|---|
| Build de Railway falla con "out of memory" | En Railway, Settings → resources: subí memoria a 2 GB o más. |
| El primer clip tarda mucho | Normal: descarga YOLO, Whisper. Del segundo clip en adelante va 10x más rápido. |
| "Gemini API error 429" | Pasaste el límite del tier gratis (1500/día). Esperá 24 hs o activá cobro en Google. |
| YouTube te bloquea con 429 / Unavailable | Configurá `YTDLP_PROXY` con un proxy residencial — ver [Fix YouTube 429](#fix-youtube-429). |
| Clips sin subtítulos | El modelo Whisper se está descargando. Esperá 2 min y probá de nuevo. |

---

## 💻 Correr localmente (opcional)

Si preferís probarlo en tu PC antes:

```bash
git clone https://github.com/gamalielnava-commits/sermonrepo.git
cd sermonrepo
cp .env.example .env   # y rellená las claves
docker compose up --build
```

Abrí http://localhost:5175 (frontend dev) o http://localhost:8000 (backend).

---

## 📄 Licencia y atribución

- Este proyecto está basado en [mutonby/openshorts](https://github.com/mutonby/openshorts) — licencia **MIT**.
- El README original está preservado en [`README-UPSTREAM.md`](./README-UPSTREAM.md).
- Rebranding, diseño y deploy en Railway por **Sermon Pro**.
