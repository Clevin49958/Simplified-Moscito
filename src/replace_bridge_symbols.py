from collections import defaultdict
import re
from md2pdf.core import md2pdf

# Define the replacement symbols
symbols = {
  "!C": "<font color=green class=club>&clubs;</font>", 
  "!D": "<font color=orange class=diam>&diams;</font>", 
  "!H": "<font color=red class=heart>&hearts;</font>", 
  "!S": "<font color=blue class=spade>&spades;</font>",
  "!M": "<font color=magenta class=major>M</font>",
  "!oM": "<font color=magenta class=major>oM</font>",
  "!minors": "<font color=grassgreen class=minor>minors</font>",
  "!m": "<font color=grassgreen class=minor>m</font>",
  "!om": "<font color=grassgreen class=minor>om</font>"
}

def generate_anchor_tags(input):
  """Detect headings in md and generate anchor tags for them"""
  pattern = r"(#+)\s([\d\w \-\!\(\)\/]+)\n" # regex pattern to detect headings

  anchor_counter = defaultdict(int) # counter for anchor tags
  # while there are still headings in the input string
  while re.search(pattern, input):
    # get heading level and heading text
    heading_level = re.search(pattern, input).group(1)
    heading_text = re.search(pattern, input).group(2)

    anchor_text = heading_text.lower().replace(" ", "-") # generate anchor text
    anchor_text = re.sub(r"[^\w\s-]", "", anchor_text) # remove special characters

    # add counter to anchor text if there are multiple headings with the same text
    anchor_counter[anchor_text] += 1
    if anchor_counter[anchor_text] > 1:
      anchor_text += f"-{anchor_counter[anchor_text] - 1}"

    # generate anchor tag
    anchor_tag = f"<a name='{anchor_text}'></a>"

    print(f"heading level: {heading_level}")
    print(f"heading text: {heading_text}")
    print(f"anchor text: {anchor_text}")
    print()

    input = re.sub(pattern, f"{heading_level} {anchor_tag} {heading_text}\n", input, count=1) # replace heading with anchor tag
  return input

filename = "Moscito"
# Open the file in read and write mode
with open(f"src/{filename}.md", "r+") as file:
  # Read the input string from the file
  input_string = file.read()

  input_string = generate_anchor_tags(input_string)

  # Loop through the symbols and replace them in the input string
  for key, value in symbols.items():
    input_string = input_string.replace(key, value)

  # Move the file pointer to the beginning of the file
  # file.seek(0)

  # Write the output string to the file
  # with open(f"src/System Card {filename}.md", "w") as output:
  #   output.write(input_string)
  
  md2pdf(f"{filename}.pdf",
        md_content=input_string,
        css_file_path="src/markdownhere.css")
