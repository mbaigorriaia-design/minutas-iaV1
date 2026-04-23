import asyncio
import traceback
import os
from datetime import datetime
from processor import extract_structured_minutes, save_to_markdown

async def main():
    try:
        transcript = """Reunión de Sincronización - Proyecto Tronador II (Subsistema de Aviónica)
Fecha: 19 de Marzo de 2026

[Inicio de la transcripción]

Laura (Líder Proyecto): Buenos días a todos. La idea de hoy es revisar el estado del subsistema de aviónica para la próxima prueba en banco. Carlos, ¿cómo venimos con la integración del nuevo software de telemetría?

Carlos (Ingeniero Software): Hola Laura. Bien, terminamos la rama principal ayer. Sin embargo, estamos viendo una latencia de unos 45 milisegundos en la recepción de datos de los sensores de presión. Es un poco más alto del límite de 30ms que habíamos establecido. 

Laura: Entiendo. ¿Crees que es un problema del puerto de comunicaciones o de la carga de procesamiento?

Carlos: Principalmente carga de procesamiento. Creo que si optimizamos el hilo de lectura podemos bajar esos 15 milisegundos extra. Necesito hasta el viernes para implementar esa corrección.

Laura: Perfecto, anotamos eso como tarea tuya para el viernes. Ana, ¿desde Calidad hay algún bloqueo para las pruebas ambientales de la próxima semana?

Ana (Control de Calidad): Hola. Por ahora el único bloqueo es que no hemos recibido la certificación de calibración de la cámara de vacío térmica. El proveedor dijo que la enviaría hoy a la tarde. Si llega hoy, no hay retrasos. Si no, tendremos que mover la prueba del martes al jueves.

Laura: Ok. Diego, por favor hacé el seguimiento con el proveedor hoy después del mediodía para asegurar que nos manden esa certificación. 

Diego (Operaciones): Entendido, me anoto llamar al proveedor a las 14hs. Por otro lado, les comento que en Operaciones ya preparamos el área limpia tipo ISO 8 para ensamblar los componentes una vez que pasen la prueba de Ana.

Laura: Excelente noticia, gracias Diego. Bueno, resumiendo: Carlos optimiza la latencia para el viernes y Diego persigue al proveedor hoy por la tarde para no retrasar a Ana. ¿Todos de acuerdo?

Carlos: De acuerdo.
Ana: Todo claro.
Diego: Listo.

Laura: Perfecto, cortamos acá entonces. Gracias a todos, buen día.

[Fin de la transcripción]"""
        import time
        start = time.time()
        print("Enviando texto aeroespacial a Ollama... por favor ten paciencia (observa tu uso de CPU)...")
        res = await extract_structured_minutes(transcript)
        elapsed = time.time() - start
        
        # Guarda en la carpeta doc/
        filename = f"minuta_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join("..", "doc", filename)
        save_to_markdown(res, filepath)
        
        print("\n¡Éxito! JSON obtenido (resumido):")
        print(res.json(indent=2))
        print(f"\n✅ El archivo markdown fue creado exitosamente en: {filepath}")
        print(f"⏱️ Tiempo total de procesamiento Ollama: {elapsed:.2f} segundos ({elapsed/60:.2f} minutos)")
        
    except Exception as e:
        print("\nERROR TIPO:", type(e))
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
