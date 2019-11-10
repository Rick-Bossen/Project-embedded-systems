from view.MainView import Root
from controller.SerialController import SerialController

serialcontroller = SerialController()

window = Root(serialcontroller)


# checks for new devices
def checkdevices():
    devices = serialcontroller.find_devices()
    for device in devices:
        try:
            window.nametowidget(device.lower())
        except KeyError:
            window.add_tab(device, devices[device])
    serialcontroller.check_connections()


# updates the view with new data
def updateview():
    serialcontroller.check_connections()
    input = serialcontroller.read_input()
    for device in input:
        if input[device]:
            print(input[device])
            window.updatetab(device, input[device])
    window.updatedataview(input)


window.interval(1000, checkdevices)
window.interval(6000, updateview)
window.mainloop()
