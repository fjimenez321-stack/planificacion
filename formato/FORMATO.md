# Formato institucional de planificación (UTP 2026)

Molde: `plantilla_planificacion.docx` (hoja horizontal). **No modificar sin acuerdo de UTP.**

## Estructura del documento (en este orden)

1. **Título** centrado: `COLEGIO SAN AGUSTIN VILLA ALEMANA` / `UNIDAD TECNICO PEDAGOGICA 2026`
2. **Tabla de encabezado** (1 fila × 2 columnas)
   - Izquierda: `UNIDAD <N romano>: <nombre>` · `Profesor (a): …` · `Curso: …`
   - Derecha: `Asignatura: …` · `Mes: …`
3. **Tabla de propósito** (3 columnas): `Propósito` | `Eje y Objetivo de aprendizaje` | `Duración`
4. **Tabla semanal** (6 columnas, una fila por semana):
   `Semana` | `Tema` | `Actividades` | `Objetivos Específicos` | `Nivel Bloom` | `Evaluación Formativa`
5. **Nota final** (opcional): título en negrita + texto en cursiva. Normalmente justifica la progresión Bloom.

## Campos del .yaml

| Campo | Contenido |
|---|---|
| `estado` | `borrador` · `vigente` · `ejecutada` (no se imprime) |
| `version` | entero; sube con cada reestructuración (no se imprime) |
| `encabezado.unidad` | `UNIDAD III: Energía mecánica…` |
| `encabezado.profesor` / `curso` / `asignatura` / `mes` | texto |
| `proposito` | un párrafo |
| `objetivos[]` | `oa` (código) + `texto` literal del programa |
| `duracion` | `Dos meses`, `6 semanas`… |
| `semanas[].semana` | número |
| `semanas[].oa` | lista de OA que trabaja (no se imprime; obligatorio para la trazabilidad) |
| `semanas[].tema` | breve; sale en negrita |
| `semanas[].actividades` | concretas: metodología + recurso |
| `semanas[].objetivos_especificos` | verbo Bloom + contenido |
| `semanas[].bloom` | uno o dos de: Recordar, Comprender, Aplicar, Analizar, Evaluar, Crear (separados por ` / `) |
| `semanas[].evaluacion_formativa` | instrumento; si hay sumativa, se indica aquí (`Evaluación N°1 (OA11)`) |
| `nota.titulo` / `nota.texto` | opcional |

## Criterios de calidad

- Progresión Bloom de menor a mayor orden dentro de cada ciclo de OA.
- Cada semana tiene al menos un instrumento de evaluación formativa.
- Hay al menos una evaluación sumativa por OA.
- Las actividades incluyen trabajo práctico o experimental cuando el OA lo permite.

Ejemplo completo: `cursos/2M-fisica/planificaciones/U3-energia-momentum.yaml`.
