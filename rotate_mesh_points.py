#Brian Callahan, 2/25/2018

import bpy

def testRun():
    counterClockwise = False
    
    axis = 'x'
    
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

class RotateMeshPoints(bpy.types.Operator):
    
    bl_idname = 'object.resize_uv'
    bl_label = 'Resize UVs'
    
    @classmethod
    def poll(cls, context):
        for o in contest.selected_objects:
            if o.type in {'MESH', 'CURVE’, ‘SURFACE', 'ARMATURE’, ‘LATTICE'}:
                return True
        return False
    
    def execute(self, context):
        
        
        return {'FINISHED'}

def swap(vectorCoords, axis, counterClockwise=False):
    
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

def unregister():
    bpy.utils.unregister_class(RotateMeshPoints)

if __name__ == '__main__':
    register()

testRun()