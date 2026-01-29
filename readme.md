# Guía de Estandarización - Ingesta de Datos de Campañas de Email

## Objetivo
Establecer criterios claros para el registro de campañas y bases de datos que permitan:
- Análisis más eficientes
- Visualizaciones consistentes
- Seguimiento histórico confiable
- Comparaciones válidas entre campañas

---

## 1. NOMENCLATURA DE CAMPAÑAS

### Estructura Estándar
```
Email [NÚMERO] - [TIPO/TEMA] - [DETALLE OPCIONAL]
```

### Ejemplos:
- ✅ `Email 115 - Espacios Verdes`
- ✅ `Email 114 - Resumen 2025`
- ✅ `Email 113 - Info Servicios Fin de Año`
- ❌ `Email SN - News al 27 de junio` (usar número consecutivo)

### Reglas:
1. **Siempre usar número consecutivo** (nunca "SN" = Sin Número)
2. Mantener el formato corto y descriptivo
3. Evitar fechas en el nombre (ya está en la columna Fecha)
4. Usar mayúsculas iniciales consistentemente

---

## 2. ESTANDARIZACIÓN DE BASES DE DATOS

### Bases Identificadas en el Sistema Actual

#### A) Base Principal
- **Estándar:** `Completa`
- **NO usar:** 
  - ❌ "Completa sin barrio"
  - ❌ "Completa - excluyendo Deportes"
  - ❌ "Completa (menos San Isidro + Martinez + Acassuso)"

#### B) Bases Segmentadas por Geografía
**Estándar para localidades:**
- `San Isidro`
- `Martínez`
- `Acassuso`
- `Villa Adelina`
- `Boulogne`
- `Beccar`
- `La Horqueta`

**Combinaciones geográficas:**
- `Martínez y Acassuso` (cuando son dos localidades específicas)
- `San Isidro, Martínez y Acassuso` (cuando son tres o más)

#### C) Bases Segmentadas por Perfil
- `Empleados Municipales`
- `Base Empleados de Salud`
- `Base Deportes`
- `Comerciantes`
- `Proveedores`
- `Base Jóvenes`

#### D) Bases de Remarketing
**Formato estándar:**
```
RMKT NA - [Base Original]
```

**Ejemplos:**
- ✅ `RMKT NA - Completa`
- ✅ `RMKT NA - Empleados Municipales`
- ✅ `RMKT NA - Beccar`

**NO usar:**
- ❌ "vecinos que se anotaron" → usar `Anotados` o `Inscriptos`
- ❌ "Vecinos contactados por call center" → usar `Anotados Call`

#### E) Bases de Eventos Específicos
Para eventos con inscripción:
- `Anotados` (genérico)
- `Inscriptos` (para capacitaciones)
- `Anotados Call` (contactados por call center)

---

## 3. REGLAS PARA SEGMENTACIONES COMPLEJAS

### Caso 1: Exclusiones de la Base Completa
**Problema actual:**
```
❌ "Completa - excluyendo Deportes"
❌ "Completa (menos San Isidro + Martinez + Acassuso)"
```

**Solución:**
Crear base con nombre propio o usar campo de "Segmento Excluido" en otra columna

**Alternativa:**
- Si la exclusión es menor: `Completa`
- Si la exclusión es significativa: crear nombre específico como `Base Interior` o `Base Localidades Norte`

### Caso 2: Vencimientos de Licencias
**Problema actual:**
```
❌ "Completa 19 + 20 + 21 + 22 + 23 + 24 + 25 / 25"
```

**Solución:**
- Base: `Completa`
- Agregar columna "Segmento" con valor: `Vencimientos Marzo 19-25`

### Caso 3: Múltiples Envíos de la Misma Campaña
**Manejo en planilla:**

| Fecha | Campaña | Base | Enviados |
|-------|---------|------|----------|
| 20/3/2025 | Email 02 - Lollapalooza | San Isidro, Martínez y Acassuso | 51,669 |
| 20/3/2025 | Email 02 - Lollapalooza | Resto Interior | 47,007 |

**NO duplicar la fecha de fila** para mostrar remarketing en otra columna

---

## 4. ESTRUCTURA DE COLUMNAS REQUERIDAS

### Columnas Obligatorias
1. **Fecha** - formato DD/MM/AAAA
2. **Campaña** - nombre estandarizado
3. **Base** - según nomenclatura estándar
4. **Asunto** - texto literal del email
5. **Enviados** - número sin formato
6. **Abiertos** - número sin formato
7. **OR** - porcentaje con formato %
8. **Clics** - número sin formato
9. **CTR** - porcentaje con formato %
10. **CTOR** - porcentaje con formato %
11. **Desuscripción** - número sin formato
12. **% Des** - porcentaje con formato %

### Columnas Opcionales (recomendadas)
13. **OR Global** - para remarketing
14. **Segmento** - para detalles adicionales sin contaminar el campo Base
15. **Tipo de Campaña** - News / Institucional / Evento / Servicio
16. **Notas** - observaciones especiales

---

## 5. CATÁLOGO DE BASES ESTANDARIZADAS

### Tabla de Referencia

| Tipo | Nombre Estándar | Usar en lugar de... |
|------|----------------|---------------------|
| Principal | `Completa` | "Base completa", "Todos", "General" |
| Geográfica | `[Localidad]` | Nombre exacto sin variaciones |
| Geográfica combinada | `[Local1] y [Local2]` | Usar "y" como separador |
| Empleados | `Empleados Municipales` | "Base Municipales", "Empleados Muni" |
| Empleados Salud | `Base Empleados de Salud` | "Empleados de Salud", "Personal Salud" |
| Deportes | `Base Deportes` | "Deportes", "Inscriptos Deportes" |
| Remarketing | `RMKT NA - [Base]` | "Retargeting", "No Abiertos" |
| Inscriptos genérico | `Anotados` | "Inscriptos", "Registrados" |
| Capacitaciones | `Inscriptos` | "Anotados a capacitación" |
| Call center | `Anotados Call` | "Contactados call", "Base Call" |
| Comercios | `Comerciantes` | "Base Comercios", "Negocios" |
| Proveedores | `Proveedores` | Sin variaciones |
| Jóvenes | `Base Jóvenes` | "Juventud", "Jóvenes" |

---

## 6. CASOS ESPECIALES Y CÓMO RESOLVERLOS

### A) Test A/B o Múltiples Asuntos
**Opción 1:** Crear filas separadas
```
Email 115 - Test A | Asunto 1 | Base Completa 50% | ...
Email 115 - Test B | Asunto 2 | Base Completa 50% | ...
```

**Opción 2:** Usar columna adicional "Variante"

### B) Envíos por Lotes
Para segmentaciones por fecha de vencimiento u otro criterio temporal:
- Base: `Completa`
- Segmento: `Lote 1 - Vencimientos 01-05/25`

### C) Eventos con Múltiples Fechas
**Ejemplo: Ojos en Alerta con varias capacitaciones**

Opción recomendada:
- Campaña única: `Email XX - Ojos en Alerta [Mes]`
- Base: `Completa` (para convocatoria)
- Base: `Inscriptos [Localidad]` (para recordatorios)

---

## 7. PROCESO DE CARGA

### Checklist Pre-Carga
- [ ] Verificar que el número de campaña es consecutivo
- [ ] La base está en el catálogo estandarizado
- [ ] No hay información redundante en múltiples columnas
- [ ] Los porcentajes están calculados correctamente
- [ ] Las fechas tienen formato consistente
- [ ] No hay filas duplicadas por error

### Validaciones Automáticas Sugeridas
```python
# Pseudocódigo de validación
if base not in BASES_ESTANDARIZADAS:
    alert("Base no estándar detectada: revisar")

if "Completa" in base and any(exclusion_keyword in base):
    alert("Base Completa con exclusiones: considerar renombrar")

if campaña contains "SN":
    alert("Campaña sin número: asignar número consecutivo")
```

---

## 8. BENEFICIOS DE LA ESTANDARIZACIÓN

✅ **Análisis más rápidos:** Filtros funcionan correctamente
✅ **Comparaciones válidas:** Mismas bases se pueden trackear en el tiempo
✅ **Visualizaciones limpias:** Gráficos sin duplicados de categorías
✅ **Reportes automatizables:** Los dashboards funcionan sin ajustes manuales
✅ **Onboarding más fácil:** Nuevos miembros entienden la estructura rápidamente

---

## 9. EJEMPLOS ANTES/DESPUÉS

### ❌ ANTES (No Estandarizado)
```
Fecha: 13/1/2026
Campaña: Email 115 - Espacios Verdes
Base: Completa
---
Fecha: 26/12/2025
Campaña: Email 114 - Resumen cómo fue 2025
Base: Completa
---
Fecha: 22/12/2025
Campaña: Email 111- News al 17/12
Base: RMKT NA - Completa
(nota: sin espacio después del número, guión inconsistente)
```

### ✅ DESPUÉS (Estandarizado)
```
Fecha: 13/01/2026
Campaña: Email 115 - Espacios Verdes
Base: Completa
---
Fecha: 26/12/2025
Campaña: Email 114 - Resumen 2025
Base: Completa
---
Fecha: 22/12/2025
Campaña: Email 111 - News 17/12
Base: RMKT NA - Completa
```

---

## 10. CONTACTO Y DUDAS

Para casos no contemplados en esta guía:
1. Consultar con el equipo de análisis antes de crear nuevas categorías
2. Documentar el nuevo caso en este documento
3. Comunicar al equipo la actualización

**Fecha última actualización:** Enero 2026
**Próxima revisión:** Trimestral