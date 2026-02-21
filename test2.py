import asyncio
import time
    
async def traer_datos_usuario():
    print("Consultando DB Usuarios...")
    await asyncio.sleep(2) # No bloquea el hilo
    print("Usuarios OK")
    return {"id": 1, "nombre": "Senior"}

async def traer_datos_facturacion():
    print("Consultando DB Facturación...")
    await asyncio.sleep(2)
    print("Facturación OK")
    return {"saldo": 500}

async def main():
    inicio = time.time()

    # Ejecuta ambas tareas concurrentemente
    user, billing = await asyncio.gather(
        traer_datos_usuario(),
        traer_datos_facturacion()
    )

    total = time.time() - inicio
    print(f"Tiempo total asíncrono: {total:.2f} segundos")
    print(f"Usuario: {user}")
    print(f"Facturación: {billing}")

if __name__ == "__main__":
    asyncio.run(main())
