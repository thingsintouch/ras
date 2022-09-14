import psutil
from common.logger import loggerINFO, loggerCRITICAL, loggerDEBUG

cpu_count = psutil.cpu_count()

def get_hardware_status():
    memUsedPercent = int(round(psutil.virtual_memory().percent))
    cpuPerc = int(round(psutil.cpu_percent()))
    loadAvg = psutil.getloadavg()
    temperatures = psutil.sensors_temperatures()
    try:
        temperatureCurrent = int(psutil.sensors_temperatures()['cpu_thermal'][0].current)
    except KeyError:
        try:
            temperatureCurrent = int(psutil.sensors_temperatures()['cpu-thermal'][0].current)
        except KeyError:
            temperatureCurrent = None

    loadAvgPerc = [ int(round(l*100/cpu_count)) for l in loadAvg]
    loggerDEBUG(f"RAM usage - memUsedPercent {memUsedPercent}%")    
    loggerDEBUG(f"cpuPerc {cpuPerc}%") 
    loggerDEBUG(f"loadAvgPerc 1min:{loadAvgPerc[0]}% - 5min:{loadAvgPerc[1]}% - 15min:{loadAvgPerc[2]}%" ) 
    loggerDEBUG(f"current temperature {temperatureCurrent}°C")

    return (temperatureCurrent, loadAvgPerc[1], memUsedPercent)