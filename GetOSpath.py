def GetOSpath():

    import platform
    if platform.system() == 'Darwin':
        Prefix = '/Volumes/projects/'
    elif platform.system() == 'Linux':
        Prefix = '/projects/'
    elif playform.system() == 'Windows':
        Prefix = 'P:/'    
    return Prefix