import javalang
from snowflake.snowpark.files import SnowflakeFile

def parse_java_file(file_path):
    try:
        with SnowflakeFile.open(file_path, 'r',require_scoped_url=False) as file:
            java_code = file.read()
            print(f"Parsing file {file_path}")
            tree = javalang.parse.parse(java_code)
            print("File parsed")
            found_methods = []
            lines = java_code.splitlines()
            print("Collecting methods")
            for path, node in tree.filter(javalang.tree.ClassDeclaration):
                for method in node.methods:
                    print(f"Method {method.name} - {method.body[0].position} -- {method.body[-1].position}")
                    method_code = lines[method.body[0].position.line:method.body[-1].position.line]
                    method_code = ("\\n".join(method_code)).strip()
                    if method_code:
                        print(method_code)
                        found_methods.append({"name": node.name + "." + method.name,"code": method_code})
            return found_methods
    except Exception as e:
            return []
    
