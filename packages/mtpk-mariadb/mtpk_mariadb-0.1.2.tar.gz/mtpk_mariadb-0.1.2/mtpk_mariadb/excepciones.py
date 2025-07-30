#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
# ----------------------------------------
# jjandres 2025 - 10-06-2025)
# ----------------------------------------


from typing import Any, Optional
import traceback

class MtpkErrorValidacionDb(Exception):
    """
    Excepción específica para errores de validación dentro del ámbito de base de datos,
    como restricciones, formatos inválidos o violaciones lógicas de consistencia.

    Args:
        mensaje (str): Mensaje del error.
        codigo (str): Código de referencia opcional.
    """
    def __init__(self, mensaje: str, codigo: str = ""):
        self.mensaje = mensaje
        self.codigo = codigo
        super().__init__(f"{mensaje} [{codigo}]")


class MtpkErrorDb(Exception):
    """
    Excepción base para errores críticos relacionados con operaciones de base de datos.
    Registra automáticamente el error y su traza si se proporciona un logger.

    Args:
        mensaje (str): Descripción del error.
        codigo (str): Código de error opcional.
        logger (Optional[Any]): Logger opcional para capturar el evento.
    """
    def __init__(self, mensaje: str, codigo: str = "", logger: Optional[Any] = None):
        self.mensaje = mensaje
        self.codigo = codigo
        texto_error = f"{mensaje} [{codigo}]"

        if logger:
            logger.error(texto_error)
            logger.error(traceback.format_exc())

        super().__init__(texto_error)