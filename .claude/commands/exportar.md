---
description: Valida y regenera los .docx de las planificaciones
argument-hint: [curso o archivo.yaml]   (sin argumento: todos)
---
Exporta: $ARGUMENTS

1. Identifica los `.yaml` (todos los de `cursos/*/planificaciones/` si no hay argumento).
2. Corre `python scripts/generar_docx.py <archivos>`. Si alguno no valida, informa los errores y corrígelos solo si son evidentes (por ejemplo, un campo `oa:` faltante). Pregunta antes de tocar contenido pedagógico.
3. Haz commit de los .docx regenerados.
4. Entrega los enlaces de GitHub para descargar cada .docx.
