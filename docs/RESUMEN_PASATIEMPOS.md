# RESUMEN · Pasatiempos tóxicos (Francisco Ruiz) · 25 nov 2026

## 1. Cómo trabajar
- Español de España, respuestas cortas para el móvil. No inventar: usar el guion que dé Francisco y los datos de los libros.
- Calidad PREMIUM siempre (prompts largos y detallados, no básicos).
- No puedo oír audio: Francisco revisa voces y cortes.
- No publicar ni programar sin permiso. Hashtags: máximo 5 y siempre #retos.
- NUNCA mezclar con Bityn. Rama: `claude/pasatiempos-toxicos-navidad-4ysz82` (repo Bytin_R04).

## 2. Los dos libros
### Libro 1 · «Pasatiempos tóxicos · para gente con mala leche»
- Calle del Rencor, 13. Notas anónimas en el espejo del ascensor; 8 pistas; nunca destripar al culpable. Guía en `libro_pt1/guia.md`, texto en `libro_pt1/texto.txt`.
- Interior auditado SIN errores y versión fácil lista: `libro_pt1/Pasatiempos_toxicos_INTERIOR_v3_facil.pdf` (100 págs). Informe: `libro_pt1/AUDITORIA.md`.
- Cubierta NUEVA lista: `libro_pt1/Pasatiempos_toxicos_CUBIERTA_KDP_v3.pdf` (edificio con los 9 vecinos + título con lupa). Vista previa `libro_pt1/portada_nueva_mockup.jpg`. Script `scripts/libro1_portada_nueva.py`.
- PENDIENTE: subir interior y cubierta a KDP; enlace de Amazon del libro 1 (no lo tengo).
### Libro 2 · «Pasatiempos tóxicos · Edición Navidad»
- Misterio del último turrón (23:30, despensa). 6 sospechosos: abuela Paqui, suegra Mari Carmen, cuñado Toni, tía Encarna, primo Iván, perro Chispas. Culpable: no decirlo nunca. Cuñadoku = sudoku con números falsos.
- Interior auditado SIN errores y versión fácil corregida (márgenes OK): `libro_navidad/Pasatiempos_toxicos_Navidad_INTERIOR_KDP_v2_facil.pdf`. Informe: `libro_navidad/AUDITORIA.md`.
- Amazon: https://amzn.eu/d/0gNeRQi6

## 3. Personajes (fichas aprobadas)
- Libro 1 / serie: `docs/libro1_reparto/` → 1.ºA Doña Remedios · 1.ºB Paco «el del taladro» · 2.ºA Vanessa · 2.ºB Don Anselmo · 3.ºA Marisa + su marido Manolo · 3.ºB Iker · 4.ºA Charo y Satanás · 4.ºB misterio. Imagen conjunta `reparto_libro1.png`. Hoja por pisos `libro_pt1/portada_referencia_pisos.png`.
- Navidad: `libro_navidad/fichas/` → Toni, Mari Carmen, abuela Paqui, Iván (Encarna y Chispas sin crear: salen como «?»).
- Fondos: salón de Nochebuena (`libro_navidad/fondo_salon.png`), ascensor y portal (`libro_pt1/v_vecino/`).

## 4. Vídeos hechos
- V01 Navidad «El asesinato del último turrón» (29,6 s): `libro_navidad/V01_ultimo_turron.mp4` + portada + `V01_publicar.md`. Publicado. Medir: retención seg. 1 (>50 %), visionado medio (>10 s), completos, comentarios.
- Libro 1 «El vecino que todos tenemos» (39 s, guion de Francisco): `libro_pt1/V_vecino_que_todos_tenemos.mp4` + portada + `V_vecino_publicar.md`. Pendiente: que Francisco revise audio (Remedios, 4.ºB, Marisa), enlace de Amazon, y cambiar el cierre por la portada nueva.
- Método de producción: fichas → imagen de inicio (personaje recortado sobre fondo, scripts `scripts/cut.py`, `scripts/frames.py`) → Grok vídeo con 1 frase por clip y voz descrita → montaje con `scripts/navidad_v01_build.py` / `scripts/libro1_vecino_build.py` (subtítulos amarillos, SFX, tablero, portada, <3 MB, sin música).

## 5. Próximos pasos
1. Subir a KDP los interiores fáciles de los dos libros y la cubierta nueva del libro 1.
2. Mirar estadísticas del V01 y decidir.
3. Vídeo del vecino: revisar audio, cerrar con portada nueva, publicar.
4. Siguiente vídeo Navidad: V02 «Cuñadoku» (Toni + Mari Carmen + página real del Cuñadoku).
5. Más adelante: serie «La Comunidad del 13» con los vecinos del libro 1 (piloto «El cuñado ahorrador» en `docs/comunidad13_piloto_cunado.md`).

## 6. Técnico
720×1280, 30 fps, H.264 a dos pasadas (<3 MB), AAC. Texto entre y=130 y 1047, x<620. Fuentes en scratchpad: Anton, Baloo 2, Poppins, Bangers, Permanent Marker (`npm pack @fontsource/...`). Grok: imagen 9:16 en el prompt; vídeo desde imagen de inicio; sin texto generado.
