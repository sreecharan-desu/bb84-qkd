import json
import sys
import argparse

def edit_notebook(file_path, search_text, replacement_text):
    """
    Utility to find and replace text within the code cells of a Jupyter Notebook.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        modified_count = 0
        for cell in notebook.get('cells', []):
            if cell.get('cell_type') == 'code':
                # source can be a single string or a list of strings
                source = cell.get('source', [])
                if isinstance(source, list):
                    source_str = "".join(source)
                else:
                    source_str = source
                
                if search_text in source_str:
                    new_source_str = source_str.replace(search_text, replacement_text)
                    # Convert back to list if it was a list (Jupyter standard)
                    if isinstance(source, list):
                        cell['source'] = [line + ("" if line.endswith("\n") else "\n") 
                                         for line in new_source_str.splitlines()]
                        if cell['source']:
                            cell['source'][-1] = cell['source'][-1].rstrip("\n")
                    else:
                        cell['source'] = new_source_str
                    modified_count += 1
        
        if modified_count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=1)
            print(f"Successfully modified {modified_count} cells in {file_path}.")
        else:
            print(f"No matches found for '{search_text}' in {file_path}.")
            
    except Exception as e:
        print(f"Error editing notebook: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Edit strings inside code cells of a .ipynb file.")
    parser.add_argument("file", help="Path to the .ipynb file")
    parser.add_argument("search", help="Text to search for")
    parser.add_argument("replace", help="Replacement text")
    
    args = parser.parse_args()
    edit_notebook(args.file, args.search, args.replace)
