def GetOSpath():

    import platform
    if platform.system() == 'Darwin':
        Prefix  = '/Volumes/projects/'
        Prefix2 = '/Volumes/procdata/'
    elif platform.system() == 'Linux':
        Prefix  = '/projects/'
        Prefix2 = '/procdata/' 
    elif platform.system() == 'Windows':
        Prefix  = 'P:/'    
        Prefix2 = 'Q:/'
    return (Prefix, Prefix2)