import logging
from pathlib import Path

from services import HotelService

def inicializar_db():
    archivo = Path("hotel.csv")
    if not archivo.exists():
        with archivo.open("w", encoding="utf-8") as f:
            f.write("numero,tipo,precio,capacidad,disponible\n")


def app():
    logging.basicConfig(
        filename="hotel.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    inicializar_db()

    logging.info(f"App iniciada")
    hotelService = HotelService()
    hotelService.iniciar_atencion()

if __name__ == "__main__":
    app()
