# Finanzas — Facturación a organismos
Versión 1.0 — octubre 2026

Este bloque reúne las reglas con las que Atalaya Data emite, entrega y corrige las facturas dirigidas a los organismos públicos. Se refiere siempre a los comprobantes que recibe el organismo cliente.

## Momento de emisión de la factura

Atalaya Data emite la factura de cada período el primer día hábil del mes de servicio, siempre que exista una orden de compra aceptada que la respalde. La facturación es mensual y vencida respecto de la aceptación de la orden, nunca anticipada más allá del mes en curso.

Cuando el contrato prevé pago anual, la factura se emite una sola vez, el primer día hábil del primer mes del período contratado. En ese caso el comprobante cubre doce meses de servicio y su importe corresponde al total anual consignado en la orden de compra.

Si la orden de compra se acepta después del primer día hábil, la factura se emite dentro de los 3 días hábiles posteriores a la aceptación e incluye únicamente el período en curso. Los meses anteriores a la aceptación no se facturan en forma retroactiva por separado, sino que se incorporan al mismo comprobante, con el detalle de cada mes en el cuerpo de la factura.

## Dónde descargar las facturas

Las facturas se publican en el Portal de Clientes, dentro de Facturación, en la sección "Comprobantes", dentro de las 2 horas posteriores a su emisión. Cada comprobante está disponible en PDF y en formato estructurado XML, para que el organismo pueda cargarlo directamente en su sistema contable.

Además, el sistema envía una copia en PDF al correo del responsable administrativo registrado en el contrato. Si el organismo desea que la copia llegue a más de una casilla, puede indicar hasta tres direcciones adicionales mediante el formulario FC-02, disponible en el Portal de Clientes.

Los comprobantes permanecen en el portal durante 10 años desde su emisión. Pasado el primer año, los archivos se trasladan a un repositorio histórico y pueden tardar hasta 24 horas en estar disponibles tras la solicitud. Para pedir un comprobante archivado, el organismo escribe a facturacion@atalayadata.example indicando el número de factura o el período buscado. Los usuarios del organismo con rol administrativo en el Portal de Clientes pueden descargar todos los comprobantes de un año en un único archivo comprimido.

## Datos fiscales que figuran en la factura

La factura muestra los datos fiscales del organismo tal como constan en el registro de clientes de Atalaya Data: denominación oficial, número de identificación fiscal, condición frente al impuesto y domicilio fiscal. Esos datos se cargan en el momento de la contratación, tomándolos de la orden de compra.

Si el organismo cambia su denominación, por ejemplo por una reorganización de ministerios, debe informarlo mediante el formulario FC-03 adjuntando el acto administrativo que dispone el cambio. Atalaya Data actualiza el registro en 5 días hábiles, y las facturas emitidas desde esa fecha reflejan el dato nuevo.

Los comprobantes ya emitidos conservan los datos con los que fueron generados. Atalaya Data no reemite facturas únicamente por un cambio posterior de denominación; solo lo hace cuando el dato erróneo estaba presente desde el origen, mediante una corrección que el organismo solicita a facturacion@atalayadata.example. Antes de cada renovación, Atalaya Data pide al organismo que confirme que los datos fiscales registrados siguen siendo correctos.

## Cómo pedir una corrección de la factura

Si una factura contiene un error de datos, como una denominación equivocada, un período mal consignado o un número de expediente omitido, el organismo debe pedir la corrección dentro de los 15 días corridos posteriores a su emisión. El pedido se envía a facturacion@atalayadata.example con el número de factura y la descripción del error.

El área de Facturación analiza la solicitud en 2 días hábiles. Cuando el error es atribuible a Atalaya Data, se emite una nota de crédito que anula el comprobante y una nueva factura con los datos correctos, sin cargo para el organismo y con la misma fecha de vencimiento original.

Si el error proviene de datos incorrectos en la orden de compra, el procedimiento requiere además que el organismo envíe una orden de compra corregida, con el mismo número de orden y la palabra "corregida" en el asunto. Pasados los 15 días corridos, la corrección sigue siendo posible, pero se trata como una excepción que debe aprobar la jefatura de Facturación.

## Numeración y series de las facturas

Las facturas de Atalaya Data se numeran de forma correlativa dentro de una serie que identifica el tipo de comprobante. La serie A corresponde a las facturas de servicio mensual o anual, la serie B a las facturas de ampliación y la serie R a las facturas de reemplazo emitidas tras una corrección. Cada número se compone de la letra de la serie, un punto de venta de cuatro dígitos y un correlativo de ocho dígitos.

El organismo puede usar esa numeración para ordenar sus archivos, ya que nunca se repite ni se reutiliza, ni siquiera cuando una factura se anula. Los números anulados quedan registrados en el Portal de Clientes con el estado "anulada" y un enlace a la nota de crédito que los reemplaza.

Si el organismo detecta un salto en la numeración que no puede explicar, puede consultarlo escribiendo a facturacion@atalayadata.example. El área de Facturación responde en 3 días hábiles y, si corresponde, entrega una constancia firmada que confirma el estado de cada número de la serie dentro del período consultado.

## Facturas de licencias adicionales

Cuando un organismo suma licencias durante la vigencia del contrato, Atalaya Data emite una factura aparte para esas licencias, sin modificar la factura del servicio principal. Esa factura adicional lleva su propio número y se identifica con la leyenda "Ampliación" seguida del número de la orden complementaria que la respalda.

La factura de ampliación se emite el primer día hábil del mes siguiente a la aceptación de la orden complementaria. Su importe cubre las licencias nuevas por los meses restantes del período vigente, y no por un período completo, de modo que ambos servicios terminan en la misma fecha. Si la orden complementaria se acepta después del día 15, el mes en curso no se cobra. Desde la siguiente factura principal, el nuevo tramo de volumen se aplica a todas las licencias del organismo.

Esta separación facilita al organismo la imputación presupuestaria, ya que cada comprobante responde a una sola orden de compra. Si el organismo prefiere unificar todo en una única factura al renovar, puede solicitarlo en el momento de emitir la orden de renovación y el cambio se aplica desde el período siguiente.

## Facturas con varias partidas presupuestarias

Algunos organismos necesitan que una misma contratación se impute a más de una partida presupuestaria. Atalaya Data admite hasta cuatro partidas por contrato, y emite una factura separada por cada una, con el importe proporcional que el organismo haya definido.

Para activar esta modalidad, el organismo completa el formulario FC-04 indicando el código de cada partida y el porcentaje que le corresponde. Los porcentajes deben sumar el 100 % y no pueden modificarse durante el período de servicio en curso; los cambios rigen a partir de la siguiente renovación.

Cada factura derivada indica la partida en el campo de observaciones y lleva el mismo número de orden de compra. El vencimiento de todas es idéntico, y el pago de una no condiciona el de las demás. Esta modalidad se activa en un plazo máximo de siete días hábiles desde la presentación del formulario. Si una partida se agota durante el período, el organismo debe avisar al área de Facturación para reasignar el porcentaje en la renovación.

## Entrega de facturas por mesa de entradas

Algunos organismos exigen recibir las facturas en papel y selladas por su mesa de entradas para iniciar el trámite de pago. Atalaya Data atiende ese requisito enviando la factura impresa por mensajería a la dirección que el organismo haya indicado en el contrato, dentro de los 5 días hábiles posteriores a la emisión.

El envío en papel no tiene costo cuando se trata de una factura por mes; si el organismo solicita reenvíos adicionales del mismo comprobante, cada reenvío se cobra 1.200 pesos en concepto de gastos de mensajería. El cargo se agrega a la siguiente factura, con el detalle correspondiente.

Atalaya Data conserva el cargo de recepción sellado que devuelve la mensajería, y puede entregar una copia al organismo si la necesita como constancia de la fecha de ingreso. El plazo de vencimiento sigue contándose desde la fecha de emisión, no desde la fecha en que el organismo recibe el papel, salvo que el contrato disponga lo contrario.
