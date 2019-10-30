from centrale.model.Device import Device
from centrale.view.main import Root
from centrale.model.SharedVars import SharedVar
from centrale.controller.SerialController import SerialController
from centrale.controller.ViewController import ViewController

sharedvar = SharedVar()
window = Root(sharedvar)
sharedvar.initvars(window)
serialcontroller = SerialController()
viewcontroller = ViewController(window, sharedvar)
# devices = serialcontroller.find_devices()


def test():
    devices = serialcontroller.find_devices()
    for device in devices:
        try:
            window.nametowidget(device.lower())
        except KeyError:
            window.add_tab(device, devices[device])

def test2():
    input = serialcontroller.read_input()
    for device in input:
        print(device, input[device])

window.interval(1000, test)
window.interval(60000, test2)
window.mainloop()
