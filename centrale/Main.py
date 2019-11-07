from model.Device import Device
from view.MainView import Root
from model.SharedVars import SharedVar
from controller.SerialController import SerialController
from controller.ViewController import ViewController

serialcontroller = SerialController()

sharedvar = SharedVar()
window = Root(sharedvar, serialcontroller)
sharedvar.initvars(window)
viewcontroller = ViewController(window, sharedvar)


def check_devices():
    devices = serialcontroller.find_devices()
    for device in devices:
        try:
            window.nametowidget(device.lower())
        except KeyError:
            window.add_tab(device, devices[device])
    serialcontroller.check_connections()


def check_input():
    input = serialcontroller.read_input()
    for device in input:
        print(device, input[device])


window.interval(1000, check_devices)
window.interval(6000, check_input)
window.mainloop()
