# Tecnología — Roles y permisos
Versión 1.0 — octubre 2026

Este bloque describe qué puede hacer cada persona dentro de la plataforma y quién decide esos permisos. Reúne también los procedimientos para modificar o retirar accesos en los organismos clientes.

## Roles disponibles en la plataforma

La plataforma ofrece cinco roles predefinidos, que no pueden modificarse ni combinarse. El rol Lector permite ver tableros que le hayan compartido, sin editar nada. El rol Analista puede consultar fuentes de datos y construir consultas propias, pero no publicar tableros para otros. El rol Editor de tableros crea, modifica y comparte tableros dentro de su espacio de trabajo.

El rol Administrador del organismo gestiona usuarios, roles, fuentes y clasificaciones de datos de su propio organismo. Por último, el rol Auditor tiene acceso de solo lectura al registro de auditoría y a nada más, de modo que no puede ver los datos de negocio. Cada usuario tiene un único rol por espacio de trabajo. Si una persona necesita funciones de dos roles, por ejemplo analizar datos y administrar, se le asignan dos usuarios distintos con correos diferentes, algo que la plataforma permite sin costo técnico adicional. Los nombres de los roles aparecen en la ficha de cada usuario, dentro de la Consola de administración.

## Quién puede asignar y cambiar roles

Solamente el Administrador del organismo puede asignar o modificar roles, y únicamente sobre los usuarios de su propio organismo. El personal de Atalaya Data no cambia roles por pedido telefónico ni por correo, salvo en el caso excepcional de que el organismo haya perdido a todos sus administradores.

Cada organismo debe tener al menos dos Administradores y como máximo cinco. El mínimo existe para que siempre haya una persona que pueda atender un bloqueo o una baja, y el máximo limita la cantidad de personas con poder sobre los accesos. Un Administrador no puede quitarse a sí mismo el rol si es el último que queda. Para designar a un nuevo administrador, otro administrador existente debe asignar el rol desde la ficha del usuario, y el cambio exige confirmar con un código del doble factor. Si el organismo se queda sin administradores, un representante legal debe enviar a la Mesa de Ayuda la nota firmada de Designación de administrador, que Atalaya Data verifica en un plazo de tres días hábiles.

## Cambiar el rol de un usuario existente

Para modificar el rol de un usuario, el Administrador del organismo abre la Consola de administración, entra en Usuarios, selecciona la ficha de la persona y elige el nuevo rol en el campo Rol. El cambio se guarda al confirmar con el código del doble factor y queda registrado en la auditoría con el nombre de quien lo hizo.

Los permisos nuevos se aplican de inmediato en los próximos pedidos del usuario, pero las sesiones ya abiertas pueden tardar hasta 15 minutos en reflejarlos. Si el cambio es una reducción de permisos, por ejemplo de Editor de tableros a Lector, el usuario conserva la propiedad de los tableros que creó, aunque pasa a verlos en modo de solo lectura. El administrador puede traspasarlos a otra persona con el procedimiento de transferencia de tableros. Cuando se eleva el rol a Administrador del organismo, la plataforma envía además un aviso a los demás administradores del organismo, para que todos conozcan el cambio y puedan objetarlo si no lo esperaban.

## Revocar el acceso de un usuario que dejó el organismo

Cuando una persona deja el organismo, su acceso debe retirarse el mismo día. El Administrador del organismo lo hace desde la Consola de administración, en Usuarios, abriendo la ficha y pulsando Desactivar usuario. La plataforma cierra todas las sesiones de esa persona en un máximo de cinco minutos y le impide volver a ingresar. La cuenta no se elimina: queda en estado Inactivo para conservar el historial de auditoría.

Si el organismo no tiene un administrador disponible, puede completar el formulario Baja de usuario, en la sección Soporte del Portal de Clientes. Debe incluir el correo del usuario, la fecha de salida y el nombre de quien autoriza la baja, que tiene que figurar como contacto autorizado del organismo. Atalaya Data ejecuta la baja dentro de las dos horas posteriores a la recepción del formulario. Una cuenta inactiva puede reactivarse si la persona regresa al organismo, siempre que el administrador lo apruebe con un código del doble factor. La baja nunca borra los tableros del usuario, porque quedan sin propietario hasta que el administrador los transfiere a otra persona.

## Transferir los tableros de un usuario dado de baja

Al desactivar un usuario, sus tableros no se eliminan ni se vuelven inaccesibles. La plataforma los marca con la etiqueta Sin propietario y los mantiene disponibles para las personas con quienes estaban compartidos, que siguen viéndolos con sus permisos actuales. Nadie, sin embargo, puede editarlos hasta que se les asigne un nuevo dueño.

La transferencia la realiza el Administrador del organismo desde la Consola de administración, en el menú Contenido, opción Tableros sin propietario. Allí selecciona uno o varios tableros, elige el nuevo propietario, que debe tener rol Editor de tableros o superior, y confirma. Los tableros conservan su historial de versiones, sus enlaces de lectura y las programaciones de envío que tuvieran configuradas. Si pasan 60 días sin que se asigne un nuevo propietario, la plataforma traspasa automáticamente los tableros al Administrador del organismo que hizo la baja, y le avisa por correo con la lista completa de lo transferido. Este plazo no puede ampliarse ni reducirse.

## Permisos por espacio de trabajo

Cada organismo organiza su trabajo en espacios de trabajo, por ejemplo uno por dirección o por programa. Los permisos de un usuario no son globales: se definen por espacio. Una persona puede ser Editor de tableros en el espacio de Estadística y Lector en el de Presupuesto, y no ve nada en los espacios donde no fue incorporada.

Los espacios los crea el Administrador del organismo desde la Consola de administración, en el menú Espacios. Un organismo puede tener hasta 30 espacios activos. Para incorporar a un usuario, el administrador abre el espacio, elige la pestaña Miembros y pulsa Agregar miembro, indicando el rol correspondiente. Un espacio puede archivarse cuando ya no se usa: queda en solo lectura durante 90 días y luego desaparece del listado, aunque sus tableros pueden restaurarse a pedido del administrador dentro de ese período. Los espacios no pueden fusionarse entre sí. Cuando se necesita reunir contenidos de dos espacios, la solución es mover los tableros uno por uno al espacio de destino.

## Revisión trimestral de usuarios activos

Para evitar cuentas olvidadas, la plataforma genera cada trimestre un Informe de usuarios activos. Se envía por correo a los Administradores del organismo el primer día hábil de enero, abril, julio y octubre. El informe lista a todos los usuarios con su rol, su último ingreso y sus espacios de trabajo.

Los administradores deben revisar el listado y confirmar que cada persona sigue necesitando su acceso, usando el botón Confirmar revisión del propio informe. Si pasan 15 días sin confirmación, la plataforma envía un recordatorio. Además, toda cuenta que lleve 90 días sin ingresar se desactiva automáticamente, sin importar su rol, y aparece en el informe siguiente marcada como Inactiva por falta de uso. Para reactivarla basta con que el administrador pulse Reactivar en la ficha del usuario. La revisión queda registrada en la auditoría con la fecha y el nombre de quien la confirmó, lo que permite demostrar el control de accesos ante los organismos de control del Estado.

## Orden jerárquico de los roles de la plataforma

Los cuatro roles que trabajan con los datos de un organismo forman una escala jerárquica. De menor a mayor, el orden es: Lector, Analista, Editor de tableros y Administrador del organismo. Cada rol incluye lo que puede hacer el anterior: el Analista consulta fuentes y construye consultas además de ver tableros, el Editor de tableros también crea, modifica y comparte tableros, y el Administrador del organismo suma la gestión de usuarios, roles, fuentes y clasificaciones de datos.

Cuando un procedimiento de la plataforma exige un rol "o superior", se refiere a esta escala. Por ejemplo, "Analista o superior" incluye al Analista, al Editor de tableros y al Administrador del organismo, pero no al Lector; y "Editor de tableros o superior" incluye al Editor de tableros y al Administrador del organismo. El rol Auditor no forma parte de la escala: solo lee el registro de auditoría, no ve datos de negocio y por eso nunca cuenta como un rol superior a otro ni sirve para cumplir un requisito de rol mínimo. Cada usuario tiene un único rol por espacio de trabajo.
