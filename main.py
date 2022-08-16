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

def reload_img():
    import requests
    import base64
    r = requests.get("https://marumego.herokuapp.com/random.gif")
    base = base64.b64encode(r.content).decode('ascii')
    rt.kv['img.src'] = f"data:image/gif;base64,{base}"

if 'img.src' not in rt.kv:
    reload_img()

rt.button("Refresh image", on_click=reload_img)
rt.img(rt.kv['img.src'], visible=checkbox.value)

print(rt.__REGISTRY)
