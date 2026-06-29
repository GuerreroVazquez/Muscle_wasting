import yaml

def generate_cytoscape_node_border_paint_style(yaml_file_path):
    """
    Reads a YAML file containing Cytoscape pathway groupings and colors,
    and generates the NODE_BORDER_PAINT visual property XML section.

    Args:
        yaml_file_path (str): The path to the YAML file.

    Returns:
        str: A string containing the XML for the NODE_BORDER_PAINT visual property.
    """
    try:
        with open(yaml_file_path, 'r') as file:
            data = yaml.safe_load(file)
    except FileNotFoundError:
        return f"Error: The file '{yaml_file_path}' was not found."
    except yaml.YAMLError as e:
        return f"Error parsing YAML file: {e}"

    if not data or 'groups' not in data:
        return "Error: YAML file does not contain expected 'groups' key."

    # check that no pathay item repeats in data
    all_pathways = set()
    duplicate_pathways = set()
    for group in data['groups']:
        if 'pathways' in group:
            for pathway in group['pathways']:
                if pathway in all_pathways:
                    duplicate_pathways.add(pathway)
                    group['pathways'].remove(pathway)
                    continue
                all_pathways.add(pathway)

    
    xml_output = '<visualProperty default="#ECE2F0" name="NODE_BORDER_PAINT">\n'
    xml_output += '  <discreteMapping attributeName="pathways" attributeType="string">\n'

    # Process each group from the YAML
    for group_data in data['groups']:
        group_name = group_data.get('groupName', 'Unnamed Group')
        group_color = group_data.get('color', '#ECE2F0') # Default if color is missing

        if 'pathways' in group_data and group_data['pathways']:
            for pathway in group_data['pathways']:
                # Remove any special characters from the pathway name
                escaped_pathway = pathway.strip()                
                xml_output += f'    <discreteMappingEntry attributeValue="{escaped_pathway}" value="{group_color}"/>\n'
        else:
            # Optional: Log or warn if a group has no pathways
            print(f"Warning: Group '{group_name}' has no pathways defined.")

    xml_output += '  </discreteMapping>\n'
    xml_output += '</visualProperty>'

    return xml_output

if __name__ == "__main__":
    # IMPORTANT: Replace 'your_pathways.yml' with the actual path to your YAML file.
    # Make sure the YAML file is saved with the structure provided in the previous example.
    yaml_file_path = 'pathways_grouping.yml' 
    save_path = 'grouped_pathways.txt'
    with open(yaml_file_path, 'r') as file:
        yaml_file = file.read()    
    print(f"Generating Cytoscape style from {yaml_file_path}...")
    # Generate and print the XML
    cytoscape_style_xml = generate_cytoscape_node_border_paint_style(yaml_file_path)
    with open(save_path, 'w') as file:
        file.write(cytoscape_style_xml)

    # Optionally, save the output to a file
    # with open("NODE_BORDER_PAINT_style.xml", "w") as xml_file:
    #     xml_file.write(cytoscape_style_xml)
    # print("Saved the generated XML to NODE_BORDER_PAINT_style.xml")