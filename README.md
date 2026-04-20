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
| `MAX_CONCURRENT_JOBS` | Opcional | `1` está bien para empezar |

> 💡 Con solo `GEMINI_API_KEY` ya podés generar clips. Los demás son para funciones extra.

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
| YouTube te bloquea la descarga | Pegá cookies de YouTube como `YOUTUBE_COOKIES` (usá la extensión "Get cookies.txt" en Chrome). |
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
