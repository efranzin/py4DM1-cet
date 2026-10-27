# Written by ahmed khalil ahmed.khalil@areasciencepark.it
#
# Import modules for file system operations (os), JSON parsing (json), 
# and regular expressions -- regex (re)
import os, json, re

# Import PIL for image loading and matplotlib for visualization
from PIL import Image
import matplotlib.pyplot as plt


# Class for visualizing SEM images alongside selected metadata
class SEMVisualizer:
    def __init__(self, json_path, image_path):
        # Store the path to the cleaned metadata JSON file
        self.json_path = json_path
        
        # Store the path to the SEM image file
        self.image_path = image_path
        
        # Define the list of metadata variables to extract and display
        self.variables = [
            "AP_WD",
            "AP_BEAM_TIME",
            "AP_IMAGE_PIXEL_SIZE",
            "AP_HOLDER_HEIGHT",
            "AP_BEAM_CURRENT",
            "AP_HOLDER_DIAMETER"]        
        
        # Initialize an empty dictionary to hold loaded metadata
        self.metadata = {}

    # Load metadata from JSON file into self.metadata
    def load_metadata(self):
        """
        Reads the cleaned JSON file (self.json_path) into self.metadata.
        """

        with open(self.json_path, "r") as f:
            f = json.load(f)
    
        self.metadata = f

        # TODO (Task 3): implement this method
        # raise NotImplementedError("load_metadata is not implemented yet")       


    def clean_value(self, raw_value, variable_name=None):
        """
        Splits a cleaned metadata value into its number and unit.

        The value must be a (signed) number, optionally in scientific
        notation, followed by a unit. Otherwise ("N/A", "N/A") is returned.

        Examples:
            "3.18 mm"         ->  ("3.18", "mm")
            "-13 pA"          ->  ("-13", "pA")
            "2.34e-006 mbar"  ->  ("2.34e-006", "mbar")
            "InLens" or None  ->  ("N/A", "N/A")

        Returns:
            (value, unit) as strings, or ("N/A", "N/A") if no
            number followed by a unit is found
        """

        # Ensure the input is a string before applying regex
        if not isinstance(raw_value, str):
            return ("N/A", "N/A")

        # Use regex to match a signed number (optionally in scientific notation)
        # followed by its unit, e.g. '-13 pA', '2.34e-006 mbar'
        match = re.fullmatch(
            r'([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)\s*([^\d\s].*)', raw_value.strip())

        # If a match is found, return the value and the unit
        if match:
            value, unit = match.groups()
            return (value, unit)

        # Return fallback values (Not Available) if no match is found
        return ("N/A", "N/A")

    def extract_variables(self):
        """
        Extracts selected metadata variables and formats
        them into (name, value, unit) tuples for display.        
        Missing variables give (name, "N/A", "N/A").
        Return the list of formatted metadata rows
        """

        self.listMetaData = []

        for v in self.variables:
            self.listMetaData.append((v, *self.clean_value(self.metadata.get(v, None))))

        return self.listMetaData

    def show_image_with_table(self):
            """
            Displays the SEM image alongside a formatted metadata
            table and saves the combined output as a figure.

            1. Loads the metadata.
            2. Builds a figure with two vertically stacked panels:
            the grayscale SEM image (top) and a table with the
            column labels "Variable", "Value", "Unit" (bottom).
            3. Creates the folder ./output if needed.
            4. Saves the figure as ./output/<image name without extension>.png
            5. Displays the figure, then closes it.
            """
            # 1. Load metadata and prepare data rows
            self.load_metadata()
            table_data = self.extract_variables()
            headers = ["Variable", "Value", "Unit"]

            # Load image via PIL
            img = Image.open(self.image_path)

            # 2. Build figure with 2 vertically stacked subplots (top: image, bottom: table)
            fig, (ax_img, ax_tbl) = plt.subplots(
                2, 1, figsize=(8, 10), gridspec_kw={'height_ratios': [3, 1]}
            )

            # Display grayscale SEM image on top panel
            ax_img.imshow(img, cmap='gray')
            ax_img.axis('off')

            # Hide axes for the table panel
            ax_tbl.axis('off')

            # Create table on bottom panel
            table = ax_tbl.table(
                cellText=table_data,
                colLabels=headers,
                loc='center',
                cellLoc='center'
            )
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1, 1.5)

            plt.tight_layout()

            # 3. Create ./output directory if needed
            output_dir = "./output"
            os.makedirs(output_dir, exist_ok=True)

            # 4. Generate save path (<image name without extension>.png)
            base_name = os.path.splitext(os.path.basename(self.image_path))[0]
            save_path = os.path.join(output_dir, f"{base_name}.png")
            plt.savefig(save_path, bbox_inches='tight', dpi=300)

            # 5. Display figure and close
            plt.show()
            plt.close(fig)