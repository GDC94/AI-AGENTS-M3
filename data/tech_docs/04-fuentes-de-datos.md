# Tecnología — Fuentes de datos
Versión 1.0 — octubre 2026

Este bloque trata de cómo los organismos incorporan sus datos a la plataforma y de qué hacer cuando una carga no sale como se esperaba. Las tareas descritas las realiza el Administrador del organismo o los usuarios con rol Analista que tengan permiso sobre el espacio de trabajo.

## Conectar una base de datos del organismo

Para conectar una base relacional del organismo, el administrador abre la Consola de administración, entra en Conectores y elige Nueva fuente, opción Base de datos. El asistente solicita la dirección del servidor, el puerto, el nombre de la base, el esquema y una cuenta de lectura. Antes de guardar, pulsa Probar conexión y la plataforma informa si pudo llegar a la base.

El servidor del organismo debe aceptar conexiones desde las dos direcciones IP fijas de salida que Atalaya Data publica en el asistente. Estas direcciones deben habilitarse en el cortafuegos del organismo antes de la prueba, porque sin ellas la conexión fracasa con un error de tiempo agotado. La conexión usa siempre un canal cifrado y no se admiten bases que solo acepten conexiones sin cifrar. El asistente permite elegir qué tablas se incorporan, y se recomienda limitarse a las necesarias para los tableros previstos. Una vez creada, la fuente aparece con estado Activa y comienza su primera carga en los diez minutos siguientes.

## Formatos de archivo aceptados

Cuando el organismo no puede abrir su base, puede cargar archivos manualmente desde Conectores, opción Subir archivo. La plataforma acepta cuatro formatos: CSV, XLSX, JSON y XML. En los CSV, la codificación debe ser UTF-8 y el separador puede ser coma o punto y coma, que el sistema detecta solo.

Cada archivo puede pesar hasta 250 MB. Las hojas de cálculo XLSX se leen únicamente en su primera hoja, de modo que los datos de otras hojas deben pasarse a archivos separados. La primera fila de cada archivo se interpreta siempre como los encabezados de las columnas, y esos nombres no pueden repetirse. No se aceptan archivos protegidos con contraseña, ni formatos comprimidos como ZIP, que deben descomprimirse antes de subirse. Tampoco admite la plataforma documentos de texto o PDF, porque no tienen estructura de columnas. Si el archivo contiene fechas, conviene usar el formato AAAA-MM-DD para evitar ambigüedades entre día y mes durante la lectura.

## Frecuencia de actualización de una fuente

Cada fuente conectada tiene una frecuencia de actualización que el administrador define en la pestaña Programación de la fuente. Las opciones son cada 15 minutos, cada hora y una vez al día. La frecuencia predeterminada es diaria, y la carga ocurre a las 02:00 hora del organismo, para no competir con el uso habitual de los tableros.

La frecuencia de 15 minutos solo está disponible para fuentes de base de datos y no para archivos subidos a mano, que se actualizan únicamente cuando alguien los reemplaza. Si una carga tarda más que el intervalo elegido, la siguiente se omite y se retoma en el próximo ciclo, de modo que nunca se superponen dos cargas de la misma fuente. Los tableros muestran siempre, en su pie, la fecha y hora de la última carga exitosa. El administrador también puede lanzar una carga inmediata con el botón Actualizar ahora, hasta un máximo de seis veces por día y por fuente. Los cambios de frecuencia se aplican desde el ciclo siguiente.

## Errores de carga más comunes y su significado

Cuando una carga falla, la plataforma muestra un código de error en la pestaña Historial de la fuente. El código E101 indica que una columna cambió de formato respecto de la carga anterior, por ejemplo un número que ahora trae texto. El código E204 señala que las credenciales de la cuenta de lectura ya no son válidas, sea por vencimiento o por cambio de clave.

El código E310 significa que la base del organismo tardó más de 120 segundos en responder, y suele deberse a consultas demasiado pesadas o a un cortafuegos que bloquea las direcciones de Atalaya Data. Con E415, la plataforma avisa que el archivo supera el tamaño máximo o está dañado. Cada código incluye en pantalla una explicación en lenguaje claro y un enlace a la fila afectada. Si el problema persiste tras corregir lo indicado, el administrador puede abrir un ticket desde el botón Reportar este error, que adjunta de forma automática el historial de la carga y evita tener que describirlo a mano. Los códigos de error no se pueden desactivar ni ocultar.

## Reintentos automáticos y avisos de carga fallida

Si una carga programada falla, la plataforma la reintenta automáticamente hasta tres veces, con 10 minutos de espera entre cada intento. Los reintentos se realizan con la misma configuración, sin intervención de nadie. Si alguno tiene éxito, la fuente queda actualizada y el incidente se cierra sin avisos.

Cuando los tres reintentos fracasan, la fuente pasa al estado Con error y la plataforma envía un correo al responsable de la fuente, designado en la pestaña General, y a los Administradores del organismo. El aviso incluye el código de error, la hora del último intento y el nombre de la fuente. Mientras permanece en ese estado, los tableros siguen mostrando los datos de la última carga correcta y exhiben una advertencia amarilla con la fecha de esa carga. La fuente queda detenida: no se vuelve a intentar sola hasta que alguien pulse Actualizar ahora o repare la causa y reactive la programación. Si el error se repite durante siete días, la plataforma suspende la fuente y envía un último aviso.

## Cuentas de conexión y rotación de credenciales

Las credenciales que la plataforma usa para leer una base del organismo deben corresponder a una cuenta de solo lectura, creada específicamente para Atalaya Data. Una cuenta con permisos de escritura es rechazada en la prueba de conexión, como medida de protección de los propios datos del organismo.

La contraseña de esa cuenta debe cambiarse al menos cada 180 días. Desde el día 150, la plataforma muestra una advertencia en la ficha de la fuente y envía un correo mensual al responsable. La rotación se hace en dos pasos: primero se cambia la clave en el servidor del organismo y después se actualiza en la plataforma, desde la pestaña Credenciales de la fuente, pulsando Actualizar credenciales. Entre un paso y otro la fuente puede fallar con el código E204, por lo que se recomienda hacer ambos cambios en la misma franja horaria. Las credenciales se guardan cifradas y no pueden verse después de guardarlas, ni siquiera el Administrador del organismo puede leerlas: solo puede reemplazarlas.

## Reglas de validación y rechazo de filas

Durante cada carga, la plataforma valida cada fila según el tipo de dato de su columna. Rechaza las filas con fechas imposibles, números con texto o campos obligatorios vacíos. Las filas rechazadas no detienen la carga: se separan y se guardan en un archivo de rechazos que puede descargarse desde la pestaña Historial de la fuente.

Si el porcentaje de filas rechazadas supera el 5 por ciento del total, la carga completa se anula y la fuente conserva los datos anteriores, con el error E102. Este umbral evita que un cambio inesperado en el origen deje tableros con la mitad de la información. El administrador puede ver el motivo de rechazo de cada fila en el archivo, que indica el número de fila y la regla incumplida. Una vez corregido el origen, la fuente se carga completa en el ciclo siguiente. Los archivos de rechazos se conservan 30 días. El umbral del 5 por ciento es fijo y no se puede ajustar por fuente.
