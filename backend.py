import kweb.browser
import kweb.viewer
from pathlib import Path

# path = Path('gds/')

# app = kweb.browser.get_app(fileslocation=path)

path = Path('./gds')
lyp_path = Path('./gds/layers1.lyp')  # Add this line with your .lyp file path

# Add debug print
print(f"Layer properties file path: {lyp_path}")
print(f"File exists: {lyp_path.is_file()}")

app = kweb.viewer.get_app(
    fileslocation=path,
    layer_props=lyp_path  # Add this parameter
)
