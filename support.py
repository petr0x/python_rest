from datetime import datetime

def milisToDate(milis):
    minutes = milis.seconds // 60
    seconds = milis.seconds - 60*minutes
    return(str(minutes)+':'+str(seconds))