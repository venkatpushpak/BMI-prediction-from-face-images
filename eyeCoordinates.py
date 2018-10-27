import distanceFormulaCalculator

def distanceRightEye(c):
    eR_36,eR_37,eR_38,eR_39,eR_40,eR_41 = 0,0,0,0,0,0
    eR_36 = c[35]
    eR_37 = c[36]
    eR_38 = c[37]
    eR_39 = c[38]
    eR_40 = c[39]
    eR_41 = c[40]
    x1 = distanceFormulaCalculator.distanceFormula(eR_37,eR_41)
    x2 = distanceFormulaCalculator.distanceFormula(eR_38,eR_40) 
    return ((x1+x2)/2)

def distanceLeftEye(c):
    eL_42,eL_43,eL_44,eL_45,eL_46,eL_47 = 0,0,0,0,0,0
    eL_42 = c[41]
    eL_43 = c[42]
    eL_44 = c[43]
    eL_45 = c[44]
    eL_46 = c[45]
    eL_47 = c[46]
    x1 = distanceFormulaCalculator.distanceFormula(eL_43,eL_47)
    x2 = distanceFormulaCalculator.distanceFormula(eL_44,eL_46) 
    return ((x1+x2)/2)



def eyePoints():
    return [36,37,38,39,40,41,42,43,44,45,46,47]