from datetime import datetime
from dateutil.relativedelta import relativedelta
from db import *
from partner_creation import create_socio


def proceso_pago():
    """
    
    Busco los documentos de socios 
    de las colecciones mediante el metodo
    find()
    
    """
    
    socios = collection_socios.find()                                           
    for socio in socios:
        name_socio = socio["name"]
        estado_socio = socio["estado"]
        descuento_socio = socio["descuentos"]
        id_socio = socio["_id"]

        """
        
        Consulto los datos necesarios, _id y
        precio de los planes de cada socio
        
        """ 
        cantidad_de_aplicaciones = collection_descuentos.find_one({"_id":id_socio})["cantidad_de_aplicaciones"]
        precio_del_plan = collection_planes.find_one({"_id":id_socio})["precio"]

        """
        
        Si el estado del socio es activo y cant_app > 0
        se aplican los descuentos para cada plan cada socio.
        
        """
        if estado_socio == "activo" and cantidad_de_aplicaciones > 0:
            if descuento_socio == 60:                                           #Aplico el descuento segun cada plan asociado
                descuento_del_10 = 60 * (precio_del_plan/100)
                pago_con_descuento = precio_del_plan - descuento_del_10
                if pago_con_descuento < 0:
                    print(f'El precio a pagar es de: $0 para el socio {name_socio}, cantidad de aplicaciones: {cantidad_de_aplicaciones}')
                    
                aplicacion_descuento(id_socio)
                print(f'El precio a pagar es de: {pago_con_descuento} para el socio {name_socio}, cantidad de aplicaciones: {cantidad_de_aplicaciones}')

                pago_socios(id_socio,precio_del_plan)
                
                
            elif descuento_socio == 15:
                descuento_del_quince = 15 * (precio_del_plan/100)
                pago_con_descuento = precio_del_plan - descuento_del_quince
                aplicacion_descuento(id_socio)
                print(f'El precio a pagar es de: {pago_con_descuento} para el socio {name_socio}, cantidad de aplicaciones: {cantidad_de_aplicaciones}')
                pago_socios(id_socio,precio_del_plan)

            elif descuento_socio == 20:
                descuento_del_veinte = 20 * (precio_del_plan/100)
                pago_con_descuento = precio_del_plan - descuento_del_veinte
        
                aplicacion_descuento(id_socio)
                print(f'El precio a pagar es de: {pago_con_descuento} para el socio {name_socio}, cantidad de aplicaciones: {cantidad_de_aplicaciones}')

                pago_socios(id_socio,precio_del_plan)

        elif estado_socio == 'activo' and cantidad_de_aplicaciones <= 0:
            print(f'No tiene descuentos para aplicar el socio {name_socio}, total a pagar: ${precio_del_plan}')
            pago_socios(id_socio,precio_del_plan)

        else:
            print('El socio no se encuentra activo')
            
        
def aplicacion_descuento(id_socio):
    """
    Se resta en 1 la can_de_app de la coleccion descuentos
    
    """
    collection_descuentos.update_one({"_id":id_socio},{"$inc":{"cantidad_de_aplicaciones":-1}})    
         

def pago_socios(id_socio,precio_del_plan):
    """
    Creo la coleccion "pagos"
    
    """
    
    mes_actual = datetime.today().strftime('%B')
    try:
        collection_pagos.insert_one({"_id":id_socio,"periodo_cobrado":mes_actual,
                                    "precio_del_plan":precio_del_plan,
                                    "descuentos_aplicados":0})
    except:
        collection_pagos.update_one({"_id":id_socio},{"$set":{"_id":id_socio}})

    mes_actual = datetime.now().strftime('%B')
    sumando_un_mes = datetime.now() + relativedelta(months=+1)                                             #Defino la fecha actual y agrego un mes de vigencia
    obteniendo_nueva_fecha = sumando_un_mes.strftime('%Y-%m-%d')
    
    """
    Actualizo la fecha_vigencia  en 1 mes, para la coleccion de "socios" 
    
    """
    collection_socios.update_one({"_id":id_socio},{"$set":{"fecha_vigencia":obteniendo_nueva_fecha}})      #Actualizacion del documento de la coleccion "pagos"
    socio_plan = collection_socios.find_one({"_id":id_socio})
    cantidad_de_aplicaciones = collection_descuentos.find_one({"_id":id_socio})["cantidad_de_aplicaciones"]
    if cantidad_de_aplicaciones > 0:
        collection_pagos.update_one({"_id":id_socio},{"$inc":{"descuentos_aplicados":+1}})

    pago = collection_pagos.find_one({"_id":id_socio})
    print(f'Pago realizado:{pago}')
    print(f'Plan del socio: {socio_plan}\n')
     
 


if __name__ == '__main__':
    #Añadir socio
    create_socio()
    #Proceso de cobros
    proceso_pago()

