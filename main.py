import reactor.runtime as rt

slider = rt.slider(default = 5)
rt.md(f"Current value is {slider.value}")
rt.md(f"I'm only visible when {slider.value} > 1", visible = slider.value > 1)
rt.md(f"I'm only visible when {slider.value} < 99", visible = slider.value < 99)
rt.button("Click me", on_click=lambda: print("\n\n\nClicked\n\n\n"))

print(rt.__REGISTRY)
