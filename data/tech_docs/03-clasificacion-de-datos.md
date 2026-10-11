# Tecnología — Clasificación de datos
Versión 1.0 — octubre 2026

Este bloque explica cómo la plataforma etiqueta los datos de los organismos según su sensibilidad y qué reglas aplica a cada etiqueta. La clasificación determina quién puede ver cada conjunto de datos y qué se puede hacer con él.

## Niveles de clasificación de los datos

Todo conjunto de datos de la plataforma tiene exactamente una clasificación, que puede ser Público, Reservado o Secreto. Público corresponde a información que el organismo ya difunde o que puede difundir sin restricciones, como estadísticas abiertas. Reservado es el nivel para datos de uso interno, como padrones, expedientes o indicadores de gestión que no deben salir del organismo.

Secreto se destina a información cuya divulgación podría afectar la seguridad, la salud pública o los derechos de las personas, por ejemplo registros de investigaciones o historias clínicas. Cada nivel se muestra con un color en la interfaz: verde para Público, amarillo para Reservado y rojo para Secreto. La etiqueta aparece junto al nombre del conjunto de datos en todas las pantallas donde se lo menciona, y no puede ocultarse. Los niveles son los mismos para todos los organismos y no se pueden renombrar ni ampliar con niveles intermedios. Si un organismo usa una escala propia, su administrador debe traducirla a estos tres niveles al cargar la información.

## Quién puede ver cada nivel de datos

El acceso depende del nivel del dato y del rol del usuario. Los datos Públicos los puede ver cualquier usuario del organismo, incluso con el rol Lector. Para ver datos Reservados se necesita rol Analista o superior, y además haber sido incorporado al espacio de trabajo donde se encuentran.

Los datos Secretos exigen un permiso explícito por cada conjunto de datos. El Administrador del organismo debe abrir el conjunto, entrar en la pestaña Acceso secreto y agregar uno por uno a los usuarios autorizados, que deben tener rol Analista o superior. Cada vez que alguien abre un dato Secreto, la plataforma pide de nuevo el código del doble factor, aunque la sesión ya esté iniciada. El rol Auditor nunca ve contenido de los datos, sea cual sea el nivel; solo ve el registro de quién accedió. Si un usuario carece del nivel necesario, el conjunto de datos no aparece en sus listados, de modo que ni siquiera puede saber que existe.

## Reclasificar un conjunto de datos

El Administrador del organismo puede cambiar la clasificación de un conjunto de datos desde la Consola de administración, en Datos, abriendo el conjunto y eligiendo la opción Cambiar clasificación. La plataforma pide en todos los casos un motivo escrito de al menos 20 caracteres, que queda guardado en la auditoría.

Subir el nivel, por ejemplo de Reservado a Secreto, se aplica de inmediato. Bajar el nivel requiere la aprobación de un segundo Administrador del organismo, que recibe un aviso y dispone de cinco días hábiles para aprobar o rechazar la solicitud con su código del doble factor. Si nadie responde en ese plazo, el pedido caduca y el conjunto mantiene su clasificación anterior. Mientras la solicitud está pendiente, el conjunto de datos conserva su nivel actual y se muestra con una marca de Cambio en revisión. Cuando la reclasificación se aprueba, los tableros que usan ese conjunto actualizan sus propias etiquetas en un máximo de diez minutos.

## Cómo heredan la clasificación los tableros

Un tablero no tiene una clasificación propia que alguien elija: hereda siempre la del dato más sensible que utiliza. Si un tablero combina tres fuentes, una Pública y dos Reservadas, el tablero completo se considera Reservado. Si se agrega una cuarta fuente Secreta, el tablero pasa a Secreto en el momento de guardar los cambios.

La plataforma muestra esa clasificación con una franja de color en la parte superior de cada tablero y en las exportaciones. Los usuarios que no tienen permiso para el nivel resultante dejan de ver el tablero en sus listados, aunque se lo hayan compartido antes. El editor recibe una advertencia antes de guardar si el cambio sube el nivel del tablero, con la lista de las personas que perderían acceso. De esta manera se evitan filtraciones accidentales por mezclar datos. No es posible rebajar de forma manual la etiqueta de un tablero: para lograrlo hay que quitarle la fuente más sensible o reclasificarla.

## Restricciones adicionales del nivel Secreto

Además del permiso individual, los datos Secretos tienen controles propios. Solo pueden consultarse desde las redes del organismo que su administrador haya registrado en la Consola de administración, bajo el menú Redes autorizadas. Un intento desde otra red es rechazado y queda anotado en la auditoría como acceso denegado.

Los tableros Secretos muestran sobre toda la pantalla una marca de agua con el nombre del usuario, su correo y la fecha y hora de la consulta. La marca no se puede desactivar y aparece también si se captura la pantalla. Las sesiones con datos Secretos se cierran a los 10 minutos de inactividad, la mitad del tiempo general, y no se permite abrir más de una sesión simultánea del mismo usuario. La plataforma también oculta, en estas consultas, el botón de copiar al portapapeles. Estos controles forman un paquete fijo: no pueden activarse de a uno ni desactivarse parcialmente, ni siquiera por pedido del Administrador del organismo.

## Detección automática de datos personales

Al cargar una fuente nueva, la plataforma examina los campos para detectar datos personales. Reconoce documentos de identidad, números de identificación tributaria, teléfonos, correos electrónicos y direcciones postales, tanto por el nombre de la columna como por el formato de los valores.

Los campos detectados reciben automáticamente la marca Dato personal y elevan el conjunto a Reservado como mínimo. El Administrador del organismo recibe un correo con la lista de campos marcados y dispone de cinco días hábiles para revisarla desde Datos, pestaña Sugerencias de clasificación. Puede confirmar cada sugerencia o descartarla indicando el motivo. La detección no es infalible y no reemplaza la revisión humana: los campos con nombres poco habituales o con datos mezclados en texto libre pueden pasar sin marcar. Por eso conviene revisar la lista de columnas de cada fuente nueva antes de compartirla con otros usuarios. Las marcas de dato personal no pueden eliminarse sobre campos que la detección sigue reconociendo.

## Clasificación inicial de las fuentes nuevas

Toda fuente que se conecta o se carga por primera vez comienza con la clasificación Reservado, sin importar su contenido. El criterio es prudente: es más sencillo abrir un dato que había quedado protegido que reparar la difusión indebida de uno que se expuso por error.

Mientras el administrador no revise la fuente, solo pueden verla los usuarios con rol Analista o superior que estén en el espacio de trabajo donde se cargó. Para ajustar el nivel, el administrador debe seguir el procedimiento de reclasificación. En el caso particular de la clasificación inicial, la primera modificación de una fuente nueva se considera una confirmación y no exige aprobación de un segundo administrador, siempre que ocurra dentro de los 30 días siguientes a la carga. Pasado ese plazo, rigen las reglas generales. Las cargas posteriores sobre la misma fuente conservan el nivel que ya tenía, aun cuando traigan campos nuevos, que se evalúan con la detección automática antes de incorporarse.

## Correspondencia entre niveles de habilitación del personal y clasificación de datos

El personal de Atalaya Data que trabaja con datos de los organismos clientes, como los equipos de soporte y los consultores, cuenta con una habilitación de seguridad de nivel 1, 2 o 3. Cada nivel se corresponde con una clasificación de datos de la plataforma: el nivel 1 con Público, el nivel 2 con Reservado y el nivel 3 con Secreto. Cada nivel incluye los anteriores, de modo que una persona de nivel 2 puede tratar datos Públicos y Reservados, y una de nivel 3 puede tratar los tres tipos.

La consecuencia práctica es que una persona con habilitación de nivel 1 no puede ver datos Reservados. Como los datos personales se clasifican como Reservados como mínimo, toda tarea que implique ver datos personales de la población exige nivel 2. Los datos Secretos exigen nivel 3, además del permiso explícito que otorga el Administrador del organismo. Esta correspondencia rige para las personas de Atalaya Data; para los usuarios de los organismos, el acceso a cada clasificación depende de su rol y de los permisos que les asigne su propio administrador. La habilitación misma la tramita el área de Recursos Humanos junto con Seguridad de la Información.
