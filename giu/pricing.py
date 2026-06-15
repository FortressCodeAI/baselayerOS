GIU_TO_CAD = 0.01

def giu_to_cad(gius: int) -> float:
    return gius * GIU_TO_CAD

def cad_to_giu(cad: float) -> int:
    return int(cad / GIU_TO_CAD)
