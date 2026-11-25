# Planificación — Prof. Felipe Jiménez · Colegio San Agustín

Repo de trabajo para un agente (Claude) que analiza programas, planifica, registra clases y evaluaciones, y reestructura unidades.
Las reglas del agente están en [`CLAUDE.md`](CLAUDE.md) y el formato institucional en [`formato/FORMATO.md`](formato/FORMATO.md).

## Flujo

```
programa (OA) ──► /planificar-unidad ──► U<n>.yaml ──► .docx (formato UTP)
                                             ▲
clase ──► /registrar-clase ──► registros/    │
prueba ──► /analizar-evaluacion ──► logro ───┴── /reestructurar
```

## Uso desde el celular

Abre una sesión de Claude con este repo y pide, por ejemplo:

- `/registrar-clase 2M-fisica hoy vimos impulso, la mitad no entendió Δp, faltó el experimento`
- `/analizar-evaluacion 2M-fisica` (y adjunta el Excel de notas por pregunta)
- `/reestructurar 2M-fisica`

Los .docx se descargan desde `cursos/<curso>/planificaciones/docx/`.

## Generar a mano

```
pip install -r requirements.txt
python scripts/generar_docx.py cursos/2M-fisica/planificaciones/2027/U3-energia-momentum.yaml
```

## Cursos

| Curso | Planificaciones |
|---|---|
| `1M-biologia` | 2027: 4 unidades, 36 semanas (borrador) |
| `1M-fisica` | 2027: 4 unidades, 36 semanas (borrador) + 2026: U4 |
| `2M-biologia` | 2027: 4 unidades, 36 semanas (borrador) |
| `2M-fisica` | 2027: 4 unidades, 36 semanas (borrador) + 2026: U3 |
| `5B-biologia` | 2027: 2 unidades, 36 semanas (borrador) |
| `5B-fisica` | 2027: 2 unidades, 36 semanas (borrador) |
| `6B-biologia` | 2027: 2 unidades, 36 semanas (borrador) |
| `6B-fisica` | 2027: 3 unidades, 36 semanas (borrador) |

5° y 6° Básico: Ciencias Naturales separada por ejes (Biología = Ciencias de la vida; Física = Físicas y químicas + Tierra y Universo).
Programas completos, incluido el eje Química, en `programas/<nivel>/`.
