# Tecnología — Auditoría
Versión 1.0 — octubre 2026

Este bloque explica qué registra la plataforma sobre la actividad de los usuarios y cómo consultar esa información. El registro de auditoría es una herramienta de control pensada para los organismos clientes y sus entes de supervisión.

## Qué eventos registra la auditoría

La plataforma registra de forma automática seis tipos de eventos: ingresos y cierres de sesión, consultas de datos, exportaciones, cambios de roles, cambios de clasificación y modificaciones de fuentes de datos. Cada registro incluye el usuario, la fecha y hora con precisión de segundos, la dirección de red de origen y el recurso afectado.

Las consultas de datos se anotan a nivel de conjunto de datos y no de fila individual. Así, el registro indica que una persona abrió un padrón, pero no copia el contenido de lo que vio. También se anotan los intentos fallidos, como contraseñas incorrectas o accesos denegados por falta de permiso. Los registros no pueden modificarse ni borrarse por ningún usuario, ni siquiera por los Administradores del organismo o por el personal de Atalaya Data, porque se guardan en un almacenamiento de solo escritura. Las horas se guardan en horario universal coordinado y se muestran convertidas a la hora local del organismo en la pantalla de consulta. El registro funciona desde la activación de la cuenta del organismo y no puede desactivarse ni reducirse.

## Consultar quién accedió a un dato

Para saber quién vio un conjunto de datos, el usuario con rol Auditor abre el menú Auditoría y elige la pestaña Accesos a datos. Allí selecciona el conjunto, el rango de fechas y, si lo desea, un usuario concreto. La plataforma devuelve una lista ordenada con cada acceso, el rol que tenía la persona en ese momento y el resultado: permitido o denegado.

El Administrador del organismo puede hacer la misma consulta, pero solo sobre conjuntos de datos de los espacios donde participa; el Auditor, en cambio, ve todos los espacios del organismo. Cada consulta de auditoría genera a su vez un registro, de modo que la actividad de los propios auditores también queda controlada. La búsqueda admite rangos de hasta 12 meses por consulta, y muestra 100 resultados por página. Si el rango elegido es mayor, hay que dividirlo en varios períodos. Los filtros por rol, por clasificación del dato y por tipo de resultado se combinan entre sí y se limpian con el botón Restablecer filtros.

## Cuánto tiempo se conservan los registros

Los registros de auditoría tienen dos etapas de conservación. Durante los primeros 24 meses permanecen en línea y pueden consultarse desde el menú Auditoría con respuesta inmediata. Pasado ese plazo se trasladan a un archivo histórico donde se guardan hasta completar 7 años desde su fecha.

Para consultar los registros del archivo histórico, el Auditor debe pedir una recuperación desde la pestaña Archivo histórico, indicando el período. La plataforma tarda hasta 24 horas en dejarlos disponibles y los mantiene visibles durante 7 días. Al cumplirse los 7 años, los registros se eliminan de forma definitiva y no pueden recuperarse. Los plazos son iguales para todos los organismos y rigen sin importar la clasificación de los datos. Un organismo que, por una norma propia, necesite conservar los registros más tiempo debe descargarlos antes del vencimiento y guardarlos en sus propios sistemas, porque Atalaya Data no amplía los plazos de manera individual.

## Descargar el registro de auditoría

El Auditor puede descargar el registro desde Auditoría, con el botón Exportar registro. El archivo se entrega en formato CSV junto con un archivo de firma digital, que permite comprobar más adelante que el contenido no fue alterado después de la descarga.

Cada descarga puede abarcar hasta 90 días de registros. Para períodos mayores hay que hacer varias descargas consecutivas. Si el volumen del período supera las 500.000 filas, la descarga se procesa en segundo plano y llega al Centro de descargas con el mismo plazo de 72 horas que otras exportaciones. El archivo incluye, en su primera línea, el nombre del Auditor, la fecha de generación y los filtros aplicados. El Administrador del organismo no puede descargar el registro completo: solo ve en pantalla los datos de su alcance. Las descargas del registro se anotan en la propia auditoría con el tamaño del archivo. Para verificar la firma digital, el organismo puede solicitar a la Mesa de Ayuda la clave pública vigente de Atalaya Data.

## Alertas por accesos inusuales

La plataforma vigila patrones que pueden indicar un uso indebido y avisa al Administrador del organismo por correo. Se genera una alerta cuando un usuario ingresa fuera del horario habitual, entre las 22:00 y las 06:00, o cuando realiza más de 500 consultas en una hora.

También se avisa ante cinco o más accesos denegados seguidos, y cuando una cuenta ingresa desde dos países distintos en un lapso de seis horas. Cada alerta indica el usuario, el motivo y la hora, y se conserva en la pestaña Alertas del menú Auditoría hasta que un administrador la marque como Revisada, con un comentario obligatorio. Las alertas no bloquean al usuario por sí solas: son informativas, y la decisión de suspender una cuenta corresponde al administrador. Si una alerta permanece sin revisar durante cinco días hábiles, la plataforma la reenvía a todos los administradores del organismo. Los umbrales de 500 consultas y la franja horaria son valores fijos para todos los organismos, y no existe una opción para modificarlos ni para desactivar los avisos.

## Pedir un informe formal de auditoría

Cuando el organismo necesita un informe que valga ante un juzgado, un tribunal de cuentas u otra autoridad, no alcanza con la descarga del Auditor. Debe completar el formulario Solicitud de informe de auditoría, disponible en la sección Soporte del Portal de Clientes, indicando el período, los conjuntos de datos y la autoridad destinataria.

La solicitud solo la aceptan los contactos autorizados del organismo, y debe adjuntar la nota oficial que respalda el pedido. Atalaya Data prepara el informe en un plazo de 10 días hábiles y lo entrega en PDF firmado digitalmente, acompañado de una constancia de integridad de los registros. Si la autoridad requiere el informe en menos tiempo, el organismo puede marcar la opción Urgente, que reduce el plazo a 3 días hábiles y exige que la nota oficial indique el motivo de la urgencia. Cada solicitud recibe un número de seguimiento que el organismo puede consultar en el portal. Los informes se entregan únicamente a la dirección de correo registrada del contacto autorizado, nunca a terceros.
