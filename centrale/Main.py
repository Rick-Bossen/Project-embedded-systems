from controller.SerialController import SerialController
from controller.ViewController import ViewController
from view.MainView import Root

serial_controller = SerialController()
view_controller = ViewController(serial_controller)
window = Root(view_controller)

view_controller.window = window
window.interval(1000, view_controller.check_devices)
window.interval(6000, view_controller.update_view)

window.mainloop()
