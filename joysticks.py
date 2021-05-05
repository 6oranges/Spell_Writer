pygame.joystick.init()
try:
    self.joystick
except:
    self.joystick=pygame.joystick.Joystick()
if self.joysticks.get_button(1) == 1:
    swingsword()
if round(self.joystick.get_axis(0)) == -1:
    pointleft()
    moving(True)
elif round(self.joystick.get_axis(0)) == 1:
    pointright()
    moving(True)
elif round(self.joystick.get_axis(1)) == -1:
    pointup()
    moving(True)
elif round(self.joystick.get_axis(1)) == 1:
    pointdown()
    moving(True)
else:
    moving(False)
