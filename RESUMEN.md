# Resumen del canal · @bityn.y.r04 (18 nov 2026, noche)
Para arrancar un chat nuevo: «Lee RESUMEN.md, PROMPT_MAESTRO.md y CLAUDE.md y sigue». Rama de trabajo: `claude/new-session-ifjtrt` (main está desfasada).

## Ritmo
- **DOS vídeos al día: 13:30 y 19:30** (Madrid). Publicación manual por Francisco.
- **Aviso diario a las 12:37** (tarea programada): manda los dos paquetes del día (mp4 + portada + vNN_publicar.md) leyendo la rama de trabajo. El 18 nov falló por límite de uso de la cuenta.
- Estado «Publicado» en `videos/calendario.md` SOLO cuando Francisco lo confirme. Nunca suponer.

## Publicado
- 17 nov V01 · Reto de los batidos (p.69)
- 18 nov V02 · Respuesta del reto (ojo: sale Bityn en la hucha dorada, escena no del libro)

## Listos (en `videos/` y en Drive, carpeta «Bityn y R-04 · Vídeos TikTok»)
| Día | Hora | Vídeo | Cierre |
|---|---|---|---|
| 19 nov | 13:30 | V03 · ¿A quién se parece tu hijo o hija? (personajes) | 2 |
| 19 nov | 19:30 | V04 · La batería de R-04 (p.3, GK2 p.4, p.4) | 0 |
| 20 nov | 13:30 | V05 · Enigma de X: ¿qué precio salió peor? (p.16-18) | 1 |
| 20 nov | 19:30 | V06 · QR secreto y base de R-04 (p.94, web, 4 PDF) | 2 |
| 21 nov | 13:30 | V07 · ¿Todo el dinero que entra es tuyo? (p.41-42) | 0 |

## Por hacer (urgente: solo hay vídeos hasta el 21 a mediodía)
- 21 nov 19:30 V08 · Regalo de Navidad (usar GK3b Cohete Goloso + voz de R-04, p.14). Cierre 1.
- 22 nov V09 y V10 · por decidir (clips premium de Grok p.3 si llegan).
- Ideas reales del libro aún sin usar: reto pulsera p.20 (2 € vs 3 €), tarta-reloj de X p.24/p.42, Don Gruñón p.29, MegaSnack «¡Todo a 1 €!» p.33, contrato con Brillo p.37, tres botes p.52, escape room p.56-61, recetas p.75.

## Reglas nuevas del 18 nov
- Decir siempre **«tu hijo o hija»** (o «tu peque»), nunca solo «tu hijo».
- No usar formato «Mi hijo me ha enseñado…» como testimonio inventado.
- Clips SOLO con **Grok** (Kling aparcado). Método premium: imagen nueva 9:16 en Grok adjuntando la ficha oficial `kling/ficha_bityn_r4.jpg` + escena real con página; luego animar con poco movimiento. Editar viñetas en Grok NO funciona (cambia personajes). Imagen inicial siempre 9:16 (si no, sale apaisado). No escribir «drone» (pone hélices). Voz de R-04: «tiny toy robot, high-pitched, metallic, NOT a human voice, NOT a child's voice».
- Pendientes de Grok: GK4 = p.3 voltereta y caída («¡Mira, Bityn! ¡Triple voltereta con tirabuzón!» / «Bip… bip… bi…»), GK5 = p.3 rescate («¡¡R-04!!»). Prompts en el chat del 18 nov (también resumidos en CLAUDE.md).
- Errata del libro p.16 (nota de X): «vendréis» → «venderéis».

## Reglas de siempre (detalle en CLAUDE.md)
Público: padres (no niños) · Gancho en el 1.er segundo · Sin música · Edad 8-12 en cierre y descripción · Zonas seguras (y≤1047, x≤620) · Variedad total (no repetir clips ni cierre seguidos) · NO inventar escenas: todo con página del libro · Revisar hoja de fotogramas antes de entregar.

## Material
- Clips: `kling/clips` (G1-G3, GK2 Sr. Tornillo p.4, GK3b Cohete Goloso p.14). GK1 (hucha) = inventado, no usar.
- Montaje: `montaje/lib.py` (3 cierres) y `montaje/v01…v07_*.py`. Fuentes/SFX: `npm pack @fontsource/baloo-2@5.3.0 uisfx@0.4.0`.
- Libros leídos: `libro/guia_contenido.md` (libro 2) y `libro1/guia_contenido.md` (libro 1).

## Otros pendientes
- Seguridad: dejar privados en Drive los PDF/carpetas compartidos por enlace.
- Tras 1-2 semanas: pedir estadísticas de TikTok y ajustar horas y formatos.
