using CairoMakie
using FileIO

fig = Figure(resolution = (2400, 2500))
ax1 = fig[1, 1] = Axis(fig)
ax2 = fig[2, 1] = Axis(fig)

ax1.aspect = DataAspect()
ax2.aspect = DataAspect()

adc = rotr90(load("nilered_adc_timings_spectra.png"))
tddft = rotr90(load("nilered_tddft_timings_spectra.png"))

image!(ax1, adc)
image!(ax2, tddft)

label_a = fig[1, 1, TopLeft()] = Label(fig, "a)", textsize = 80, halign = :right)
label_b = fig[2, 1, TopLeft()] = Label(fig, "b)", textsize = 80, halign = :right)
tightlimits!.([ax1, ax2])
hidedecorations!(ax1)
hidedecorations!(ax2)
hidespines!(ax1)
hidespines!(ax2)

trim!(fig.layout)

save("timings_spectra.pdf", fig)
save("timings_spectra.png", fig)