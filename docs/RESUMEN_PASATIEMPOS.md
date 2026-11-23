# RESUMEN · Pasatiempos tóxicos (Francisco Ruiz) · 23 nov 2026

## 1. Cómo trabajar
- Español de España. Respuestas **cortas** para el móvil. No inventar; si no sé algo, decirlo.
- No subir ni programar nada sin permiso de Francisco. No puedo oír el audio: preguntar qué dicen los personajes.
- Antes de proponer ideas o guiones: aplicar el **prompt maestro** (`docs/prompt_maestro_guionista.md`): investigar referentes, escribir 30 ideas, puntuarlas y presentar solo las mejores, con el remate escrito primero.
- **Hashtags:** máximo 5 y siempre **#retos**.
- NUNCA mezclar con el canal de Bityn.

## 2. Repositorio y archivos
- Rama de trabajo: **`claude/pasatiempos-toxicos-navidad-4ysz82`** (contiene todo lo de Pasatiempos; antes estaba en `claude/pasatiempos-turron-fix-kv1aqb`).
- `scripts/`: montajes (Python + PIL + ffmpeg). Los más recientes:
  - `dios_navidad_build.py`: fábula con medallas y palabra a palabra.
  - `abuela_gordo_build.py`: pegatinas emoji y zooms en los remates.
- `skill/editor-reels-libros`: skill de método.
- `docs/comunidad13_biblia.md`: **serie actual**.
- `docs/serie_operacion_turron.md`: serie de Navidad (aparcada).
- `docs/prompt_maestro_guionista.md`: método.
- Fuentes: Baloo 2 (`npm pack @fontsource/baloo-2`), Anton en Drive.

## 3. Drive
- Carpeta de vídeos: `1vRiDiSiXd5rmt731jQ8YasHl_sqIUZGb`
- Interior del libro de Navidad (KDP, 106 págs.): `1oW3lFtOle3s-UMZjvDc2JTGGtncMPwxe`
- Portada de Navidad: `1QVDdzDoXlCnO8lnglUTmlnGgNCXY2otS` · Cubierta: `1mX4HZcqezTpoG0g5oKpI2b8o5gukud8G`
- Anton-Regular.ttf: `17BxchMl4qAGlNFvUO3JS9eJv7ufdvvjD` · Música: `1Noy3aVNVMTXt_8DqwBevzGOe3iEcmEFT`
- **Falta:** el primer libro, «Pasatiempos tóxicos» (calle del Rencor, 13). Pedir el ID para leerlo.

## 4. Libro de Navidad
- «Pasatiempos tóxicos · Edición Navidad». 9,99 € (se valora 8,99 €). Regalía de unos 4-5 €. 2 reseñas.
- Amazon: https://amzn.eu/d/0gNeRQi6 · TikTok @pasatiempostoxico · Metricool brandId 8123021.
- Personajes: abuela Paqui, Mari Carmen, Toni, Encarna, Iván, abuelo Paco, Lucía, Rocío, Chispas.
- Misterio del turrón: el culpable es **Toni** (no destriparlo nunca). Pistas: videollamada con Pura, dentadura de Encarna, consola de Iván, huella del 44.

## 5. Lo aprendido en TikTok
- Unas 700 visualizaciones por vídeo. **La gente se va en el segundo 1.**
- Reseña de la abuela promocionada con 3 €: 2.574 visualizaciones, **1,6 s de media**, 1,4 % la ve entera. **Promocionar no arregla un mal gancho.** Regla: solo promocionar si más del 50 % sigue en el segundo 1 y el visionado medio pasa del 30 %.
- No funcionan: parecer un anuncio, la abuela como protagonista (Francisco no la ve viral), los chistes flojos, el cuñado como monotema, la Navidad como único tema.
- Referentes que gustan: fábula animada de Dios (204.000 me gusta), chistes animados de caricatura (56.000), microseries de IA (Fruit Love Island). Humor corto: menos de 20 s. Serie: 40-55 s con gancho y continuidad.
- Descartados por Francisco: el vídeo del Gordo, la v2 de Dios (sin gracia) y las ideas de abuela, nevera y perro.

## 6. PROYECTO ACTUAL · «LA COMUNIDAD DEL 13»
- Serie animada pop art (amarillo limón, fucsia, cian, contornos negros), 9:16, 40-55 s, una voz fija por personaje y un misterio que avanza.
- 8 vecinos: Maruja, Manolo, Rafa, Vane, Kevin, Amparo, Sonia y Paco. Misterio: notas anónimas en el ascensor y el archivo de Eusebio, el portero muerto.
- Francisco ya ha escrito los episodios 1-7 y el mapa de 4 temporadas (todo en `docs/comunidad13_biblia.md`).
- **Siguiente paso:** fichas de imagen de los 8 personajes en Grok (frente, cuerpo entero, fondo amarillo) → las reviso → planos de 3-6 s, una acción y una voz por clip → yo monto (cabecera, textos y notas en edición, efectos, «continuará»).
- Pendiente de decidir: si Vane lleva blusa de leopardo. Corregir «Amaparo» → Amparo.

## 7. Amazon Ads
- Automática «Navidad auto ES»: añadir las negativas (murdle, murdoku, asesino, asesinato, crimenes, adviento, devir, semana santa, educar, color by numbers; exacta «navidad»), presupuesto 2-3 €/día, parte superior al 0-30 %.
- Manual nueva (Francisco la estaba creando): 5 €/día, 8 palabras en frase (0,40 €) y exacta (0,50 €; 0,60 € las dos de «pasatiempos navidad»), «solo reducir», parte superior +30 %, «Amazon y más allá». Sin el grupo «Palabras clave relacionadas».
- Revisar los términos de búsqueda en 5-7 días.

## 8. Técnico
- 720×1280, 30 fps, H.264 en dos pasadas para quedar por debajo de 3 MB, AAC, loudnorm I=-14.
- Texto entre y=130 e y=1047 y a la izquierda de x=620. Revisar una hoja de fotogramas antes de entregar.
- Grok: clips de unos 6-10 s, imagen a vídeo desde una ficha, voz descrita siempre igual, sin texto. El libro con la tapa amarilla lisa: pongo encima la portada real (detección del amarillo).
