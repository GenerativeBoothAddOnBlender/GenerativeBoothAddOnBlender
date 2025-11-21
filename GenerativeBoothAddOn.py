bl_info = {
    "name": "Generative Booth",
    "author": "Arya Harditya, Graciella T. N. S.",
    "version": (0, 0, 3),
    "blender": (4, 0, 2),
    "location": "3D Viewport > Sidebar > Generative Booth",
    "description": "Generative Booth Add-on",
    "category": "Development",
}

import bpy
import math
import random

pole_length = 1.45
table_length = 1.45

blendMesh = bpy.ops.mesh
blendCtx = bpy.context

# ------------------------------------DEFS-----------------------------------

# ______________MATERIAL______________
            
def add_material(mat_name, col):
    
    mesh_obj = bpy.context.active_object
    color = col
    
    mat = bpy.data.materials.get(mat_name)
    if mat is None:
        mat = bpy.data.materials.new(name=mat_name)
    
    mat.diffuse_color = color

    if not mesh_obj.data.materials:
        mesh_obj.data.materials.append(mat)
    else:
        mesh_obj.data.materials[0] = mat

# ______________BOOTH BASE______________

def add_floor_booth(width, length, height):
    """Creates the main floor object."""
    blendMesh.primitive_cube_add(
        size=1.0,
        enter_editmode=False,
        align='WORLD', 
        location=(0, 0, 1.0),
        scale=(1.0, 1.0, 1.0)
    )
    obj = bpy.context.active_object
    obj.name = "Booth_Floor"
    
    bpy.ops.object.editmode_toggle()
    blendMesh.subdivide(number_cuts=5)
    bpy.ops.object.editmode_toggle()

    obj.scale.x = width
    obj.scale.y = length
    obj.scale.z = height
    
    obj.location.z = height / 2.0
    
def add_roof_booth(width, length, height):
    """Creates the main roof object."""
    blendMesh.primitive_cube_add(
        size=1.0, 
        enter_editmode=False, 
        align='WORLD', 
        location=(0, 0, 2.8), 
        scale=(1.0, 1.0, 1.0)
    )
    obj = bpy.context.active_object
    obj.name = "Booth_Roof"
    
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    bpy.ops.object.editmode_toggle()
    blendMesh.subdivide(number_cuts=5)
    bpy.ops.object.editmode_toggle()
    
    obj.scale.x = width
    obj.scale.y = length
    obj.scale.z = height
    
    obj.location.z = 2.8 + (height / 2.0)

def create_single_wall(wall_name, location, scale, rotation_degrees, color):
    """Creates a single cube wall with specified properties."""
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,  
        enter_editmode=False,
        align='WORLD',
        location=location,
        rotation=(math.radians(rotation_degrees[0]), 
                  math.radians(rotation_degrees[1]), 
                  math.radians(rotation_degrees[2]))
    )
    obj = bpy.context.active_object
    obj.name = wall_name
    
    obj.scale = scale 
    
    mat_name = f"{wall_name}_mat"
    mat = bpy.data.materials.new(name=mat_name)
    mat.diffuse_color = color
    obj.data.materials.append(mat)
    
    bpy.ops.object.select_all(action='DESELECT')
    return obj

def add_all_walls(props):
    """Creates all three walls using the specific wall properties for scale and color."""
    
    create_single_wall(
        wall_name="Booth_Wall_Back",
        location=(0, 0, 0), 
        scale=(props.back_wall_length, props.back_wall_width, props.back_wall_height),
        rotation_degrees=(0, 0, 0), 
        color=props.back_wall_color 
    )

    create_single_wall(
        wall_name="Booth_Wall_Left",
        location=(0, 0, 0),
        scale=(props.left_wall_width, props.left_wall_length, props.left_wall_height),
        rotation_degrees=(0, 0, 0), 
        color=props.left_wall_color
    )

    create_single_wall(
        wall_name="Booth_Wall_Right",
        location=(0, 0, 0),
        scale=(props.right_wall_width, props.right_wall_length, props.right_wall_height),
        rotation_degrees=(0, 0, 0), 
        color=props.right_wall_color
    )

    props.update_back_wall_dimensions(bpy.context)
    props.update_left_wall_dimensions(bpy.context)
    props.update_right_wall_dimensions(bpy.context)

    props.update_back_wall_visibility(bpy.context)
    props.update_left_wall_visibility(bpy.context)
    props.update_right_wall_visibility(bpy.context)

def toggle_wall_visibility(wall_name, visible):
    """Hides or shows a specific wall object."""
    try:
        wall_obj = bpy.data.objects[wall_name]
        wall_obj.hide_set(not visible)
        wall_obj.hide_render = not visible
    except KeyError:
        pass

# ______________BOOTH ELEMENTS______________

def add_table_booth(width, length, height, loc_range):
    """Creates a table object."""
    blendMesh.primitive_cube_add(
        size=1.0, 
        enter_editmode=True, 
        align='WORLD', 
        location=(random.uniform(-loc_range, loc_range), random.uniform(-loc_range, loc_range),  height / 2.0), 
        scale=(width, length, height)
    )
    blendMesh.subdivide(number_cuts=5)
    bpy.ops.object.editmode_toggle()
    
def add_chair_booth(width, length, height, loc_range):
    """Creates a chair object."""
    blendMesh.primitive_cube_add(
        size=1.0, 
        enter_editmode=True, 
        align='WORLD', 
        location=(random.uniform(-loc_range, loc_range), random.uniform(-loc_range, loc_range),  height / 2.0), 
        scale=(width, length, height)
    )
    blendMesh.subdivide(number_cuts=5)
    bpy.ops.object.editmode_toggle()

def add_totem_booth(width, length, height, loc_range):
    """Creates a totem object."""
    blendMesh.primitive_cube_add(
        size=1.0, 
        enter_editmode=True, 
        align='WORLD', 
        location=(random.uniform(-loc_range, loc_range), random.uniform(-loc_range, loc_range),  height / 2.0), 
        scale=(width, length, height)
    )
    blendMesh.subdivide(number_cuts=5)
    bpy.ops.object.editmode_toggle()
    
def create_single_pole(x_loc, y_loc, z_scale, z_loc):
    """Creates a single pole object."""
    bpy.ops.mesh.primitive_cube_add(size=1, align='WORLD')
    
    obj = bpy.context.active_object
    obj.scale.x = 0.1
    obj.scale.y = 0.1
    obj.scale.z = z_scale
    obj.location.z = z_loc
    
    obj.location.x = x_loc
    obj.location.y = y_loc
    
    return obj 

def generate_poles(count, pos_range, pole_color):
    """Generates multiple poles with random positions."""
    pole_z_scale = 2.7
    pole_z_loc = 1.4
    
    for i in range(count):
        x_loc = random.uniform(-pos_range, pos_range)
        y_loc = random.uniform(-pos_range, pos_range)
        
        pole_obj = create_single_pole(x_loc, y_loc, pole_z_scale, pole_z_loc)
        pole_obj.name = f"Booth_Pole_{i+1}" 
        
        mat_name = "pole_mat"
        # Use existing material if possible
        add_material(mat_name, pole_color)
        
        bpy.context.view_layer.objects.active = pole_obj
        pole_obj.select_set(True)
    
    if bpy.context.selected_objects:
        bpy.context.view_layer.objects.active = bpy.context.selected_objects[-1]
        
# ______________LIGHTS______________

def toggle_light_visibility(light_name, visible):
    """Hides or shows a specific light object."""
    try:
        light_obj = bpy.data.objects[light_name]
        light_obj.hide_set(not visible) 
        light_obj.hide_render = not visible 
    except KeyError:
        pass

def add_top_area_light():
    """Adds area light at the top."""
    bpy.ops.object.light_add(type='AREA', radius=5, align='WORLD', location=(0, 0, 5), scale=(1, 1, 1))
    light = bpy.context.object
    light.name = "Area_Light_Top"
    light.data.energy = 200

def add_back_area_light():
    """Adds area light at the back."""
    bpy.ops.object.light_add(type='AREA', radius=3.5, align='WORLD', location=(0, -4, 1.5), rotation=(math.radians(90), 0, 0), scale=(1, 1, 1))
    light = bpy.context.object
    light.name = "Area_Light_Back"
    light.data.energy = 200

def add_front_area_light():
    """Adds area light at the front."""
    bpy.ops.object.light_add(type='AREA', radius=3.5, align='WORLD', location=(0, 4, 1.5), rotation=(math.radians(-90), 0, 0), scale=(1, 1, 1))
    light = bpy.context.object
    light.name = "Area_Light_Front"
    light.data.energy = 200 

def add_left_area_light():
    """Adds area light at the left."""
    bpy.ops.object.light_add(type='AREA', radius=3.5, align='WORLD', location=(4, 0, 1.5), rotation=(0, math.radians(90), 0), scale=(1, 1, 1))
    light = bpy.context.object
    light.name = "Area_Light_Left"
    light.data.energy = 200 
    
def add_right_area_light():
    """Adds area light at the right."""
    bpy.ops.object.light_add(type='AREA', radius=3.5, align='WORLD', location=(-4, 0, 1.5), rotation=(0, math.radians(-90), 0), scale=(1, 1, 1))
    light = bpy.context.object
    light.name = "Area_Light_Right"
    light.data.energy = 200 

def add_all_lights():
    """Calls all individual light creation functions."""
    add_top_area_light()
    add_back_area_light()
    add_front_area_light()
    add_left_area_light()
    add_right_area_light()

# ______________CAMERA______________

def add_keyframed_camera():
    """Adds a camera with keyframed animation."""
    loc_a = (12.0268, 13.0229, 4.59699)
    rot_a = (math.radians(78.6001), math.radians(-0.000062), math.radians(137)) 

    loc_b = (-13.0768, 13.0707, 4.69756)
    rot_b = (math.radians(79.2001), math.radians(0), math.radians(225.2)) 
    
    loc_c = (0.0, 15.3912, 6.08665)
    rot_c = (math.radians(72.2002), math.radians(0), math.radians(180))

    bpy.ops.object.camera_add(
        enter_editmode=False,
        align='WORLD',
        location=loc_a,
        rotation=rot_a
    )
    cam_obj = bpy.context.active_object
    cam_obj.name = "Keyframed_Booth_Camera"
    
    bpy.context.scene.camera = cam_obj

    bpy.context.scene.frame_end = 3

    bpy.context.scene.frame_set(1)
    cam_obj.location = loc_a
    cam_obj.rotation_euler = rot_a
    cam_obj.keyframe_insert(data_path="location", frame=1)
    cam_obj.keyframe_insert(data_path="rotation_euler", frame=1)
    
    bpy.context.scene.frame_set(2)
    cam_obj.location = loc_b
    cam_obj.rotation_euler = rot_b
    cam_obj.keyframe_insert(data_path="location", frame=2)
    cam_obj.keyframe_insert(data_path="rotation_euler", frame=2)
    
    bpy.context.scene.frame_set(3)
    cam_obj.location = loc_c
    cam_obj.rotation_euler = rot_c
    cam_obj.keyframe_insert(data_path="location", frame=3)
    cam_obj.keyframe_insert(data_path="rotation_euler", frame=3)
    
    bpy.context.scene.frame_set(1)
    
    return cam_obj

# ----------------------------------CLASSES-----------------------------------

# ______________BOOTH BASE______________

#________FLOOR__________

class MESH_OT_add_floor(bpy.types.Operator):
    """Create a floor of the booth"""
    bl_idname = "mesh.add_floor_booth"
    bl_label = "Add Floor for the Booth"
    bl_options = {"UNDO"}

    def execute(self, context):
        props = context.scene.generative_booth_props
        
        add_floor_booth(props.floor_width, props.floor_length, props.floor_height)
        add_material("floor_mat", props.floor_color)
        return {"FINISHED"}

#________ROOF__________
class MESH_OT_add_roof(bpy.types.Operator):
    """Create a roof of the booth"""
    bl_idname = "mesh.add_roof_booth"
    bl_label = "Add Roof for the Booth"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.generative_booth_props
        
        add_roof_booth(props.roof_width, props.roof_length, props.roof_height)
        add_material("roof_mat", props.roof_color)
        return {"FINISHED"}

#________WALLS__________
class MESH_OT_add_all_walls(bpy.types.Operator):
    """Create the Back, Left, and Right walls for the booth"""
    bl_idname = "mesh.add_all_walls"
    bl_label = "Add ALL Walls"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        props = context.scene.generative_booth_props
        add_all_walls(props) 
        return {"FINISHED"}

# ______________BOOTH ELEMENTS______________

#________TABLE__________
class MESH_OT_add_table(bpy.types.Operator):
    """Create a table for the booth"""
    bl_idname = "mesh.add_table_booth"
    bl_label = "Add Table for the Booth"
    bl_options = {"UNDO"}
    
    def execute(self, context):
        props = context.scene.generative_booth_props

        add_table_booth(0.4, 1, 0.8, props.table_pos_range) 
        add_material("table_mat", props.table_color)
        return {"FINISHED"}

class OBJECT_OT_modify_table_booth_position(bpy.types.Operator):
    """Randomize the position of the selected Table"""
    bl_idname = "object.modify_table_booth_position"
    bl_label = "Randomize Table Position"
    bl_options = {"UNDO"}

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "No mesh object selected!")
            return {'CANCELLED'}
        
        loc_range = context.scene.generative_booth_props.table_pos_range
        
        obj.location.x = random.uniform(-loc_range, loc_range)
        obj.location.y = random.uniform(-loc_range, loc_range)

        return {"FINISHED"}

#________CHAIR__________
    
class MESH_OT_add_chair(bpy.types.Operator):
    """Create a chair for the booth"""
    bl_idname = "mesh.add_chair_booth"
    bl_label = "Add Chair for the Booth"
    bl_options = {"UNDO"}
    
    def execute(self, context):
        props = context.scene.generative_booth_props

        add_chair_booth(0.4, 0.4, 0.4, props.chair_pos_range)
        add_material("chair_mat", props.chair_color)
        return {"FINISHED"}
    
class OBJECT_OT_modify_chair_booth_position(bpy.types.Operator):
    """Randomize the position of the selected Chair"""
    bl_idname = "object.modify_chair_booth_position"
    bl_label = "Randomize Chair Position"
    bl_options = {"UNDO"}

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "No mesh object selected!")
            return {'CANCELLED'}
        
        loc_range = context.scene.generative_booth_props.chair_pos_range
        
        obj.location.x = random.uniform(-loc_range, loc_range)
        obj.location.y = random.uniform(-loc_range, loc_range)

        return {"FINISHED"}

#________TOTEM__________

class MESH_OT_add_totem(bpy.types.Operator):
    """Create a totem for the booth"""
    bl_idname = "mesh.add_totem_booth"
    bl_label = "Add Totem for the Booth"
    bl_options = {"UNDO"}
    
    def execute(self, context):
        props = context.scene.generative_booth_props
        
        add_totem_booth(0.4, 0.4, 1, props.totem_pos_range)
        add_material("totem_mat", props.totem_color)
        return {"FINISHED"}
    
class OBJECT_OT_modify_totem_booth_position(bpy.types.Operator):
    """Randomize the position of the selected Totem"""
    bl_idname = "object.modify_totem_booth_position"
    bl_label = "Randomize Totem Position"
    bl_options = {"UNDO"}

    def execute(self, context):
        obj = context.active_object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "No mesh object selected!")
            return {'CANCELLED'}
        
        loc_range = context.scene.generative_booth_props.totem_pos_range
        
        obj.location.x = random.uniform(-loc_range, loc_range)
        obj.location.y = random.uniform(-loc_range, loc_range)

        return {"FINISHED"}
    
#________POLES__________

class MESH_OT_add_poles(bpy.types.Operator):
    """Create poles of the booth"""
    bl_idname = "mesh.add_poles_booth"
    bl_label = "Add Poles for the Booth"
    bl_options = {"UNDO"}
    
    def execute(self, context):
        props = context.scene.generative_booth_props
        
        generate_poles(props.pole_count, props.pole_pos_range, props.pole_color)

        return {"FINISHED"}

class OBJECT_OT_modify_poles_position(bpy.types.Operator):
    """Randomize the position of ALL generated Poles"""
    bl_idname = "object.modify_poles_booth_position"
    bl_label = "Randomize Poles Position"
    bl_options = {"UNDO"}

    def execute(self, context):
        loc_range = context.scene.generative_booth_props.pole_pos_range
        bpy.ops.object.select_all(action='DESELECT')
        
        for obj in bpy.data.objects:
            if obj.name.startswith("Booth_Pole_") and obj.type == 'MESH':
                
                obj.location.x = random.uniform(-loc_range, loc_range)
                obj.location.y = random.uniform(-loc_range, loc_range)
                
                obj.select_set(True)

        return {"FINISHED"}

# _____________LIGHTS AND CAMERA______________

#________LIGHTS__________

class OBJECT_OT_add_all_lights(bpy.types.Operator):
    """Create all default area lights and enable visibility toggles"""
    bl_idname = "object.add_all_lights"
    bl_label = "Add ALL Lights"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        add_all_lights()
        props = context.scene.generative_booth_props
        props.light_top_visible = True
        props.light_back_visible = True
        props.light_front_visible = True
        props.light_left_visible = True
        props.light_right_visible = True
        return {"FINISHED"}

#________CAMERA__________
    
class OBJECT_OT_add_keyframed_camera(bpy.types.Operator):
    """Create a camera with keyframed position and rotation for an animation"""
    bl_idname = "object.add_keyframed_camera"
    bl_label = "Add Keyframed Camera"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        add_keyframed_camera()
        self.report({'INFO'}, "Keyframed Camera Added!")
        return {"FINISHED"}


# ------------------------------------PROPERTIES GROUP-----------------------------------

class GenerativeBoothProperties(bpy.types.PropertyGroup):

    #____________FLOOR_______________
    
    def update_floor_color(self, context):
        obj = bpy.data.objects.get("Booth_Floor")
        if obj and obj.type == 'MESH':
            if obj.data.materials:
                mat = obj.data.materials[0]
                mat.diffuse_color = self.floor_color
    
    def update_floor_dimensions(self, context):
        obj = bpy.data.objects.get("Booth_Floor")
        if obj and obj.type == 'MESH':
            obj.scale.x = self.floor_width
            obj.scale.y = self.floor_length
            obj.scale.z = self.floor_height
            obj.location.z = self.floor_height / 2.0
            
            # Trigger wall updates to align them with the new floor edges
            self.update_back_wall_dimensions(context)
            self.update_left_wall_dimensions(context)
            self.update_right_wall_dimensions(context)
                
    #____________ROOF______________
    def update_roof_color(self, context):
        obj = bpy.data.objects.get("Booth_Roof")
        if obj and obj.type == 'MESH':
            if obj.data.materials:
                mat = obj.data.materials[0]
                mat.diffuse_color = self.roof_color
    
    def update_roof_dimensions(self, context):
        obj = bpy.data.objects.get("Booth_Roof")
        if obj and obj.type == 'MESH':
            obj.scale.x = self.roof_width
            obj.scale.y = self.roof_length
            obj.scale.z = self.roof_height

            obj.location.z = 2.8 + (self.roof_height / 2.0)

    #___________WALL_______________
    def update_back_wall_visibility(self, context):
        """Toggles the visibility of the back wall object."""
        toggle_wall_visibility("Booth_Wall_Back", self.back_wall_visible)
        
    def update_left_wall_visibility(self, context):
        """Toggles the visibility of the left wall object."""
        toggle_wall_visibility("Booth_Wall_Left", self.left_wall_visible)

    def update_right_wall_visibility(self, context):
        """Toggles the visibility of the right wall object."""
        toggle_wall_visibility("Booth_Wall_Right", self.right_wall_visible)

    def update_back_wall_dimensions(self, context):
        try:
            obj = bpy.data.objects["Booth_Wall_Back"]
            obj.scale = (self.back_wall_length, self.back_wall_width, self.back_wall_height)

            obj.location.x = 0
            obj.location.y = -self.floor_length / 2.0 - self.back_wall_width / 2.0
            obj.location.z = self.back_wall_height / 2.0
        except KeyError: pass

    def update_back_wall_color(self, context):
        obj = bpy.data.objects.get("Booth_Wall_Back")
        if obj and obj.type == 'MESH' and obj.data.materials:
            obj.data.materials[0].diffuse_color = self.back_wall_color

    def update_left_wall_dimensions(self, context):
        try:
            obj = bpy.data.objects["Booth_Wall_Left"]
            obj.scale = (self.left_wall_width, self.left_wall_length, self.left_wall_height)

            obj.location.x = -self.floor_width / 2.0 - self.left_wall_width / 2.0
            obj.location.y = 0
            obj.location.z = self.left_wall_height / 2.0
        except KeyError: pass
    
    def update_left_wall_color(self, context):
        obj = bpy.data.objects.get("Booth_Wall_Left")
        if obj and obj.type == 'MESH' and obj.data.materials:
            obj.data.materials[0].diffuse_color = self.left_wall_color

    def update_right_wall_dimensions(self, context):
        try:
            obj = bpy.data.objects["Booth_Wall_Right"]
            obj.scale = (self.right_wall_width, self.right_wall_length, self.right_wall_height)

            obj.location.x = self.floor_width / 2.0 + self.right_wall_width / 2.0
            obj.location.y = 0
            obj.location.z = self.right_wall_height / 2.0
        except KeyError: pass

    def update_right_wall_color(self, context):
        obj = bpy.data.objects.get("Booth_Wall_Right")
        if obj and obj.type == 'MESH' and obj.data.materials:
            obj.data.materials[0].diffuse_color = self.right_wall_color

    #____________FLOOR_______________

    floor_color: bpy.props.FloatVectorProperty(name="Floor Color", subtype='COLOR', size=4, min=0.0, max=1.0, default=(1.0, 1.0, 1.0, 1.0), update=update_floor_color)
    floor_width: bpy.props.FloatProperty(name="Width", default=3.0, min=3.0, max=8.0, description="The width of the floor (X-axis)", update=update_floor_dimensions)
    floor_length: bpy.props.FloatProperty(name="Length", default=3.0, min=3.0, max=8.0, description="The length of the floor (Y-axis)", update=update_floor_dimensions)
    floor_height: bpy.props.FloatProperty(name="Height", default=0.1, min=0.01, max=0.1, description="The height of the floor", update=update_floor_dimensions)
    
    #____________ROOF_______________
    
    roof_color: bpy.props.FloatVectorProperty(name="Roof Color", subtype='COLOR', size=4, min=0.0, max=1.0, default=(1.0, 1.0, 1.0, 1.0), update=update_roof_color)
    roof_width: bpy.props.FloatProperty(name="Width", default=3.0, min=3.0, max=8.0, description="The width of the roof", update=update_roof_dimensions)
    roof_length: bpy.props.FloatProperty(name="Length", default=3.0, min=3.0, max=8.0, description="The length of the roof", update=update_roof_dimensions)
    roof_height: bpy.props.FloatProperty(name="Height", default=0.1, min=0.01, max=0.1, description="The height of the roof", update=update_roof_dimensions)

    #____________WALL_____________
    back_wall_length: bpy.props.FloatProperty(name="Length", default=3.0, min=1.0, max=8.0, update=update_back_wall_dimensions) 
    back_wall_width: bpy.props.FloatProperty(name="Thickness", default=0.1, min=0.01, max=0.1, update=update_back_wall_dimensions)
    back_wall_height: bpy.props.FloatProperty(name="Height", default=2.7, min=1.0, max=2.8, update=update_back_wall_dimensions)
    back_wall_visible: bpy.props.BoolProperty(name="Visible", default=True, update=update_back_wall_visibility)
    back_wall_color: bpy.props.FloatVectorProperty(name="Color", subtype='COLOR', size=4, min=0.0, max=1.0, default=(1.0, 1.0, 1.0, 1.0), update=update_back_wall_color)

    left_wall_length: bpy.props.FloatProperty(name="Length", default=3.0, min=1.0, max=8.0, update=update_left_wall_dimensions)
    left_wall_width: bpy.props.FloatProperty(name="Thickness", default=0.1, min=0.01, max=0.1, update=update_left_wall_dimensions)
    left_wall_height: bpy.props.FloatProperty(name="Height", default=2.7, min=1.0, max=2.8, update=update_left_wall_dimensions)
    left_wall_visible: bpy.props.BoolProperty(name="Visible", default=True, update=update_left_wall_visibility)
    left_wall_color: bpy.props.FloatVectorProperty(name="Color", subtype='COLOR', size=4, min=0.0, max=1.0, default=(1.0, 1.0, 1.0, 1.0), update=update_left_wall_color)

    right_wall_length: bpy.props.FloatProperty(name="Length", default=3.0, min=1.0, max=8.0, update=update_right_wall_dimensions)
    right_wall_width: bpy.props.FloatProperty(name="Thickness", default=0.1, min=0.01, max=0.1, update=update_right_wall_dimensions)
    right_wall_height: bpy.props.FloatProperty(name="Height", default=2.7, min=1.0, max=2.8, update=update_right_wall_dimensions)
    right_wall_visible: bpy.props.BoolProperty(name="Visible", default=True, update=update_right_wall_visibility)
    right_wall_color: bpy.props.FloatVectorProperty(name="Color", subtype='COLOR', size=4, min=0.0, max=1.0, default=(1.0, 1.0, 1.0, 1.0), update=update_right_wall_color)

    #____________CHAIR_______________
    def update_chair_color(self, context):
        obj = context.active_object
        if obj and obj.type == 'MESH':
            if obj.data.materials:
                mat = obj.data.materials[0]
                mat.diffuse_color = self.chair_color

    chair_color: bpy.props.FloatVectorProperty(name="Chair Color", subtype='COLOR', size=4, min=0.0, max=1.0, default=(1.0, 1.0, 1.0, 1.0), update=update_chair_color)
    chair_pos_range: bpy.props.FloatProperty(name="Random Position Range", default=1.0, min=0.1, max=4.0, description="Max distance from center for random position")
    
    #____________TABLE_______________
    
    def update_table_color(self, context):
        obj = context.active_object
        if obj and obj.type == 'MESH':
            if obj.data.materials:
                mat = obj.data.materials[0]
                mat.diffuse_color = self.table_color

    table_color: bpy.props.FloatVectorProperty(name="Table Color", subtype='COLOR', size=4, min=0.0, max=1.0, default=(1.0, 1.0, 1.0, 1.0), update=update_table_color)
    table_pos_range: bpy.props.FloatProperty(name="Random Position Range", default=1.0, min=0.1, max=4.0, description="Max distance from center for random table position")
    
    #____________TOTEM______________
    
    def update_totem_color(self, context):
        obj = context.active_object
        if obj and obj.type == 'MESH':
            if obj.data.materials:
                mat = obj.data.materials[0]
                mat.diffuse_color = self.totem_color

    totem_color: bpy.props.FloatVectorProperty(name="Totem Color", subtype='COLOR', size=4, min=0.0, max=1.0, default=(1.0, 1.0, 1.0, 1.0), update=update_totem_color)
    totem_pos_range: bpy.props.FloatProperty(name="Random Position Range", default=1.0, min=0.1, max=4.0, description="Max distance from center for random totem position")
    
    #____________POLE______________
    
    def update_pole_color(self, context):
        mat = bpy.data.materials.get("pole_mat")
    
        if mat:
            mat.diffuse_color = self.pole_color
        else:
            pass

    pole_color: bpy.props.FloatVectorProperty(
        name="Pole Color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0, 1.0),
        update=update_pole_color
    )
    pole_pos_range: bpy.props.FloatProperty(
        name="Random Position Range", 
        default=1.0, 
        min=0.1, 
        max=4.0, 
        description="Max distance from center for random pole position"
    )
    pole_count: bpy.props.IntProperty(
        name="Number of Poles", 
        default=4, 
        min=1, 
        max=20, 
        description="The number of poles to generate"
    )
    
    #____________LIGHT______________
    
    def update_light_visibility_callback(self, context):
        light_map = {
            'light_top_visible': "Area_Light_Top",
            'light_back_visible': "Area_Light_Back",
            'light_front_visible': "Area_Light_Front",
            'light_left_visible': "Area_Light_Left",
            'light_right_visible': "Area_Light_Right",
        }
        for prop_name, light_name in light_map.items():
            if hasattr(self, prop_name):
                visible = getattr(self, prop_name)
                toggle_light_visibility(light_name, visible)
    
    light_top_visible: bpy.props.BoolProperty(name="Top Light", default=True, description="Toggle visibility of the Top Area Light", update=update_light_visibility_callback)
    light_back_visible: bpy.props.BoolProperty(name="Back Light", default=True, description="Toggle visibility of the Back Area Light", update=update_light_visibility_callback)
    light_front_visible: bpy.props.BoolProperty(name="Front Light", default=True, description="Toggle visibility of the Front Area Light", update=update_light_visibility_callback)
    light_left_visible: bpy.props.BoolProperty(name="Left Light", default=True, description="Toggle visibility of the Left Area Light", update=update_light_visibility_callback)
    light_right_visible: bpy.props.BoolProperty(name="Right Light", default=True, description="Toggle visibility of the Right Area Light", update=update_light_visibility_callback)


# ------------------------------------DRAWS-----------------------------------

class GENERATE_Base(bpy.types.Panel):
    bl_label = "Generate Base"
    bl_category = "Generative Booth"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        props = context.scene.generative_booth_props
        
        # ------------------------------------FLOOR-----------------------------------
        box = layout.box()
        box.label(text='Floor', icon='AXIS_TOP')
        
        box.operator("mesh.add_floor_booth", text="Add Floor", icon='ADD')
        
        col = box.column(align=True)
        col.prop(props, "floor_width")
        col.prop(props, "floor_length")
        col.prop(props, "floor_height")
        
        row = box.row()
        row.label(text="    Color:")
        row.prop(props, "floor_color", text="")
        
        # ------------------------------------ROOF-----------------------------------
        box = layout.box()
        box.label(text='Roof', icon='GRID')
        
        box.operator("mesh.add_roof_booth", text="Add Roof", icon='ADD')
        
        col = box.column(align=True)
        col.prop(props, "roof_width")
        col.prop(props, "roof_length")
        col.prop(props, "roof_height")
        
        row = box.row()
        row.label(text="    Color:")
        row.prop(props, "roof_color", text="")
        
        # ------------------------------------WALLS (NEW LAYOUT)-----------------------------------
        box = layout.box()
        box.label(text='Walls', icon='AXIS_SIDE')
        
        box.operator("mesh.add_all_walls", text="Add Walls", icon='ADD')
        
        col = layout.column(align=True)
        
        row = box.row(align=True)
        row.prop(props, "back_wall_visible", icon='HIDE_OFF' if props.back_wall_visible else 'HIDE_ON', text="")
        row.label(text=" Back Wall") 
        
        col = box.column(align=True)
        col.prop(props, "back_wall_length", text="Length")
        col.prop(props, "back_wall_width", text="Width")
        col.prop(props, "back_wall_height", text="Height")
        
        color_row = box.row(align=True)
        color_row.label(text="   Color:")
        color_row.prop(props, "back_wall_color", text="")
        
        col = layout.column(align=True)
        
        row = box.row(align=True)
        row.prop(props, "left_wall_visible", icon='HIDE_OFF' if props.left_wall_visible else 'HIDE_ON', text="")
        row.label(text=" Left Wall")
        
        col = box.column(align=True)
        col.prop(props, "left_wall_length", text="Length")
        col.prop(props, "left_wall_width", text="Width")
        col.prop(props, "left_wall_height", text="Height")
        
        color_row = box.row(align=True)
        color_row.label(text="   Color:")
        color_row.prop(props, "left_wall_color", text="")

        col = layout.column(align=True)

        row = box.row(align=True)
        row.prop(props, "right_wall_visible", icon='HIDE_OFF' if props.right_wall_visible else 'HIDE_ON', text="")
        row.label(text=" Right Wall")
        
        col = box.column(align=True)
        col.prop(props, "right_wall_length", text="Length")
        col.prop(props, "right_wall_width", text="Width")
        col.prop(props, "right_wall_height", text="Height")

        color_row = box.row(align=True)
        color_row.label(text="   Color:")
        color_row.prop(props, "right_wall_color", text="")


class GENERATE_Booth_Elements(bpy.types.Panel):
    bl_label = "Generate Booth Elements"
    bl_category = "Generative Booth"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        props = context.scene.generative_booth_props
        
        # ------------------------------------TABLE-----------------------------------
        box = layout.box()
        box.label(text="Table", icon='NOCURVE')
        box.operator("mesh.add_table_booth", text="Add Table", icon='ADD')
        
        row = box.row()
        row.label(text="    Parameter:")
        row.prop(props, "table_pos_range", text="")
        
        box.operator("object.modify_table_booth_position", text="Generate Position", icon='STICKY_UVS_DISABLE')
        
        row = box.row()
        row.label(text="    Color:")
        row.prop(props, "table_color", text="")
        
        layout.separator()
        
        # ------------------------------------CHAIR-----------------------------------
        box = layout.box()
        box.label(text="Chair", icon='CON_SAMEVOL')

        box.operator("mesh.add_chair_booth", text="Add Chair", icon='ADD')
        
        row = box.row()
        row.label(text="    Parameter:")
        row.prop(props, "chair_pos_range", text="")
        
        box.operator("object.modify_chair_booth_position", text="Generate Position", icon='STICKY_UVS_DISABLE')
        
        row = box.row()
        row.label(text="    Color:")
        row.prop(props, "chair_color", text="")
        
        layout.separator()
        
        # ------------------------------------TOTEM-----------------------------------
        box = layout.box()
        box.label(text="Totem", icon='ASSET_MANAGER')
        box.operator("mesh.add_totem_booth", text="Add Totem", icon='ADD')
        
        row = box.row()
        row.label(text="    Parameter:")
        row.prop(props, "totem_pos_range", text="")
        
        box.operator("object.modify_totem_booth_position", text="Generate Position", icon='STICKY_UVS_DISABLE')
        
        row = box.row()
        row.label(text="    Color:")
        row.prop(props, "totem_color", text="")
        
        layout.separator()
        
        # ------------------------------------POLES-----------------------------------
        box = layout.box()
        box.label(text="Poles", icon='MOD_ARRAY')
        
        row = box.row()
        row.prop(props, "pole_count", text="Count")

        box.operator("mesh.add_poles_booth", text="Add Poles", icon='ADD')

        row = box.row()
        row.label(text="     Parameter:")
        row.prop(props, "pole_pos_range", text="")

        box.operator("object.modify_poles_booth_position", text="Generate Position", icon='STICKY_UVS_DISABLE')

        row = box.row()
        row.label(text="     Color:")
        row.prop(props, "pole_color", text="")

class GENERATE_Lights(bpy.types.Panel):
    bl_label = "Generate Light"
    bl_category = "Generative Booth"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        props = context.scene.generative_booth_props
        
        box = layout.box()
        box.label(text="Lights", icon='LIGHT_AREA')

        box.operator("object.add_all_lights", text="Add Lights", icon='ADD')
        
        col = box.column(align=True)
        col.label(text="Lights Visibility:")
        
        lights = [
            ("light_top_visible", " Top Light"),
            ("light_back_visible", " Back Light"),
            ("light_front_visible", " Front Light"),
            ("light_left_visible", " Left Light"),
            ("light_right_visible", " Right Light"),
        ]

        for prop_name, label in lights:
            row = col.row(align=True)

            row.prop(props, prop_name, icon='HIDE_OFF' if getattr(props, prop_name) else 'HIDE_ON', text="")
            row.label(text=label)

        box = layout.box()
        box.label(text="Camera", icon='OUTLINER_OB_CAMERA')
        box.operator("object.add_keyframed_camera", text="Add Keyframed Camera", icon='ADD')


classes = (
    OBJECT_OT_add_all_lights, 
    MESH_OT_add_table,
    MESH_OT_add_totem,
    MESH_OT_add_chair,
    MESH_OT_add_floor, 
    MESH_OT_add_roof, 
    MESH_OT_add_all_walls, 
    MESH_OT_add_poles,
    OBJECT_OT_modify_chair_booth_position,
    OBJECT_OT_modify_table_booth_position,
    OBJECT_OT_modify_totem_booth_position,
    OBJECT_OT_modify_poles_position,
    OBJECT_OT_add_keyframed_camera,
    GenerativeBoothProperties,
    GENERATE_Base, 
    GENERATE_Booth_Elements, 
    GENERATE_Lights
)

#------------------------------------REGISTER/UNREGISTER-----------------------------------

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.generative_booth_props = bpy.props.PointerProperty(type=GenerativeBoothProperties)


def unregister():
    del bpy.types.Scene.generative_booth_props
    
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
if __name__ == "__main__":
    register()