# Tecnología — Despliegue y mantenimiento
Versión 1.0 — octubre 2026

Este bloque informa cómo se ofrece la plataforma a los organismos y cómo se planifican las tareas de mantenimiento. Las reglas de aviso y de horarios son las mismas para todos los clientes.

## Modalidades de despliegue disponibles

Atalaya Data ofrece dos modalidades de despliegue. En la modalidad Nube, la plataforma funciona en la infraestructura de Atalaya Data y el organismo solo la usa a través del navegador. En la modalidad Servidores del organismo, el software se instala en la infraestructura propia del cliente y lo opera su equipo de sistemas, con acompañamiento técnico de Atalaya Data.

La modalidad Nube se actualiza sin intervención del cliente y es la que eligen la mayoría de los organismos. La modalidad Servidores del organismo suele elegirse cuando una norma exige que los datos permanezcan dentro de las instalaciones. En ambas modalidades el producto y las funciones son los mismos, aunque los plazos de actualización cambian. El organismo define su modalidad al contratar y puede cambiarla una vez, mediante un pedido formal a su ejecutivo de cuenta. La migración de una modalidad a otra se planifica en un cronograma acordado, que lleva en general entre cuatro y seis semanas. Durante ese lapso, la modalidad anterior sigue funcionando con normalidad.

## Ventanas de mantenimiento programado

El mantenimiento rutinario de la modalidad Nube se concentra en una ventana fija: el primer domingo de cada mes, entre las 01:00 y las 05:00 hora del organismo. En ese tramo la plataforma puede interrumpirse por completo o de forma parcial, y las cargas programadas que caigan dentro de la ventana se reprograman automáticamente al finalizar.

Las ventanas se anuncian en un calendario público dentro de la página de estado del servicio. Si una tarea requiere más de cuatro horas, se divide en dos ventanas consecutivas en lugar de ampliar la primera. Durante la ventana, la pantalla de ingreso muestra un cartel de mantenimiento con la hora estimada de regreso. Los usuarios que estén trabajando reciben un aviso 15 minutos antes del inicio, y las sesiones abiertas se cierran de forma ordenada. Los cambios que el usuario no haya guardado en ese momento pueden perderse, por lo que conviene guardar el trabajo al ver el primer aviso. Las ventanas no se postergan a pedido de un organismo en particular.

## Avisos de actualizaciones de la plataforma

Cada vez que Atalaya Data publica una versión con cambios visibles para los usuarios, avisa a los organismos con 10 días hábiles de anticipación. El aviso llega por correo a los Administradores del organismo y se muestra además como banner dentro de la plataforma durante los cinco días previos.

El correo incluye las notas de la versión, con una lista de las funciones nuevas, los cambios de comportamiento y los problemas corregidos. Cuando una actualización modifica algo que los usuarios hacen a diario, como la forma de exportar o el aspecto de los tableros, se agrega una guía breve de cambios en la primera pantalla posterior al ingreso. Las correcciones menores que no alteran el uso se publican sin aviso previo y se listan después en el historial de versiones de la página de estado. Las versiones principales se publican cada trimestre, en los meses de febrero, mayo, agosto y noviembre, y las versiones menores pueden salir en cualquier semana del año. Los administradores que no deseen recibir los avisos pueden consultar el historial directamente en la página de estado.

## Mantenimiento de emergencia

Cuando se detecta una vulnerabilidad o una falla grave que no puede esperar a la ventana mensual, Atalaya Data realiza un mantenimiento de emergencia. Siempre que sea posible, avisa con al menos dos horas de anticipación por correo a los Administradores del organismo y mediante un aviso en la página de estado.

Si el riesgo es inmediato y no hay margen para avisar, la intervención se hace de inmediato y la comunicación llega después, dentro de la hora siguiente a su finalización. Estas intervenciones suelen durar menos de 30 minutos y no requieren ninguna acción del organismo. Al terminar, se publica en la página de estado un resumen con la hora de inicio y de fin, y la causa a grandes rasgos. Si el mantenimiento de emergencia causó una pérdida de servicio de más de una hora, el organismo recibe además una explicación escrita dentro de los cinco días hábiles posteriores. Los mantenimientos de emergencia no cuentan como las ventanas programadas del mes, y por eso pueden sumarse a ellas sin que haya límite de cantidad al año.

## Actualizar una instalación en servidores del organismo

En la modalidad Servidores del organismo, las actualizaciones no se aplican solas. Atalaya Data publica cada trimestre un paquete de versión en el portal de descargas, accesible con las credenciales del contacto técnico del organismo, junto con la guía de instalación paso a paso.

El organismo dispone de 60 días corridos desde la publicación para actualizar. La plataforma admite como máximo una versión de atraso respecto de la última publicada: una instalación dos versiones atrás deja de recibir correcciones y se considera fuera de soporte. Los paquetes de seguridad críticos tienen un plazo más corto, de 15 días. Antes de instalar, el equipo técnico debe ejecutar el verificador de requisitos incluido en el paquete, que revisa la versión del sistema operativo, el espacio libre y la conectividad. Si la instalación falla, el verificador genera un informe que puede adjuntarse a un ticket de la Mesa de Ayuda. Atalaya Data no entra por sí misma en los servidores del cliente, salvo que un contacto autorizado habilite una sesión remota de 4 horas como máximo.

## Requisitos mínimos del servidor

Para instalar la plataforma en los servidores del organismo, cada nodo debe cumplir requisitos mínimos de equipamiento. Se exige un sistema operativo Linux de 64 bits con soporte vigente del fabricante, 16 núcleos de procesador, 64 GB de memoria y 1 TB de almacenamiento en discos de estado sólido.

Una instalación de producción necesita al menos tres nodos, para que el servicio continúe aunque uno falle. Se recomienda sumar un cuarto nodo si el organismo prevé más de 500 usuarios activos al mismo tiempo. La red entre nodos debe ser de al menos 10 gigabits y con latencia menor a un milisegundo. Los servidores deben tener sincronización horaria con un servidor de tiempo confiable, porque la plataforma rechaza conexiones cuando la diferencia de hora supera los dos minutos. Además se necesita salida a internet hacia los servidores de licencias de Atalaya Data, por el puerto 443. Los equipos de pruebas pueden tener la mitad de recursos, siempre que no se usen con datos reales.
