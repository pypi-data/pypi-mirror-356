import py3Dmol
#------------------------------------------------------------------------------------------
def viewmol_RDKit(atoms, width=300, height=300):
    view = py3Dmol.view(width=width, height=height)
    xyz_str=atoms2xyz_str(atoms)
    view.addModel(xyz_str, 'xyz')
    view.setStyle({'sphere': {'scale': 0.3}, 'stick': {'radius': 0.2}})
    view.setBackgroundColor("white")
    view.zoomTo()
    view.show()
#------------------------------------------------------------------------------------------
def viewmol_ASE(atoms, width=300, height=300):
    view = py3Dmol.view(width=width, height=height)
    xyz_str = f"{len(atoms)}\n"
    xyz_str += f"\n"
    for atom in atoms:
        symbol = atom.symbol
        x, y, z = atom.position
        xyz_str += f"{symbol:2s} {x:14.9f} {y:16.9f} {z:16.9f}\n"
    view.addModel(xyz_str, 'xyz')
    view.setStyle({'sphere': {'scale': 0.3}, 'stick': {'radius': 0.2}})
    view.setBackgroundColor("white")
    view.zoomTo()
    view.show()
#------------------------------------------------------------------------------------------

