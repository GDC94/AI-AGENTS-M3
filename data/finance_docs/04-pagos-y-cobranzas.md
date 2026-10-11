# Finanzas — Pagos y cobranzas
Versión 1.0 — octubre 2026

Este bloque explica cómo, cuándo y por qué medios los organismos abonan a Atalaya Data, y cómo se actúa ante atrasos. Lo gestiona el área de Cobranzas, que acompaña a cada organismo hasta la cancelación de sus facturas.

## Plazo de pago de las facturas a organismos

El plazo de pago de cada factura depende del tipo de organismo. Para organismos nacionales y provinciales, vence a los 30 días corridos desde la fecha de emisión; para municipios, a los 45 días corridos. La diferencia responde a los circuitos de aprobación de gasto, más largos en las administraciones locales.

La fecha de vencimiento aparece en el encabezado de la factura y también en el Portal de Clientes, junto al estado del comprobante. Si el vencimiento cae en un día no hábil, se traslada al siguiente día hábil sin recargo alguno.

Atalaya Data no modifica el plazo a pedido una vez emitida la factura. Si el organismo sabe de antemano que su circuito excederá el plazo estándar, debe acordar un plazo distinto al firmar el contrato, ya que el plazo especial queda reflejado de manera automática en todas las facturas del período. El área de Cobranzas consulta el estado de pago de cada comprobante cada lunes.

## Medios de pago aceptados

Atalaya Data acepta tres medios de pago: transferencia bancaria a la cuenta recaudadora, depósito en ventanilla de la entidad receptora y orden de pago electrónica emitida por el sistema de tesorería del organismo. No se aceptan cheques ni pagos en efectivo, por la dificultad de conciliarlos con las facturas.

Los datos de la cuenta recaudadora figuran al pie de cada factura y en la sección "Pagos" del Portal de Clientes. Atalaya Data no modifica esos datos sin avisar por escrito al responsable administrativo con al menos 30 días corridos de anticipación; ante cualquier mensaje que indique una cuenta distinta, el organismo debe verificarlo llamando a Cobranzas antes de pagar.

La orden de pago electrónica debe identificar la factura mediante su número completo en el campo de referencia. Si un solo pago cancela varias facturas, el organismo debe enviar la lista de comprobantes incluidos para que la conciliación se realice sin demoras.

## Aviso de pago al área de Cobranzas

Una vez efectuado el pago, el organismo debe avisarlo a cobranzas@atalayadata.example adjuntando el comprobante de transferencia o la orden de pago. Este aviso acelera la imputación, aunque no es obligatorio: el sistema detecta los depósitos por sí mismo, pero puede tardar más en reconocerlos si la referencia está incompleta.

Con el aviso, Cobranzas imputa el pago en un máximo de 2 días hábiles y el estado de la factura cambia a "pagada" en el Portal de Clientes. Sin aviso, la imputación puede demorar hasta 6 días hábiles, tiempo durante el cual la factura seguirá apareciendo como pendiente.

El mensaje debe incluir el número de factura, la fecha de pago, el importe abonado y el nombre del banco emisor. Si el importe pagado difiere del facturado por retenciones aplicadas por el organismo, deben detallarse por separado en el mismo mensaje para que Cobranzas pueda registrarlas correctamente. Los avisos recibidos antes de las 14 horas se procesan el mismo día hábil; los posteriores se procesan al día siguiente.

## Intereses por mora

Cuando una factura no se paga en su fecha de vencimiento, comienza a devengar un interés por mora del 0,05 % diario sobre el saldo impago. El interés se calcula sobre días corridos y se acumula hasta la fecha de acreditación del pago, sin capitalizarse.

Los intereses no se incluyen en la factura original, sino en un comprobante separado que Atalaya Data emite al mes siguiente a la cancelación del capital. El organismo dispone de 30 días corridos para abonarlo, y ese comprobante no devenga a su vez nuevos intereses.

Si la demora se debe a un error de Atalaya Data, como una factura con datos incorrectos que debió reemplazarse, el área de Cobranzas anula el interés correspondiente a los días de demora imputables a la empresa. El organismo debe solicitarlo por escrito citando el número de la factura y la fecha en que informó el error. El Portal de Clientes muestra en todo momento el interés acumulado de cada factura vencida, actualizado al cierre del día anterior.

## Recordatorios y gestión de facturas vencidas

Cobranzas envía un primer recordatorio por correo 5 días hábiles después del vencimiento de una factura impaga. Si no hay respuesta, remite un segundo aviso a los 15 días hábiles, esta vez con copia al responsable administrativo del contrato y al área jurídica del organismo.

Superados los 30 días corridos de atraso, un ejecutivo de cuenta llama al organismo para entender el motivo de la demora y acordar una fecha de pago. Ese acuerdo queda por escrito y puede incluir un plan de cancelación en hasta tres vencimientos mensuales, con aprobación de la jefatura de Cobranzas.

Durante todo este proceso, el servicio sigue operativo. Atalaya Data no corta el acceso a la plataforma por una única factura vencida, porque reconoce los tiempos administrativos de los organismos. La suspensión solo se evalúa cuando se acumulan atrasos de más de 90 días corridos, y antes de hacerlo se envía una notificación formal al responsable administrativo. Cada contacto con el organismo queda registrado en el historial de la cuenta, al que el responsable administrativo puede pedir acceso.

## Suspensión del servicio por falta de pago

Cuando un organismo acumula facturas impagas con más de 90 días corridos de atraso, Atalaya Data puede suspender el servicio. Antes de hacerlo, envía una notificación formal al responsable administrativo, con copia a la autoridad que firmó el contrato, que concede 10 días hábiles para regularizar la situación.

La suspensión limita el acceso a la plataforma al modo de solo lectura: los usuarios pueden consultar tableros ya creados, pero no cargar datos nuevos ni exportar información. Los datos del organismo se conservan íntegros durante toda la suspensión.

El servicio se reactiva dentro de las 24 horas hábiles posteriores a la acreditación del pago total del capital adeudado. Los intereses pendientes no impiden la reactivación, aunque deben abonarse en el plazo indicado en su comprobante. Una suspensión no interrumpe la facturación: los períodos suspendidos se facturan igual, porque el contrato sigue vigente. El organismo puede pedir por escrito una prórroga de la suspensión, que la gerencia de Cobranzas resuelve en 3 días hábiles.

## Recibo oficial de pago

Una vez que el organismo cancela una factura, puede descargar el recibo oficial de pago desde la sección "Comprobantes" del Portal de Clientes, dentro de Facturación. El recibo se genera de manera automática dentro de las 24 horas posteriores a la imputación del pago y lleva un número único, que conviene conservar para cualquier consulta posterior.

El recibo identifica la factura cancelada, la fecha de imputación y el importe abonado, y funciona como respaldo del pago en el expediente del organismo. Atalaya Data lo entrega en PDF firmado digitalmente. Mientras el pago no esté imputado, la factura figura como pendiente y el recibo no se genera, de modo que avisar el pago a Cobranzas acelera la disponibilidad del documento. El organismo puede incorporarlo al expediente de pago sin necesidad de pedir una copia en papel. Si pasadas 24 horas desde la imputación el recibo no aparece en el portal, el organismo puede escribir a cobranzas@atalayadata.example indicando el número de la factura.

## Constancia de libre deuda

Si el organismo necesita una constancia de libre deuda, por ejemplo para participar en otro trámite o para cerrar un ejercicio, la solicita a cobranzas@atalayadata.example indicando su nombre, su número de identificación fiscal y el trámite para el que la necesita. La constancia se emite en un máximo de 3 días hábiles, tiene validez de 60 días corridos y certifica que el organismo no registra facturas vencidas a la fecha de emisión. Si el organismo tiene facturas vencidas, Cobranzas no emite la constancia hasta que se regularicen y se lo informa por correo.

El primer ejemplar de cada constancia es gratuito. Los ejemplares adicionales emitidos dentro del mismo mes se cobran a razón de 800 pesos cada uno. Atalaya Data entrega las constancias en PDF firmado digitalmente; si el organismo requiere un original en papel, puede retirarlo en la sede central. Pasados los 60 días corridos de validez, la constancia deja de servir y debe solicitarse una nueva.
