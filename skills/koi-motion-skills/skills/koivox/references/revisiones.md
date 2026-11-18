# Brief, fixes y versiones

Una conversación larga se confunde y empieza a ignorar las referencias. Por eso el proyecto vive en archivos y no en la memoria del chat.

## Archivos

| Archivo | Qué tiene |
|---|---|
| `BRIEF.md` | Historia, reglas de look (de `estilo.md` y `analisis-referencias.md`), lista de "nunca", duración y fuentes de cada dato. Solo lo aprobado. Se toca únicamente si el usuario cambia una decisión. |
| `FIXES.md` | Rondas numeradas de cambios: `## Ronda 3 (sobre v03)` y debajo `3.1`, `3.2`… Cada ítem dice qué escena, qué se ve mal y qué tiene que pasar. |
| `Export/borradores/vNN.mp4` | Una versión por ronda. Nunca se pisa una anterior. Las viejas van a la Papelera solo con el OK del usuario, una vez entregado el video ([entrega.md](entrega.md)). |

## Dos roles

- **Project manager (esta conversación):** convierte las notas del usuario en `FIXES.md`. Si algo no está claro, hace **una sola** pregunta. No construye.
- **Constructor:** lee `BRIEF.md` y la última ronda de `FIXES.md`, cambia **solo** eso y renderiza la versión siguiente. Si el contexto ya está cargado, se lanza un subagente con esta consigna:

```text
Leé BRIEF.md y la Ronda N de FIXES.md en <carpeta>. Aplicá solo esos cambios en tools/build.py; todo lo demás queda igual.
Antes de renderizar revisá cada escena: ¿quién es?, ¿por qué está ahí?, ¿podría pasar de verdad?
Renderizá Export/borradores/vNN.mp4 con render.sh a 120. No toques versiones anteriores.
Devolvé la lista de ítems hechos y cualquiera que no pudiste hacer.
```

## Notas del usuario

- Pedir **todas las notas juntas** después de ver el video entero. Cada nota suelta es un render más.
- No hace falta el minuto exacto. Alcanza con describir qué se ve: "en la oficina los brazos flotan".
- Cuando una versión gusta, se congela: la siguiente parte de ella y no se reconstruye de cero.
- Borradores a 120. El render a 240 va solo cuando no quedan notas.
