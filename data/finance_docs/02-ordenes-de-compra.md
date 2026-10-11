# Finanzas — Órdenes de compra
Versión 1.0 — octubre 2026

Este bloque describe cómo debe emitirse y enviarse la orden de compra con la que un organismo formaliza su pedido a Atalaya Data. Reúne las reglas de contenido, de envío y de corrección que aplica el área de Administración de Ventas.

## Datos obligatorios de la orden de compra

Toda orden de compra debe incluir ocho datos para ser aceptada: razón social y número de identificación fiscal del organismo, número de expediente o de contrato, descripción del servicio contratado, cantidad de licencias, precio unitario y total sin impuestos, período de servicio cubierto, domicilio fiscal de facturación y firma de la autoridad que autoriza el gasto.

El número de expediente es el dato que con mayor frecuencia falta. Sin él, Atalaya Data no puede vincular la orden con el contrato y la rechaza automáticamente. La descripción del servicio debe coincidir con la que figura en la cotización aceptada; si el texto difiere, el equipo de Administración de Ventas solicita una aclaración antes de procesar el pedido.

El organismo puede usar su propio modelo de orden de compra o el formulario OC-01 que Atalaya Data publica en el Portal de Clientes. Ambos son válidos mientras contengan los ocho datos indicados y estén firmados por una persona con facultades para comprometer fondos.

## Destinatario y canal de envío

La orden de compra se envía a la casilla ordenes@atalayadata.example, en formato PDF y con la firma de la autoridad visible. Cada correo debe contener una sola orden; si el organismo emite varias, las envía en mensajes separados para evitar confusiones en el registro.

El asunto del mensaje debe indicar el número de orden y el nombre del organismo, por ejemplo "OC 2026-0417 — Ministerio de Planificación". Este formato permite que el sistema de Administración de Ventas clasifique el pedido en forma automática y lo asigne a un analista el mismo día.

Atalaya Data no recibe órdenes de compra por mensajería instantánea, por teléfono ni a través de la sección Soporte del Portal de Clientes. Las órdenes enviadas por esos medios no se consideran presentadas y el organismo debe reenviarlas a la casilla indicada. Quienes necesiten entregar la orden en papel pueden hacerlo en la mesa de entradas de la sede central, de lunes a viernes de 9 a 16 horas.

## Confirmación de recepción de la orden

Dentro de las 24 horas hábiles posteriores a recibir una orden de compra, Atalaya Data envía una confirmación de recepción al correo desde el cual se presentó. La confirmación incluye un número de registro interno con el formato AD-OC seguido de seis dígitos, que sirve para consultar el estado del pedido.

Si el organismo no recibe esa confirmación en 2 días hábiles, debe escribir a ordenes@atalayadata.example citando el asunto original del mensaje. Es posible que el correo haya sido filtrado o que la orden tenga un archivo adjunto dañado.

La confirmación de recepción no implica aceptación definitiva. Es solo la constancia de que la orden ingresó al circuito de revisión. La aceptación se comunica por separado, una vez que el analista verificó que los datos obligatorios están completos y que el monto coincide con la cotización vigente. Conviene conservar el número de registro, porque el área de Administración de Ventas lo solicita en cualquier consulta posterior sobre la orden.

## Qué ocurre si la orden de compra tiene errores

Cuando una orden presenta errores u omisiones, el analista de Administración de Ventas la devuelve al organismo con una nota que detalla cada observación. La devolución se realiza dentro de los 3 días hábiles posteriores a la recepción, y la orden queda en estado "observada" hasta que se corrija.

El organismo puede subsanar los errores reenviando una orden corregida, no una hoja complementaria. Debe conservar el mismo número de orden y agregar al asunto la palabra "corregida". Una orden observada que no recibe respuesta en 30 días corridos se archiva, y el organismo debe presentar una nueva si todavía desea contratar.

Mientras la orden esté observada, Atalaya Data no emite factura ni da de baja el pedido. El servicio comprometido en el contrato continúa su curso normal, pero la facturación correspondiente se difiere hasta que la orden quede aceptada. Por eso se recomienda revisar la orden contra el formulario OC-01 antes de enviarla.

## Modificación de una orden de compra vigente

Una orden aceptada puede modificarse para ampliar la cantidad de licencias o extender el período de servicio. Para ello, el organismo emite una orden complementaria que haga referencia expresa al número de registro de la orden original, e indique solo la diferencia que se agrega.

Las modificaciones no pueden reducir el monto de una orden ya aceptada. Si el organismo necesita disminuir el alcance, debe pedir la cancelación parcial de la orden, que alcanza solo a los meses todavía no prestados. Esta separación evita que los ajustes hacia abajo se mezclen con los pedidos nuevos.

El analista procesa las órdenes complementarias en un plazo de 4 días hábiles. Cuando la ampliación supera el 20 % del valor de la orden original, interviene además el responsable de cuentas, que confirma por escrito al organismo las nuevas condiciones antes de aceptar el pedido. El organismo recibe una confirmación escrita con el nuevo total vigente, que debe archivar junto con la orden original.

## Cancelación total o parcial de una orden

El organismo puede cancelar una orden de compra mientras el período de servicio correspondiente no haya comenzado. La solicitud se presenta por escrito a ordenes@atalayadata.example, firmada por la misma autoridad que emitió la orden, y debe indicar el número de registro AD-OC y el motivo de la cancelación.

Si el servicio ya comenzó, solo se admite la cancelación parcial de los meses que todavía no se prestaron. Los meses transcurridos se facturan en su totalidad, aunque el organismo no haya utilizado la plataforma durante ese tiempo. Atalaya Data confirma la cancelación por escrito en un máximo de 5 días hábiles, y conserva la solicitud en el registro de la orden como respaldo para ajustar la facturación de los períodos que ya no se prestarán.

Las cancelaciones aceptadas generan una nota interna que se envía al área de facturación para evitar emitir comprobantes por períodos anulados. Si ya se había emitido una factura que luego se cancela, Atalaya Data emite la nota de crédito correspondiente.

## Vigencia de la orden de compra

Cada orden de compra tiene una vigencia que coincide con el período de servicio indicado en ella. Cuando ese período termina, la orden se da por cumplida y deja de ser el respaldo para nuevas facturas. Atalaya Data no factura períodos posteriores utilizando una orden vencida.

Para continuar con el servicio, el organismo debe emitir una nueva orden al menos 30 días corridos antes del vencimiento de la anterior. Si la nueva orden llega más tarde, el servicio no se interrumpe de inmediato: existe un período de gracia de 15 días corridos durante el cual la plataforma sigue operativa mientras se regulariza el trámite.

Pasado ese período de gracia sin una orden vigente, el área de Administración de Ventas notifica al responsable administrativo del contrato y se suspende la emisión de facturas. La reactivación se produce cuando el organismo presenta la nueva orden y esta es aceptada, sin cargos adicionales ni penalidades.
