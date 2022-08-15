import reactor.runtime as rt

my_slider = rt.slider(default = 5)
md = rt.md(f"Hello from slider with value {my_slider.value}")

print(rt.__REGISTRY)
