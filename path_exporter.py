# Path Exporter 1.0

bl_info = {
    "name": "Export Path to ThreeJS",
    "author": "Marco Marchesi",
    "version": (1, 1),
    "blender": (2, 73, 0),
    "description": "Export path vertices to threejs",
    "category": "Import-Export"}


import bpy,bpy_extras
from bpy_extras.io_utils import ExportHelper
import mathutils


def do_export(context, filepath):

    ob = context.active_object
    wmtx = context.active_object.matrix_world

    file = open(filepath, "wb")
    file.write(bytes('var sampleClosedSpline = new THREE.ClosedSplineCurve3( [\n', 'UTF-8'))

    for v in ob.data.splines[0].points:
        worldCoord = v.co * wmtx
        worldCoord.x += wmtx[0][3]
        worldCoord.y += wmtx[1][3]
        worldCoord.z += wmtx[2][3]
        
        #swap y and z because of Y-Up (threejs) and Z-Up (Blender) default
        thisVertex = 'new THREE.Vector3(' + str(round(worldCoord.x,2)) + ',' + str(round(worldCoord.z,2)) + ',' + str(-1*round(worldCoord.y,2)) + '),\n'
        file.write(bytes(thisVertex, 'UTF-8'))
    file.write(bytes('] );', 'UTF-8'))
    file.flush()
    file.close()
    return True


###### EXPORT OPERATOR #######
class PathExporter(bpy.types.Operator, ExportHelper):
    """Export the active path as an array of vertices to use within threejs"""
    bl_idname = "export.js"
    bl_label = "Path Exporter"

    filename_ext = ".js"

    @classmethod
    def poll(cls, context):
        return context.active_object.type in {'CURVE'}

    def execute(self, context):
        # start_time = time.time()
        print('\n_____START_____')
        filepath = self.filepath
        filepath = bpy.path.ensure_ext(filepath, self.filename_ext)

        exported = do_export(context, filepath)

        if exported:
            # print('finished export in %s seconds' %((time.time() - start_time)))
            print(filepath)

        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager

        if True:
            # File selector
            wm.fileselect_add(self) # will run self.execute()
            return {'RUNNING_MODAL'}
        elif True:
            # search the enum
            wm.invoke_search_popup(self)
            return {'RUNNING_MODAL'}
        elif False:
            # Redo popup
            return wm.invoke_props_popup(self, event)
        elif False:
            return self.execute(context)


### REGISTER ###

def menu_func(self, context):
    self.layout.operator(PathExporter.bl_idname, text="Path for JS Format(.js)")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_func)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_export.remove(menu_func)

if __name__ == "__main__":
    register()
