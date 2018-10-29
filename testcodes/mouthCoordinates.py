import distanceFormulaCalculator

def distanceBetweenMouth(c):
    m_60,m_61,m_62,m_63,m_64,m_65,m_66,m_67 = 0,0,0,0,0,0,0,0
    m_60 = c[59]
    m_61 = c[60]
    m_62 = c[61]
    m_63 = c[62]
    m_64 = c[63]
    m_65 = c[64]
    m_66 = c[65]
    m_67 = c[66]
    x1 = distanceFormulaCalculator.distanceFormula(m_61,m_67)
    x2 = distanceFormulaCalculator.distanceFormula(m_62,m_66)
    x3 = distanceFormulaCalculator.distanceFormula(m_63,m_65)   
    return ((x1+x2+x3)/3)



def mouthPoints():
    return [60,61,62,63,64,65,66,67]