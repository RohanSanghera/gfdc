def dev_alg(dev):
    if dev < -12:
        dev_class = 'SEVERE'
    elif dev < -6:
        dev_class = 'MODERATE'
    elif dev < -1:
        dev_class = 'MILD'
    else:
        dev_class = 'NO DEFECT'
    return dev_class

def cp_alg(cp1,cp2,cp3,cp4):
    hemifield1 = [cp1, cp3]
    hemifield2 = [cp2, cp4]
    if all(var > 15 for var in (hemifield1 + hemifield2)):
        cp_class = 'NO DEFECT'
    elif any(var == 0 for var in hemifield1) or any(var==0 for var in hemifield2):
        cp_class = 'SEVERE'
    elif (any(var < 15 for var in hemifield1) and all(var > 15 for var in hemifield2)) or (any(var < 15 for var in hemifield2) and all(var > 15 for var in hemifield1)):
        cp_class = 'MODERATE'
    elif any(var < 15 for var in hemifield1) and any(var < 15 for var in hemifield2):
        cp_class = 'SEVERE'
    return cp_class

def final_class(dev_class, cp_class, plot_class):
    if any(var == 'SEVERE' for var in [dev_class, cp_class, plot_class]):
        return 'SEVERE'
    elif any(var == 'MODERATE' for var in [dev_class, cp_class, plot_class]):
        return 'MODERATE'
    elif any(var == 'MILD' for var in [dev_class, cp_class, plot_class]):
        return 'MILD'
    elif any(var == 'NO DEFECT' for var in [dev_class, cp_class, plot_class]):
        return 'NO DEFECT'
    