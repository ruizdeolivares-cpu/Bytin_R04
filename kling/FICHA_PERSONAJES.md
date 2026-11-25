# Ficha de personajes · Bityn y R-04 (para guiones y Grok)
Referencia visual oficial: `kling/ficha_bityn_r4.jpg`. Recortes limpios: `kling/recorte_bityn_34.png`, `kling/recorte_r04_frontal.png`.

## BITYN
- **Qué es:** robot explorador humanoide (NO un niño). Protagonista de los dos libros.
- **Aspecto:** cuerpo crema/blanco con articulaciones naranjas y negras; cabeza redonda con visor negro; ojos = líneas o arcos naranjas luminosos (SIN boca, SIN nariz); antena negra a un lado y una oreja naranja puntiaguda al otro; manos negras; botas crema con suela negra. En el libro 1 y 2 suele llevar delantal de rayas verdes (food truck).
- **Expresiones del visor (ficha):** neutro (línea), feliz (arcos), risas (> <), sorprendido (dos rayas verticales), curioso (?), seguro (estrella).
- **Personalidad:** entusiasta, impulsivo, soñador («¡Somos millonarios!»), cariñoso con R-04; aprende a hacer cuentas a base de errores.
- **Voz:** robot joven, alegre, ligeramente metálica. Nunca voz de niño humano.
- **Frases reales (con página):**
  - «¡Quiero participar en la Carrera del Horizonte!» (L1 p.5)
  - «¡Es mucho! Pero no es imposible. Solo necesito un plan.» (L1 p.6)
  - «6 € parecen poco… hasta que recuerdas que voy camino de 280.» (L1 pág. 14)
  - «Prefiero tenerte funcionando que 10 € más sin ti.» (L1 pág. 36)
  - «¡164 euros! ¡Nos sobra!» (L2 p.41) · «¿¡Solo 94!?» (L2 p.41)
  - «Tranquilo, R-04. En 30 días tendré ese dinero. Te lo prometo.» (L2 p.4)
  - «Batido Nebulosa: ¡50 euros! Con tres ventas, ¡chip pagado!» (L2 p.17)
- **Nunca:** boca, dientes, cejas humanas, ropa de niño, aspecto 3D realista, hablar como un adulto sabiondo.

## R-04
- **Qué es:** pequeño robot esférico que flota (NO un dron con hélices). Mejor amigo de Bityn.
- **Aspecto:** esfera crema con detalles negros; cara negra con UN SOLO ojo en forma de anillo naranja luminoso (en momentos felices, dos arcos); dos alas curvas laterales (crema por fuera, negras por dentro); gorrito redondo arriba. SIN boca, SIN nariz, SIN hélices.
- **Expresiones (ficha):** feliz girando, con cariño (corazones), sorprendido, dormido (zzz), curioso (?), a toda velocidad, apoyando (¡bien!), inquisitivo.
- **Personalidad:** lógico, frío por fuera y tierno por dentro; hace las cuentas; misterioso (guarda secretos: Ruta 04, archivos antiguos).
- **Voz:** robot de juguete pequeño, aguda, metálica, plana como un ordenador, con «bips». En el libro 1 habla en MAYÚSCULAS.
- **Frases reales (con página):**
  - «GASTO PEQUEÑO DETECTADO.» (L1 pág. 13)
  - «SI COMPRAS UNA BEBIDA DE 2 € DURANTE CINCO DÍAS, GASTARÁS 10 €.» (L1 pág. 15)
  - «CARIÑO DETECTADO. NO SÉ DÓNDE GUARDARLO.» (L1 pág. 36)
  - «NEGATIVO. ESTABILIDAD DISMINUYENDO.» (L1 pág. 33)
  - «EL TRABAJO DA DINERO, PERO LOS GASTOS RESTAN UNA PARTE.» (L1 p.7-8)
  - «Bip. Momento. Estar en tu bote no significa que sea tuyo.» (L2 p.41)
  - «Bip… batería baja… pero ánimo alto.» (L2 p.2)
  - «Bip… bip… bi…» (L2 p.3, cuando se queda sin batería)
- **Nunca:** hélices, dos ojos redondos normales, boca, brazos fijos (solo saca brazos mecánicos finos en algunas viñetas), parecer un dron real.

## Prompt base para Grok (pegar siempre; la 1.ª línea va SIEMPRE dentro del prompt, además de elegirlo en los botones de Grok)
```
Vertical 9:16, maximum quality, 10 seconds, with audio.
2D cartoon animation, flat 2D, hand-drawn look. NOT 3D, NOT CGI, NOT realistic.
Animate this image. Keep the first frame EXACTLY: same characters, same design, same colors, same proportions in every frame. Static camera.
[ACCIÓN CORTA · máx. 12 s]
[DIÁLOGO en español de España + tipo de voz]
STRICTLY FORBIDDEN: 3D look, changing the characters, new parts, propellers, mouths, noses, a second eye on the small round robot, new characters, humans, text, subtitles, logos, watermark, music, morphing, style change.
```
Voces: tall robot = «young cheerful robotic voice, slightly metallic» · small round robot = «tiny toy-robot voice, high-pitched, metallic, flat like a computer, short beeps». Siempre «NOT a human voice, NOT a child's voice».

## Prompt ESTRICTO (22 nov, usar siempre a partir de ahora)
```
Vertical 9:16, maximum quality, 10 seconds, with audio.
STYLE LOCK: 2D cartoon, flat 2D, hand-drawn look. NOT 3D, NOT CGI, NOT realistic.
CINEMAGRAPH MODE: this is a near-still image. Do NOT redraw, re-pose, re-design or re-animate the characters. Keep the first frame pixel-identical; ONLY the parts listed under ALLOWED MOTION may move, everything else stays frozen.
CHARACTER LOCK (must stay identical in EVERY frame):
- Tall robot: exactly ONE black antenna on his left side and exactly ONE orange pointed ear on his right side (never two antennas, never two ears); black visor with two orange glowing lines as eyes; NO mouth, NO teeth, NO nose, NO eyebrows, even while speaking; cream body with orange and black joints; black hands.
- Small round robot: cream sphere floating in the air; black face with exactly ONE orange glowing ring eye; two curved side wings; one round cap on top; NO antenna, NO propellers, NO mouth, NO nose, NO second eye, NO arms.
ALLOWED MOTION: [MOVIMIENTO MÍNIMO]
CAMERA: locked, static, no zoom, no pan, no cuts.
AUDIO: [VOZ]
Speaking NEVER changes the faces: no mouth movement, no new facial features.
STRICTLY FORBIDDEN: 3D, redesign, extra antenna, missing ear, mouths, lip sync, smiles with teeth, noses, second eye, antenna on the small robot, propellers, extra limbs, morphing, melting, flicker, new characters, humans, text, letters, subtitles, logos, watermark, music, background change, style change.
```

## Fichas de Lía, Sr. Tornillo y Brillo (para los vídeos 2, 4 y 5 de la campaña)
Base: `kling/personajes/ficha_secundarios.png` (1774×887, cuerpo entero y nítido) + fichas secretas p.77-78 del libro 2.
Prompt de Grok (imagen, horizontal 16:9, máxima calidad; adjuntar ficha_secundarios.png; una ficha por personaje):
```
Character model sheet of [LÍA = the blue alien girl with chef hat / SR. TORNILLO = the golden clockmaker robot / BRILLO = the silver egg robot] from the attached image. Copy the character EXACTLY: same shapes, colours, clothes and accessories, nothing added, nothing removed.
2D cartoon, flat colours, clean lines, white background.
Left: full body front view, 3/4 view, side view and back view, same size, standing neutral.
Right: 6 head close-ups with different expressions (happy, laughing, surprised, curious, worried, proud).
Bottom: 4 small colour swatches of the palette.
No text, no letters, no labels, no logos, no watermark, no other characters.
```
Detalles a comprobar: Lía = 2 antenas con bolas rosas, gorro de chef, peto vaquero, tiritas naranjas en las rodillas, zapatillas rosas, batidora rosa · Sr. Tornillo = cuerpo redondo dorado, bigote de muelles blanco, monóculo dcho., chaleco de cuero con herramientas, engranajes en la barriga, pomo arriba · Brillo = huevo plateado, gafas de sol negras, sonrisa enorme, brazos y piernas metálicos, megáfono rojo/blanco.
