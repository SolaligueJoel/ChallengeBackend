from db import *
from datetime import datetime

def create_socio():
    name_socio = input("Ingrese su nombre: ").lower()                                       #Nombre del socio a agregar 
    lista_planes = ["plan medio","plan semi","plan completo"]
    print(lista_planes)

    nuevo_plan = input("Seleccione el plan: ").lower()                                      #Selecciono el plan

    fecha_actual = datetime.now().strftime('%Y-%m-%d')                                      #instancio la fecha actual
        
    if nuevo_plan == "plan medio":  
        try:
            collection_socios.insert_one({"name":name_socio,"plan_id":nuevo_plan,           #Insertando documento en coleccion "socios"
                                          "descuentos":10,"estado":"activo",
                                          "fecha_vigencia":fecha_actual})
            
            id_socio= collection_socios.find_one({"name":name_socio})["_id"]                #Ubicando id_socio                                                                               
            collection_planes.insert_one({"_id":id_socio,"precio":1500})                    #Insertando documento en coleccion "planes"
            collection_descuentos.insert_one({"_id":id_socio,"cantidad_de_aplicaciones":5}) #Insertando documento en coleccion "descuentos"
                        
            print(f"Socio con {nuevo_plan} agregado correctamente a la base de datos\n")
       
        except Exception as e:
            print(e)
        
    elif nuevo_plan == "plan semi":  
        try:
            collection_socios.insert_one({"name":name_socio,"plan_id":nuevo_plan,
                                          "descuentos":15,"estado":"activo",
                                          "fecha_vigencia":fecha_actual})
            
            id_socio= collection_socios.find_one({"name":name_socio})["_id"]
            collection_planes.insert_one({"_id":id_socio,"precio":2000})
            collection_descuentos.insert_one({"_id":id_socio,"cantidad_de_aplicaciones":10})
            
            print(f"Socio con {nuevo_plan} agregado correctamente a la base de datos\n")

        except Exception as e:
            print(e)
        
    elif nuevo_plan == "plan completo":  
        try:
            #Agregando documentos 
            collection_socios.insert_one({f"name":name_socio,"plan_id":nuevo_plan,
                                          "descuentos":20,"estado":"activo",
                                          "fecha_vigencia":fecha_actual})
                                                                                                    
            id_socio= collection_socios.find_one({"name":name_socio})["_id"]                 #Ubicando id_socio
            
            collection_planes.insert_one({"_id":id_socio,"precio":3000})                     #Insertando coleccion en "planes"
            
            collection_descuentos.insert_one({"_id":id_socio,
                                              "cantidad_de_aplicaciones":15})                #Insertando coleccion en "descuentos"

            print(f"Socio con {nuevo_plan} agregado correctamente a la base de datos\n")       
            
        except Exception as e:
            print(e)

        