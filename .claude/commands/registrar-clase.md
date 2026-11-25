---
description: Registra lo que pasó en una clase (desde un dictado o una nota libre)
argument-hint: <curso> [fecha] <lo que pasó>
---
Registra esta clase: $ARGUMENTS

1. Identifica el curso, la fecha (si no viene, usa la de hoy en America/Santiago) y la unidad y semana vigentes según el `.yaml` con `estado: vigente`.
2. Si el texto trae nombres de alumnos, reemplázalos por códigos y avísale a Felipe (Regla 3). Si no hay código para un alumno, escribe `[alumno]`.
3. Crea `cursos/<curso>/registros/AAAA-MM-DD.md` usando `cursos/<curso>/registros/_plantilla.md`. Si ya existe un registro de ese día, agrega una sección `## Bloque 2`.
4. Completa lo que se pueda inferir del texto. **No inventes porcentajes**: si Felipe no dio números, deja `logro_estimado: sin dato`.
5. Compara con la planificación:
   - ¿Se cumplió lo planificado para esa semana? Si no, ¿qué quedó pendiente?
   - ¿Hay señales de alerta? (por ejemplo: "no entendieron", "faltó tiempo", "muchos ausentes").
6. Si hay una alerta, termina sugiriendo `/reestructurar`, pero no reestructures sin que Felipe lo pida.
7. Haz commit: `registro: <curso> <fecha>`.
