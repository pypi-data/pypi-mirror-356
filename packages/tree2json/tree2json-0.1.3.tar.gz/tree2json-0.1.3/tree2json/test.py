from tree2json import Tree2Json

tree_str = """
esktop
├── 5个创新模块.pdf
├── AIproject
|  ├── mnist.zip
|  └── 论文
├── bihui_pic
|  ├── 4
|  └── ccccz
├── Blender 4.3.lnk
├── 钉钉.lnk
└── 飞书.lnk
"""

if __name__ == "__main__":
    converter = Tree2Json(mode="auto")
    converter.from_string(tree_str)
    converter.to_json("result.json")
    print(converter.to_json())