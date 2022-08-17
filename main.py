import reactor.runtime as rt
import time

slider = rt.slider(default = 5)
rt.md('=' * slider.value)
rt.md(f"### Current value is {slider.value}")
rt.md(f"I'm only **visible** when {slider.value} > 1", visible = slider.value > 1)
rt.md(f"I'm only visible when {slider.value} < 99", visible = slider.value < 99)

rt.kv.setdefault('button.clicked', 0)
click_count = rt.kv['button.clicked']
def click_button():
    rt.kv['button.clicked'] += 1

rt.button(f"You clicked me {click_count} times", on_click=click_button)

checkbox = rt.checkbox(True, label="Is img visible?")

rt.img("https://marumego.herokuapp.com/random.gif", visible=checkbox.value)

print(rt.__REGISTRY)
