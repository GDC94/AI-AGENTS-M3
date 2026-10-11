# Tecnología — Seguridad interna
Versión 1.0 — octubre 2026

Este bloque reúne las normas de seguridad informática que deben cumplir los empleados y consultores de Atalaya Data en su trabajo diario. Se aplica a todos los equipos y cuentas corporativas, estén o no dentro de las oficinas.

## Conectarse a la VPN corporativa

Para acceder a los sistemas internos desde fuera de las oficinas hay que usar la VPN corporativa. El programa se llama AtalayaConnect y viene instalado en todas las notebooks de la empresa. Al abrirlo, la persona ingresa su usuario corporativo y su contraseña, y luego confirma con un código del doble factor de la aplicación autenticadora.

Una sesión de VPN dura como máximo 12 horas, después de las cuales hay que volver a autenticarse. También se corta tras 30 minutos sin tráfico. La VPN debe estar activa siempre que se trabaje con datos de clientes desde una red que no sea la de las oficinas, incluidos hogares, hoteles y espacios de trabajo compartidos. Mientras está conectada, el tráfico hacia internet pasa por los filtros de seguridad de la empresa, por lo que algunos sitios pueden estar bloqueados. Cada usuario puede tener dos dispositivos registrados en la VPN al mismo tiempo, y no es posible conectar el mismo usuario desde dos equipos a la vez. Un tercer dispositivo se registra solo después de dar de baja uno de los anteriores.

## Qué hacer si la VPN no conecta

El problema más frecuente en notebooks nuevas es el error V-12, que significa que el certificado de dispositivo todavía no está instalado. Para resolverlo hay que abrir AtalayaConnect, ir al menú Ayuda y pulsar Reparar conexión. El programa descarga el certificado y vuelve a probar la conexión, en un proceso que lleva unos dos minutos.

El error V-31 indica que la hora del equipo está desfasada más de cinco minutos respecto del servidor, y se corrige activando la sincronización automática de fecha y hora del sistema operativo. Con V-40, el programa informa que la contraseña venció o que la cuenta está bloqueada, y hay que cambiarla desde el portal de identidad corporativo. Si después de aplicar estas soluciones la VPN sigue sin conectar, hay que abrir un ticket de severidad S3 en la Mesa de Ayuda TI, porque es una falla parcial con alternativa razonable: trabajar desde las oficinas, adjuntando el archivo de registro que genera el botón Exportar diagnóstico del programa. El registro contiene el código de error y la hora de cada intento, lo que ahorra preguntas y acelera la resolución. Reinstalar el programa por cuenta propia no resuelve estos errores.

## Reconocer y reportar correos de phishing

Un correo sospechoso suele pedir datos urgentes, contener enlaces a direcciones que no pertenecen a la empresa o llegar con adjuntos inesperados. Si una persona recibe un mensaje así, no debe abrir los enlaces ni descargar los archivos adjuntos, ni responder al remitente.

Debe usar el botón Reportar phishing, que aparece en la barra del cliente de correo corporativo. El botón envía el mensaje al equipo de seguridad y lo retira de la bandeja. El equipo responde dentro de la hora hábil siguiente, indicando si se trataba de una amenaza real o de un mensaje legítimo. Si la persona ya hizo clic en un enlace o ingresó su contraseña, no basta con reportar el correo: debe seguir el procedimiento para incidentes de seguridad y cambiar su contraseña de inmediato. Una vez al trimestre, el equipo de seguridad envía correos de práctica falsos y registra quién los reporta. Los resultados no tienen consecuencias individuales, y sirven para detectar qué tipos de engaño necesitan más explicación en la empresa.

## Qué hacer ante un incidente de seguridad

Se considera incidente de seguridad la sospecha de que una cuenta fue usada por un tercero, que un equipo fue infectado o que se expuso información de un cliente, incluido haber accedido por error a datos que no correspondían. Ante cualquiera de estas situaciones, la persona debe llamar de inmediato al interno 5100, la guardia de Seguridad de la Información, disponible las 24 horas. Ese mismo interno recibe el aviso de pérdida o robo de la credencial de habilitación de seguridad.

La llamada debe hacerse dentro de los 15 minutos de advertir el problema. Mientras espera instrucciones, la persona debe desconectar el equipo de la red, quitando el cable o apagando el Wi-Fi, pero sin apagar la notebook, porque el análisis necesita la memoria encendida. No debe borrar archivos ni intentar limpiar el equipo por su cuenta. El equipo de seguridad abre un caso, guía el contenido de la investigación y decide si hay que avisar al organismo cliente afectado. Quien reporta de buena fe y a tiempo nunca recibe sanciones por el hecho de haber cometido el error inicial. Los incidentes confirmados se revisan en una reunión interna dentro de los cinco días hábiles posteriores a su cierre.

## Uso de dispositivos USB

Por defecto, los puertos USB de las notebooks corporativas solo permiten conectar teclados, ratones y auriculares. Los dispositivos de almacenamiento, como pendrives y discos externos, quedan bloqueados para impedir que salgan datos de clientes o ingresen programas maliciosos.

Quien necesite copiar archivos debe solicitar un pendrive cifrado corporativo mediante el formulario Solicitud de almacenamiento extraíble del Portal Interno, con la aprobación de su responsable directo. El equipo cifrado se entrega en tres días hábiles y su contenido solo puede abrirse desde equipos de la empresa. Cuando existe una necesidad puntual que no cubre ese dispositivo, se puede pedir una excepción de hasta 30 días, que la aprueba el equipo de seguridad. Pasado ese plazo, el bloqueo se reactiva solo. Queda terminantemente prohibido conectar a la notebook de trabajo dispositivos personales encontrados o regalados por terceros, como cargadores o pendrives de promoción, porque pueden contener programas ocultos. Cualquier dispositivo de este tipo debe entregarse al equipo de seguridad, que lo revisa en un entorno aislado.

## Contraseñas de las cuentas corporativas del personal

Las cuentas corporativas del personal de Atalaya Data siguen una política más exigente que la de los usuarios de los organismos. La contraseña debe tener al menos 14 caracteres y cambiarse cada 180 días, y no puede repetir ninguna de las últimas diez usadas. Se recomienda una frase larga antes que una palabra con símbolos.

Todas las personas tienen asignado el gestor de contraseñas corporativo, que se activa en el navegador desde el Portal Interno, en la sección Seguridad. El gestor genera claves únicas para cada sistema y las completa automáticamente, por lo que no hace falta memorizarlas. Está prohibido guardar contraseñas en hojas de cálculo, notas del teléfono o papeles visibles en el puesto de trabajo. Tampoco se permite compartir una cuenta entre dos personas, ni siquiera por un corto período. La contraseña maestra del gestor es la única que debe recordarse, y si se olvida no hay manera de recuperarla: el personal de seguridad solo puede restablecer la cuenta, lo que borra las claves guardadas. Cada persona puede revisar desde el gestor cuáles de sus claves son débiles o repetidas.

## Baja de cuentas del personal que deja Atalaya

Cuando un empleado o consultor deja Atalaya Data, sus accesos se retiran el último día de trabajo. Recursos Humanos informa la fecha de salida a Tecnología con anticipación y, al cierre de esa jornada, se desactiva la cuenta corporativa, lo que impide iniciar sesión en cualquier sistema interno. En una salida inmediata, la desactivación se hace en el momento en que se comunica la decisión.

En el mismo acto se da de baja el acceso a la VPN: se revocan los certificados de los dispositivos registrados y se cierra cualquier sesión abierta. El correo corporativo deja de recibir y enviar mensajes desde esa cuenta; se activa una respuesta automática que indica el nuevo contacto y el buzón se conserva archivado durante 90 días a disposición de la jefatura antes de eliminarse. Los accesos de la persona a las cuentas de los organismos clientes los retira el Administrador de cada organismo. La devolución de la notebook y de los demás equipos la gestionan Recursos Humanos y Tecnología.
