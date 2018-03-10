#Brian Callahan, 2/25/2018
bl_info = {
    'name' : 'Point Rotation',
    'category' : 'Object',
    'author' : 'BTCallahan',
    "version" : (1, 0, 0),
    "blender" : (2, 79, 0),
    "location" : "3D View > Tool Shelf",
    "description" : "Rotates points of selected mesh/spline/surface/armiture/lattice(s) 90 degrees around an axis."
}

import bpy
from bpy.props import EnumProperty, BoolProperty, StringProperty, PointerProperty

class PointRotationSettings(bpy.types.PropertyGroup):
    
    directionTypes = [
    ('X_POS', 'X', '', 0),
    #('X_NEG', '-X', '', 1),
    ('Y_POS', 'Y', '', 1),
    #('Y_NEG', '-Y', '', 3),
    ('Z_POS', 'Z', '', 2),
    #('Z_NEG', '-Z', '', 5)
    ]
    
    rotationDirection = EnumProperty(default='X_POS', items=directionTypes, name='', description='The direction that the points of the selected object will be rotated in. Points will be rotated using their objects local space.')
    
    useCounterclockwiseRotation = BoolProperty(default = False, name='Use Counterclockwise Rotation', description='If Checked, the points will be rotated counterclockwise.')
    
    rotateObjectLocations = BoolProperty(default = False, name='Rotate All Selected Objects', description='If checked, the objects will be rotated in the same direction as the points, using world space.')

class PointRotationPanel(bpy.types.Panel):
    bl_label = "Point Rotation"
    #bl_idname = "OBJECT_PT_bento_rigging"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Rotate Object Points'
    #bl_context = "create"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        scene = context.scene
        
        toolUsed = scene.rotationSettings
        
        direction = layout.column(True)
        
        direction.label(text='Rotation Direction')
        
        direction.prop(toolUsed, 'rotationDirection')
        
        direction.label(text='Rotate All Selected Objects')

        direction.prop(toolUsed, 'rotateObjectLocations')

        row = direction.row(True)
        row.alignment = 'CENTER'
        row.scale_x=0.9
        row.scale_y=2.0
        
        row.operator('object.rotate_points', text='Rotate Object Points')  
    
class RotateMeshPoints(bpy.types.Operator):
    
    bl_idname = 'object.rotate_points'
    bl_label = 'Resize Points'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        for o in context.selected_objects:
            if o.type in {'MESH', 'CURVE’, ‘SURFACE', 'ARMATURE’, ‘LATTICE'}:
                print('poll suceeded')
                return True
        print('poll failed')
        return False
    
    def execute(self, context):
        print('execution begining...')
        settings = bpy.context.scene.rotationSettings
        
        counterClockwise = settings.useCounterclockwiseRotation
        
        axis = settings.rotationDirection
        
        rotateObjectPositions = settings.rotateObjectLocations
        
        usedData = set()
    
        obs = bpy.context.selected_objects
        
        for o in obs:
            
            if o.data.name not in usedData:
                usedData.add(o.data.name)
                if o.type == 'MESH':
                    for v in o.data.vertices:
                        v.co[0], v.co[1], v.co[2] = swap(v.co, axis, counterClockwise)
                
                elif o.type == 'CURVE':
                    for s in o.data.splines:
                        for b in s.bezier_points:
                            #handle_right
                            b.co[0], b.co[1], b.co[2] = swap(b.co, axis, counterClockwise)
                        for b in s.points:
                            b.co[0], b.co[1], b.co[2] = swap(b.co, axis, counterClockwise)
                
                elif o.type == 'SURFACE':
                    for s in o.data.splines:
                        for b in points:
                            b.co[0], b.co[1], b.co[2] = swap(b.co, axis, counterClockwise)
                
                elif o.type == 'ARMATURE':
                    for b in o.data.edit_bones:
                        
                        b.tail = [swap(b.tail, axis, counterClockwise)]
                        if not b.use_connect:
                            b.head[0], b.head[1], b.head[2] = swap(b.head, axis, counterClockwise)
                
                elif o.type == 'LATTICE':
                    for p in points:
                        p.co_deform[0], p.co_deform[1], p.co_deform[2] = swap(p.co, axis, counterClockwise)
                else:
                    print('invalid type')
                    pass
        
        if rotateObjectPositions:
            for o in obs:
                o.location = swap(o.location, axis, counterClockwise)
        
        return {'FINISHED'}

def swap(vectorCoords, axis, counterClockwise=False):
    print('beginning swap')
    x = vectorCoords[0]
    y = vectorCoords[1]
    z = vectorCoords[2]
    
    if axis == 'x':    
        if counterClockwise:
            
            x = vectorCoords[0]
            y = vectorCoords[2]
            z = vectorCoords[1] * -1
        else:
            
            x = vectorCoords[0]
            y = vectorCoords[2] * -1
            z = vectorCoords[1]
            
    elif axis == 'y':
        if counterClockwise:
            
            x = vectorCoords[2]
            y = vectorCoords[1]
            z = vectorCoords[0] * -1
        else:
            
            x = vectorCoords[2] * -1
            y = vectorCoords[1]
            z = vectorCoords[0]
            
    elif axis == 'z':
        if counterClockwise:
            
            x = vectorCoords[1] * -1
            y = vectorCoords[0]
            z = vectorCoords[2]
        else:
            
            x = vectorCoords[1]
            y = vectorCoords[0] * -1
            z = vectorCoords[2]
    return x, y, z

def register():
    bpy.utils.register_class(RotateMeshPoints)
    bpy.utils.register_class(PointRotationSettings)
    bpy.types.Scene.rotationSettings = PointerProperty(type=PointRotationSettings)
    bpy.utils.register_class(PointRotationPanel)

def unregister():
    bpy.utils.unregister_class(PointRotationPanel)
    del bpy.types.Scene.rotationSettings
    bpy.utils.unregister_class(PointRotationSettings)
    bpy.utils.unregister_class(RotateMeshPoints)

if __name__ == '__main__':
    register()
