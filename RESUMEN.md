# Resumen del canal · @bityn.y.r04 (25 nov 2026)
Para arrancar un chat nuevo: «Lee RESUMEN.md, videos/CAMPANA.md, PROMPT_MAESTRO.md y CLAUDE.md y sigue». Rama de trabajo: `claude/narrator-videos-ready-zdga76` (main está desfasada).

## Estrategia vigente (25 nov) → `videos/CAMPANA.md` manda sobre todo
- Lema: «Aventuras que entretienen. Aprendizajes que permanecen.»
- Los vídeos ENTRETIENEN y convencen a los PADRES (no vendemos «aprende a ahorrar» a los niños).
- Fórmula: problema de los padres → sketch divertido → solución del libro → producto → Amazon.
- Dos campañas separadas: «Mi primer dinero» (descubrir el dinero; juego de mesa recortable) y «Mi goloso negocio» (aventura de crear un negocio; 30 días para salvar a R-04; escape room, recetas, retos).
- No prometer de más (nada de «será experto financiero»).
- Sketches de humor inventados PERMITIDOS desde el 25 nov, siempre que lo que se diga del contenido del libro sea verdad.
- Duración: ≤20-25 s. Datos del 23 nov: L1-03 (31 s) → media 5 s vistos, 4,5 % completo. Cifra/sorpresa en el 1.er segundo, nada quieto.

## Método de producción que FUNCIONA (25 nov)
1. **Imágenes en Grok** (sí funcionan con el prompt nuevo; las 3 del vídeo 1 salieron fieles): imagen 9:16 adjuntando `kling/ficha_bityn_r4.jpg`, describiendo cada detalle (Bityn: 1 antena izq., 1 oreja naranja dcha., ojos en arco, sin boca; R-04: 1 ojo-anillo, alas grandes, gorrito, sin boca ni antena) y las siguientes «en el mismo chat» con «same characters».
2. **Animación en Grok** 6 s, cámara fija, movimiento pequeño, FACE LOCK (prompts en `videos/PLANTILLA_V1.md` y en el chat del 25 nov).
3. **Voces en Grok** solo audio (clip de 10 s, la imagen da igual). Narrador: generar todas sus frases seguidas. Al montar: quitar pausas (silenceremove) y acelerar ×1,25-1,35 (Francisco: «habla muy lento»).
4. **Montaje mío** (`montaje/l1_04_ganar_dinero.py` = plantilla): clips + voces + páginas reales del libro + textos grandes + cierre con portada. Comprimir <3 MB (crf 26, maxrate 900k).
- Grok cambia a los personajes si hay gestos grandes o cambios de plano: siempre plano fijo y movimiento mínimo.
- Revisar SIEMPRE las imágenes antes de animar.

## Vídeos
- Publicados: V01, V02 (17-18 nov), L1-03 «carta a los Reyes» (22 nov, 78 vistas).
- V08 «libro físico» Black Friday (27 nov 19:30, sin IA, 14,5 s): montado con los vídeos de Francisco (IMG_7477/7478 → libro_fisico/*_720.mp4). Datos L1-04 (26 nov): 70 vistas, 2,5 s media, 1,16 % completo → el gancho falla: texto en el fotograma 0, acción desde el 1.er segundo, 10-15 s.
- Listos sin publicar: L1-01, L1-02 «CARIÑO DETECTADO», V03-V07, L1-03b (versión corta 15 s), **L1-04 «¿Tu peque sabe lo que cuesta ganar dinero?» (vídeo 1 de la campaña nueva, 24,5 s)**. Todo en `videos/` y en Drive.
- Siguiente: vídeo 3 «30 días para salvar a un robot» → plan y prompts en `videos/PLANTILLA_V3.md` (esperando imágenes y voces de Grok), luego 2, 4 y 5 (guiones en el chat del 25 nov y resumen en CAMPANA.md). Necesitan fichas de Lía, Sr. Tornillo y Brillo (las tarjetas de `kling/personajes` son pequeñas).
- Propuesto y pendiente de respuesta: vídeo con el LIBRO FÍSICO en las manos de Francisco + voz (formato que más vende; Black Friday 27 nov).

## Reglas fijas
- «Tu hijo o hija» / «tu peque», nunca solo «tu hijo».
- Cada vídeo se resuelve en sí mismo (nada de «mañana la respuesta»).
- Siempre 2D. Solo 5 hashtags: #librosinfantiles #educacionfinanciera #regalosniños #booktokespaña #regalosnavidad.
- Enlaces con seguimiento (Amazon Attribution + Bitly): Mi primer dinero = bit.ly/3V2nbiR · Mi goloso negocio = bit.ly/4j5lAko (bio). Escritos en TODAS las descripciones.
- Portada real del libro 1: `libro1/portada_frontal.png`. Cierre del libro 1 con su portada y variante 0 o 1 (la 2 dice «enlace en el perfil»).
- Avisos automáticos de 13:13 y 19:13 PAUSADOS (reactivar solo si Francisco lo pide). Entregar en el momento, no por adelantado. «Publicado» solo si Francisco lo confirma.
- No puedo escuchar audio: identificar voces por duración/tono y pedir a Francisco que lo compruebe.
- Nunca mezclar con «Pasatiempos tóxicos».
