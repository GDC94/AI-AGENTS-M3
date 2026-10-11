# Tecnología — Acceso a la plataforma
Versión 1.0 — octubre 2026

Este bloque explica cómo las personas de los organismos clientes obtienen y mantienen su acceso a la plataforma de Atalaya Data. Está pensado para usuarios finales y para los administradores de cada organismo.

## Dar de alta usuarios nuevos en la plataforma

Solo el Administrador del organismo puede crear usuarios. Debe ingresar a la Consola de administración, abrir el menú Usuarios y elegir la opción Alta de usuario. Cada alta pide nombre completo, correo institucional, rol inicial y espacio de trabajo. El correo debe pertenecer al dominio oficial del organismo, porque la plataforma rechaza direcciones de dominios personales.

Cuando hay que crear varias cuentas a la vez, conviene usar la opción Alta masiva del mismo menú. Esta función recibe un archivo CSV con las columnas nombre, correo, rol y espacio, y admite hasta 200 filas por carga. Antes de crear las cuentas, la plataforma muestra una vista previa con los errores detectados, por ejemplo correos repetidos o roles inexistentes, y el administrador puede corregirlos y volver a subir el archivo. Al confirmar, cada persona recibe automáticamente un correo de bienvenida con las instrucciones para activar su cuenta. Si la carga supera las 200 filas, debe dividirse en varios archivos.

## Activar la cuenta en el primer ingreso

Después del alta, la persona recibe un correo con el asunto "Active su cuenta en Atalaya Data". El enlace de activación es personal y tiene una validez de 48 horas desde el envío. Al abrirlo, la plataforma pide definir una contraseña propia y aceptar las condiciones de uso del servicio. El proceso termina con la configuración obligatoria del doble factor de autenticación, que consiste en vincular una aplicación autenticadora instalada en el teléfono de la persona.

Si el enlace venció antes de usarse, el usuario no puede reactivarlo por su cuenta. En ese caso, el Administrador del organismo debe abrir la ficha del usuario en la Consola de administración y pulsar el botón Reenviar activación, que genera un enlace nuevo con otras 48 horas de validez. Mientras la cuenta no esté activada, aparece en la lista de usuarios con el estado Pendiente y no consume ninguna sesión ni puede acceder a datos. El correo de activación a veces es filtrado por los sistemas de seguridad del organismo, por lo que conviene revisar la carpeta de correo no deseado antes de pedir un reenvío.

## Recuperar una contraseña olvidada

Cualquier usuario puede recuperar su contraseña sin intervención de Atalaya Data. En la pantalla de ingreso debe elegir el enlace "Olvidé mi contraseña" e indicar su correo institucional. La plataforma envía un mensaje con un enlace de restablecimiento que caduca a los 30 minutos y que solo puede usarse una vez. Si el mensaje no llega en cinco minutos, hay que revisar la carpeta de correo no deseado y, si tampoco está allí, repetir el pedido una sola vez.

Al abrir el enlace, el sistema pide la nueva contraseña dos veces y luego solicita un código del doble factor para confirmar la identidad. Por seguridad, la recuperación nunca revela si el correo indicado existe en la plataforma: el mensaje en pantalla es siempre el mismo. Si el usuario perdió además el acceso a su aplicación autenticadora, la recuperación no alcanza y debe seguir el procedimiento de restablecimiento del doble factor. Todo cambio de contraseña genera un aviso al correo del usuario y cierra las sesiones que estuvieran abiertas en otros dispositivos.

## Requisitos de las contraseñas de la plataforma

Las contraseñas de los usuarios de los organismos deben tener al menos 12 caracteres e incluir mayúsculas, minúsculas, números y un símbolo. La plataforma rechaza contraseñas que figuren en una lista de claves frecuentes, que contengan el nombre del usuario o que coincidan con alguna de las últimas cinco contraseñas utilizadas en esa cuenta.

Cada contraseña vence a los 90 días. Desde el día 80, la pantalla de ingreso muestra un aviso para que el usuario la cambie con anticipación desde el menú Mi perfil, opción Seguridad. Si el plazo se cumple sin cambio, la plataforma obliga a definir una contraseña nueva en el siguiente ingreso, antes de dar acceso a cualquier tablero. Los administradores de cada organismo no pueden ver ni conocer las contraseñas de sus usuarios, ni tampoco el personal de Atalaya Data, porque se almacenan de forma irreversible. Tampoco es posible desactivar el vencimiento para cuentas individuales, ni siquiera para cuentas de administradores o de auditores.

## Configurar el doble factor de autenticación

El doble factor es obligatorio para todos los usuarios y se configura durante la activación de la cuenta. El usuario debe instalar en su teléfono una aplicación autenticadora que genere códigos de seis dígitos y escanear el código QR que muestra la plataforma en Mi perfil, opción Seguridad. Para terminar, ingresa el primer código generado y el sistema confirma el vínculo.

En ese momento la plataforma entrega ocho códigos de respaldo de un solo uso. Sirven para ingresar si el teléfono se pierde o se rompe, y conviene guardarlos en un lugar seguro y separado del dispositivo. Cada código funciona una única vez, y al agotarse el último hay que generar un juego nuevo desde la misma pantalla. Si el usuario se queda sin teléfono y sin códigos, solo el Administrador del organismo puede restablecer el doble factor desde la ficha del usuario, con la acción Restablecer segundo factor. Tras ese restablecimiento, la persona deberá repetir la configuración completa en su siguiente ingreso. La plataforma no admite mensajes de texto como método de reemplazo.

## Desbloquear una cuenta tras intentos fallidos

La plataforma bloquea una cuenta después de cinco intentos fallidos consecutivos de contraseña o de código del doble factor. El bloqueo dura 30 minutos y se levanta solo cuando ese tiempo termina. Durante la espera, la pantalla de ingreso informa que la cuenta está bloqueada, sin indicar cuántos minutos faltan, para no dar pistas a quien intente adivinar claves.

Si el usuario no puede esperar, el Administrador del organismo puede desbloquearlo de inmediato desde la Consola de administración, ingresando a la ficha del usuario y pulsando Desbloquear cuenta. Cuando el usuario no cuenta con un administrador disponible, puede pedir el desbloqueo a la Mesa de Ayuda de Atalaya Data, que exige confirmar la identidad con el correo institucional y el nombre del Administrador del organismo. Si una cuenta se bloquea tres veces en un mismo día, la plataforma la suspende y envía una alerta al administrador, quien debe revisar el motivo antes de reactivarla. Un bloqueo repetido puede indicar que alguien más está intentando entrar con las credenciales del usuario.

## Cierre de sesión por 20 minutos de inactividad

Para proteger los datos en equipos compartidos o desatendidos, la plataforma cierra la sesión de cualquier usuario de un organismo que permanezca 20 minutos sin actividad. Dos minutos antes del cierre aparece un aviso en pantalla con una cuenta regresiva y un botón para continuar trabajando. Si el usuario no responde, la sesión termina y se pierden los cambios no guardados en los tableros que estuviera editando, por lo que conviene guardar el trabajo con frecuencia.

El tiempo de inactividad es igual para todos los organismos y no puede modificarse desde la Consola de administración, ni siquiera por pedido del Administrador del organismo. Cualquier acción del usuario dentro de la plataforma, como abrir un tablero, aplicar un filtro o escribir en un campo, reinicia la cuenta de los 20 minutos, mientras que dejar la pantalla quieta no la reinicia. Después de un cierre por inactividad, el usuario debe ingresar de nuevo con su contraseña y con el código del doble factor de autenticación.

## Duración máxima de 10 horas por sesión de la plataforma

Además del cierre por inactividad, la plataforma limita la duración total de cada sesión a un máximo absoluto de 10 horas. El tiempo se cuenta desde el momento del ingreso y el límite se aplica aunque el usuario esté trabajando sin pausa. Al alcanzarlo, la plataforma pide ingresar de nuevo con contraseña y doble factor de autenticación, y los cambios que no se hayan guardado en un tablero en edición pueden perderse, por lo que conviene guardar el trabajo antes.

Como ocurre con el cierre por inactividad, este límite es igual para todos los organismos y no puede modificarse desde la Consola de administración. Rige para todos los roles, incluidos los administradores y los auditores. Quien necesite seguir trabajando después del límite simplemente inicia una sesión nueva, sin esperar ningún tiempo y sin pedir autorización al Administrador del organismo. La sesión nueva empieza con un conteo propio de 10 horas y con su propio control de inactividad.

## Aviso por ingreso desde una red distinta y cierre manual de sesiones

La plataforma vigila desde dónde se inicia cada sesión. Cuando un usuario ingresa desde una red distinta a la habitual, la sesión se trata igual que cualquier otra, con los mismos límites de inactividad y de duración, pero la plataforma envía además un aviso por correo a la persona con la fecha, la hora y la ubicación aproximada del ingreso. Ese mensaje permite detectar un acceso que el usuario no reconoce. Si no fue él quien ingresó, debe cambiar de inmediato su contraseña y avisar al Administrador del organismo.

Cada usuario puede cerrar de forma manual todas sus sesiones activas desde el menú Mi perfil, opción Sesiones. Conviene hacerlo al terminar de trabajar en un equipo compartido o prestado, y también cuando se sospecha que alguien más tiene abierta la cuenta en otro dispositivo. El cierre manual afecta a todos los dispositivos a la vez y obliga a volver a ingresar con contraseña y doble factor en cada uno de ellos.