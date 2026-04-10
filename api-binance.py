import requests
import json
from typing import List, Dict, Optional

def get_usdt_ves_p2p_prices(trade_type: str = "SELL", rows: int = 20) -> Optional[List[Dict]]:
        """
            Obtiene los anuncios P2P de USDT a VES desde la API interna de Binance.
            Maneja la respuesta comprimida (gzip) y los posibles errores 403.
            """
            url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

                # Cabeceras para simular una petición desde un navegador web
                    headers = {
                                "Accept": "*/*",
                                        "Accept-Encoding": "gzip, deflate, br",
                                                "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
                                                        "Content-Type": "application/json",
                                                                "Origin": "https://p2p.binance.com",
                                                                        "Referer": "https://p2p.binance.com/es/trade/sell/USDT?fiat=VES",
                                                                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                                                                                    }

                        payload = {
                                    "asset": "USDT",
                                            "fiat": "VES",
                                                    "page": 1,
                                                            "rows": rows,
                                                                    "tradeType": trade_type, # "SELL" para ver anuncios de vendedores (tú compras)
                                                                            "payTypes": [],          # Puedes añadir métodos de pago específicos
                                                                                    "publisherType": None,
                                                                                            "transAmount": None,     # Cantidad de VES, por ejemplo: "1000"
                                                                                                    "countries": []
                                                                                                        }

                            try:
                                        response = requests.post(url, headers=headers, json=payload)
                                                response.raise_for_status()  # Lanza una excepción si hay un error HTTP
                                                        return response.json().get('data', [])
                            except requests.exceptions.RequestException as e:
                                        print(f"❌ Error en la petición: {e}")
                                                return None

                                            def calcular_precio_ponderado(anuncios: List[Dict]) -> Dict:
                                                    """
                                                        Calcula el precio promedio ponderado por el volumen (cantidad) de los anuncios.
                                                        """
                                                        if not anuncios:
                                                                    return {"precio_promedio": None, "volumen_total": 0, "error": "No hay anuncios para calcular."}

                                                                    total_ponderado = 0.0
                                                                        volumen_total = 0.0

                                                                            for ad in anuncios:
                                                                                        # Los datos del anunciante y el precio vienen en 'adv'
                                                                                        adv = ad.get('adv', {})
                                                                                                precio = float(adv.get('price', 0))
                                                                                                        cantidad_disponible = float(adv.get('surplusAmount', 0)) # Cantidad de USDT disponible

                                                                                                                if precio > 0 and cantidad_disponible > 0:
                                                                                                                                total_ponderado += precio * cantidad_disponible
                                                                                                                                            volumen_total += cantidad_disponible

                                                                                                                                                if volumen_total > 0:
                                                                                                                                                            precio_promedio = total_ponderado / volumen_total
                                                                                                                                                                    return {"precio_promedio": round(precio_promedio, 2), "volumen_total": round(volumen_total, 2)}
                                                                                                                                                else:
                                                                                                                                                            return {"precio_promedio": None, "volumen_total": 0, "error": "No se pudo calcular el precio (volumen total = 0)."}

                                                                                                                                                        def get_usdt_ves_spot_price() -> Optional[float]:
                                                                                                                                                                """
                                                                                                                                                                    Obtiene el precio spot de USDT/VES desde la API pública de Binance (si existe el par).
                                                                                                                                                                    """
                                                                                                                                                                    url = "https://api.binance.com/api/v3/ticker/price"
                                                                                                                                                                        params = {"symbol": "USDTVES"} # Nota: Este par puede no existir. La API pública no tiene todos los pares fiat.
                                                                                                                                                                            try:
                                                                                                                                                                                        response = requests.get(url, params=params)
                                                                                                                                                                                                response.raise_for_status()
                                                                                                                                                                                                        data = response.json()
                                                                                                                                                                                                                return float(data.get('price', 0))
                                                                                                                                                                            except:
                                                                                                                                                                                        # Si el par no existe, la API devolverá un error.
                                                                                                                                                                                        return None

                                                                                                                                                                                    # --- EJECUCIÓN PRINCIPAL ---
                                                                                                                                                                                    if __name__ == "__main__":
                                                                                                                                                                                            print("🔍 Obteniendo precios P2P de USDT/VES...")

                                                                                                                                                                                                # 1. Obtener los anuncios de VENTA (tradeType="SELL") para saber a cuánto venden USDT.
                                                                                                                                                                                                    #    Si quieres ver a cuánto compran, usa tradeType="BUY".
                                                                                                                                                                                                        anuncios = get_usdt_ves_p2p_prices(trade_type="SELL", rows=20)

                                                                                                                                                                                                            if anuncios:
                                                                                                                                                                                                                        # 2. Calcular el promedio ponderado
                                                                                                                                                                                                                        resultado = calcular_precio_ponderado(anuncios)

                                                                                                                                                                                                                                print(f"\n--- 📊 Resultados del Mercado P2P (USDT/VES) ---")
                                                                                                                                                                                                                                        if resultado.get('precio_promedio'):
                                                                                                                                                                                                                                                        print(f"💰 Precio Promedio Ponderado (Venta): {resultado['precio_promedio']:,.2f} VES")
                                                                                                                                                                                                                                                                    print(f"📈 Volumen total de los primeros {len(anuncios)} anuncios: {resultado['volumen_total']:,.2f} USDT")

                                                                                                                                                                                                                                                                                # 3. (Opcional) Comparar con el precio spot
                                                                                                                                                                                                                                                                                            precio_spot = get_usdt_ves_spot_price()
                                                                                                                                                                                                                                                                                                        if precio_spot:
                                                                                                                                                                                                                                                                                                                            print(f"\n💹 Precio Spot (referencia): {precio_spot:,.2f} VES")
                                                                                                                                                                                                                                                                                                                                            diferencia = resultado['precio_promedio'] - precio_spot
                                                                                                                                                                                                                                                                                                                                                            print(f"📊 Diferencia (P2P - Spot): {diferencia:+,.2f} VES")
                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                        print(f"❌ {resultado.get('error', 'No se pudo calcular el precio.')}")
                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                    print("❌ No se pudieron obtener los anuncios.")
