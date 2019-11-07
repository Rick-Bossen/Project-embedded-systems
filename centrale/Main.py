from centrale.model.Device import Device
from centrale.view.MainView import Root
from centrale.model.SharedVars import SharedVar
from centrale.controller.SerialController import SerialController
from centrale.controller.ViewController import ViewController

sharedvar = SharedVar()
window = Root(sharedvar)
sharedvar.initvars(window)
serialcontroller = SerialController()
viewcontroller = ViewController(window, sharedvar)


# checks for new devices
def checkdevices():
    devices = serialcontroller.find_devices()
    for device in devices:
        try:
            window.nametowidget(device.lower())
        except KeyError:
            window.add_tab(device, devices[device])


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
window.interval(60000, updateview)
window.mainloop()
