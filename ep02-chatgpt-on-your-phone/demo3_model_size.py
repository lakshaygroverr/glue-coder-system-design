# demo3_model_size.py - how much memory does an AI model need?
# memory = number of parameters x bytes per parameter

PHONE_RAM_GB = 8  # change this to your phone's RAM

models = [
    ("Tiny model (1 billion)", 1),
    ("Small model (8 billion)", 8),
    ("Big model (70 billion)", 70),
    ("Huge model (400 billion)", 400),
]

precisions = [("16-bit", 2), ("4-bit (compressed)", 0.5)]

print(f"Your phone: {PHONE_RAM_GB} GB of RAM\n")
for name, billions in models:
    print(name)
    for label, bytes_each in precisions:
        gb = billions * bytes_each
        fits = "fits" if gb < PHONE_RAM_GB * 0.5 else "does NOT fit"
        print(f"   {label:20} {gb:7.1f} GB   -> {fits} on your phone")
    print()
