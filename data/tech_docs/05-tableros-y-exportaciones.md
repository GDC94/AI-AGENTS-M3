# Tecnología — Tableros y exportaciones
Versión 1.0 — octubre 2026

Este bloque describe cómo se construyen, comparten y exportan los tableros de la plataforma. Está dirigido a los usuarios de los organismos con rol Editor de tableros o superior (Editor de tableros o Administrador del organismo), salvo donde se indica lo contrario.

## Crear un tablero nuevo

Para crear un tablero, el usuario con rol Editor de tableros abre el espacio de trabajo donde quiere guardarlo y pulsa el botón Nuevo tablero. La plataforma pide un nombre, que debe tener entre 5 y 80 caracteres, y una descripción opcional. Después se elige la fuente de datos principal entre las que el usuario tiene permiso de ver.

El tablero nace vacío, con una cuadrícula de 12 columnas, y se guarda automáticamente como borrador cada 30 segundos. Un borrador solo lo ve su autor hasta que pulsa Publicar. Al publicar, el tablero queda visible para las personas con quienes se comparta. La plataforma conserva las últimas 20 versiones publicadas, y desde el menú Historial se puede volver a cualquiera de ellas. Un tablero puede tener un máximo de 8 pestañas. Si el espacio de trabajo ya contiene un tablero con el mismo nombre, la plataforma agrega el sufijo "(2)" para distinguirlos. El nombre puede cambiarse más adelante sin perder los enlaces ni las programaciones de envío existentes.

## Agregar y configurar gráficos en un tablero

Dentro del tablero, el botón Agregar gráfico abre una galería con cinco tipos de visualización: barras, líneas, mapa, tabla y indicador numérico. El usuario elige el tipo, arrastra los campos de la fuente a los ejes y define los filtros. Los cambios se ven en una vista previa antes de aceptarlos.

Cada tablero admite hasta 12 gráficos, un límite que protege el tiempo de carga. Los gráficos de tipo mapa requieren que la fuente tenga una columna de código geográfico reconocido, como provincia o municipio. Las tablas muestran por pantalla un máximo de 1.000 filas, con paginación, aunque la fuente tenga más. Un gráfico puede duplicarse con la opción del menú de tres puntos, y puede moverse o redimensionarse arrastrando sus bordes. Los filtros globales del tablero, ubicados en la barra superior, afectan a todos los gráficos que usan la misma fuente. Para evitar resultados engañosos, la plataforma no permite combinar en un mismo gráfico datos de dos fuentes sin una columna en común.

## Compartir un tablero con otros usuarios

El propietario de un tablero lo comparte desde el botón Compartir, en la esquina superior derecha. Allí busca a la persona por nombre o correo y le asigna uno de dos permisos: Ver, que permite consultar el tablero, o Editar, que además permite modificarlo. Solo se puede compartir con usuarios del mismo organismo.

También es posible compartir con un espacio de trabajo entero, en cuyo caso todos sus miembros reciben el permiso elegido. Un usuario con permiso Editar puede cambiar el contenido, pero no puede eliminar el tablero ni transferirlo, algo que solo hace el propietario. Si alguna persona no tiene el nivel de clasificación necesario para ver los datos del tablero, la plataforma lo advierte y no permite completar la acción. La lista de personas con acceso se consulta en la misma ventana y se modifica en cualquier momento. Quitar un permiso tiene efecto inmediato y el usuario pierde el tablero de sus listados. Cada vez que se comparte, el destinatario recibe un aviso por correo con el nombre del tablero y de quién lo compartió.

## Enlaces de solo lectura con vencimiento

Los tableros de clasificación Pública pueden compartirse también con personas ajenas a la plataforma mediante un enlace de solo lectura. El propietario lo genera desde Compartir, pestaña Enlace, y pulsa Crear enlace. Quien lo abra ve el tablero actualizado, sin poder editar ni acceder a nada más.

Todos los enlaces vencen. El plazo predeterminado es de 7 días y el máximo permitido es de 30 días, que se elige al crear el enlace. Pasado el plazo, el enlace deja de funcionar y hay que crear uno nuevo. El propietario puede revocarlo antes del vencimiento con el botón Desactivar enlace, y el efecto es inmediato. Un tablero puede tener como máximo tres enlaces vigentes a la vez. Los tableros Reservados y Secretos no admiten enlaces, y si un tablero con enlaces activos sube de clasificación, todos sus enlaces se desactivan al instante y el propietario recibe un aviso por correo. Cada visita a un enlace queda registrada en la auditoría con la fecha y la dirección de origen.

## Exportar un tablero a CSV o PDF

Desde el menú Exportar, ubicado en la barra de cada tablero, se puede descargar el contenido en dos formatos. El CSV contiene los datos de un gráfico o tabla seleccionados, con encabezados y codificación UTF-8. El PDF reproduce el tablero tal como se ve en pantalla, incluida la franja de clasificación.

La exportación directa tiene límites: un CSV puede incluir hasta 100.000 filas, y un PDF hasta 30 páginas. Los archivos se descargan al instante cuando están dentro de esos topes. Si el pedido los supera, la plataforma ofrece pasar a la exportación diferida. Solo los usuarios con rol Analista o superior (Analista, Editor de tableros o Administrador del organismo) pueden exportar a CSV, mientras que el PDF está disponible para todos los roles que ven el tablero. Cada archivo exportado lleva en el pie el nombre del usuario, la fecha y la clasificación del contenido. Los datos Secretos no se pueden exportar en ningún formato. Toda exportación queda anotada en la auditoría, con el tamaño y el formato del archivo generado.

## Exportaciones diferidas de gran volumen

Cuando un CSV supera las 100.000 filas, se usa la exportación diferida. El usuario elige Exportar, indica el formato y pulsa Solicitar exportación diferida. La plataforma procesa el pedido en segundo plano, sin necesidad de mantener abierta la pantalla, y avisa por correo cuando está listo.

La demora habitual es de hasta dos horas, según la cola de pedidos. El archivo aparece en el Centro de descargas, en el menú de la esquina superior derecha, y puede bajarse durante 72 horas. Después se elimina y hay que repetir el pedido. El tamaño máximo es de 2 millones de filas por archivo; si los datos superan esa cifra, el usuario debe filtrar el tablero y hacer varias exportaciones. Cada usuario puede tener hasta tres exportaciones diferidas en curso al mismo tiempo. Los archivos del Centro de descargas son personales: otra persona del organismo no puede verlos ni siquiera con el rol de administrador, y solo puede descargarlos quien los solicitó.

## Programar el envío periódico de un tablero

Un tablero puede enviarse por correo de manera automática a quienes lo necesiten. El propietario abre el tablero, elige Programar envío y define la frecuencia: diaria, semanal o mensual. Los envíos semanales salen los lunes a las 07:00 hora del organismo, y los mensuales el primer día hábil del mes a la misma hora.

El mensaje incluye un PDF del tablero con los datos vigentes en el momento de enviarlo. Los destinatarios deben ser usuarios activos del mismo organismo, con permiso de ver el tablero; la plataforma no envía a direcciones externas. Un tablero puede tener hasta cinco programaciones y cada una admite hasta 20 destinatarios. Si en el momento del envío la última carga de datos falló, el correo lleva una nota que lo advierte con la fecha de los datos usados. Los tableros Reservados se envían solo al correo institucional, y los Secretos no pueden programarse. Para detener un envío basta con eliminar la programación desde el mismo menú, o con que el destinatario use el enlace de baja del correo.
