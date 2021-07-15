bl_info = {
	"name" : "Align UV Island",
	"author" : "SpdB3d",
	"version" : (1, 0, 7),
	"blender" : (2, 90, 0),
	"description" : "Align UV Islands by selecting one edge",
	"category" : "UV",}

import bpy
import bmesh
import math
from bpy.props import (StringProperty,
							BoolProperty,
							IntProperty,
							FloatProperty,
							FloatVectorProperty,
							EnumProperty,
							PointerProperty,
							)
from bpy.types import (Panel,
							Operator,
							AddonPreferences,
							PropertyGroup,
							)

class MySettings(PropertyGroup):

	my_bool : BoolProperty(
		name="Rotate",
		description="Rotate islands when packing",
		default = False
		)
	my_float : FloatProperty(
		name="Margin",
		description="Specify the margin when packing the islands",
		default = 0.0 ,
		min = 0.0 ,
		max = 1.0 ,
		soft_min = 0.0 ,
		soft_max = 1.0 ,
		precision = 3 ,
		step = 0.001 ,
		subtype = "FACTOR" ,
		)

class Align_UV_Island(Panel):
	bl_space_type = 'IMAGE_EDITOR'
	bl_region_type = 'UI'
	bl_label = 'UV Align'
	bl_category = 'UV Align'
	
	def draw(self, context):
		layout = self.layout
		scene = context.scene
		mytool = scene.my_tool
		
		row = layout.row()
		row.operator('uv.simple_operator', text='Align UV Island')
		row = layout.row()
		row.operator('uv.simple_operator2', text='Hard edges from islands')
		layout.row().separator()
		
		row = layout.row()
		row.operator('uv.simple_operator3', text='Pack together')
		layout.prop(mytool, "my_bool", text="Rotate")
		layout.prop(mytool, "my_float", text="Margin")


def main(context):
	uve = []
	uvee = []
	obj = context.active_object
	me = obj.data
	bm = bmesh.from_edit_mesh(me)
	

	uv_layer = bm.loops.layers.uv.verify()
		

	
	for f in bm.faces:
		for l in f.loops:
				luv = l[uv_layer]
				if luv.select:
					
					uve.append(luv.uv)
					uvee.append(luv)

		
	ab = [uve[0].x - (uve[0].x + uve[1].x)/2  ,  uve[0].y - (uve[0].y + uve[1].y)/2 ]
	ac = [uve[0].x - (uve[0].x + uve[1].x)/2 , 0]
	
	u_v = ab[0] * ac[0] + ab[1] * ac[1]

	_u_ = math.sqrt(ab[0]**2 + ab[1]**2)
	_v_ = math.sqrt(ac[0]**2 + ac[1]**2)

	_uv_ = _u_ * _v_

	i = 1
	while(_uv_ == 0 and i != len(uve)):
		ab = [uve[0].x - (uve[0].x + uve[i].x)/2  ,  uve[0].y - (uve[0].y + uve[i].y)/2 ]
		ac = [uve[0].x - (uve[0].x + uve[i].x)/2 , 0]
		
		u_v = ab[0] * ac[0] + ab[1] * ac[1]

		_u_ = math.sqrt(ab[0]**2 + ab[1]**2)
		_v_ = math.sqrt(ac[0]**2 + ac[1]**2)

		_uv_ = _u_ * _v_
		
		i += 1
		
	if _uv_ == 0:
		angle = 0
	else:    
		angle = math.degrees(math.acos(u_v/_uv_))
		
		
	###########################################################
	
	ab = [uve[0].x - (uve[0].x + uve[1].x)/2  ,  uve[0].y - (uve[0].y + uve[1].y)/2 ]
	ac = [0,uve[0].y - (uve[0].y + uve[1].y)/2 ]
		
	u = ab
	v = ac

	u_v = ab[0] * ac[0] + ab[1] * ac[1]

	_u_ = math.sqrt(ab[0]**2 + ab[1]**2)
	_v_ = math.sqrt(ac[0]**2 + ac[1]**2)

	_uv_ = _u_ * _v_

	
	i = 1
	while(_uv_ == 0 and i != len(uve)):
		ab = [uve[0].x - (uve[0].x + uve[i].x)/2  ,  uve[0].y - (uve[0].y + uve[i].y)/2 ]
		ac = [0,uve[0].y - (uve[0].y + uve[i].y)/2 ]
				
		u = ab
		v = ac

		u_v = ab[0] * ac[0] + ab[1] * ac[1]

		_u_ = math.sqrt(ab[0]**2 + ab[1]**2)
		_v_ = math.sqrt(ac[0]**2 + ac[1]**2)

		_uv_ = _u_ * _v_
		
		i += 1
		
	if _uv_ == 0:
		angle2 = 0
	else:    
		angle2 = math.degrees(math.acos(u_v/_uv_))
	
	
	if angle > angle2:
		angle = -angle2
		
	original_type = bpy.context.area.type
	bpy.context.area.type = "IMAGE_EDITOR"   
	
	bpy.ops.uv.snap_cursor(target='SELECTED')
	
	pivot_ori = bpy.context.space_data.pivot_point
	
	bpy.context.space_data.pivot_point = 'CURSOR'
		
	bpy.ops.uv.select_linked()

	
	bpy.ops.transform.rotate(value=math.radians(angle), orient_axis='Z', orient_type='VIEW', orient_matrix=((-1, -0, -0), (-0, -1, -0), (-0, -0, -1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)


	bpy.ops.uv.select_all(action='TOGGLE')

	uvee[0].select = True
	uvee[1].select = True

	ab = [uve[0].x - (uve[0].x + uve[1].x)/2  ,  uve[0].y - (uve[0].y + uve[1].y)/2 ]
	ac = [uve[0].x - (uve[0].x + uve[1].x)/2 , 0]
		
	u = ab
	v = ac

	u_v = ab[0] * ac[0] + ab[1] * ac[1]

	_u_ = math.sqrt(ab[0]**2 + ab[1]**2)
	_v_ = math.sqrt(ac[0]**2 + ac[1]**2)

	_uv_ = _u_ * _v_
	
	
	i = 1
	while(_uv_ == 0 and i != len(uve)):
		ab = [uve[0].x - (uve[0].x + uve[i].x)/2  ,  uve[0].y - (uve[0].y + uve[i].y)/2 ]
		ac = [uve[0].x - (uve[0].x + uve[i].x)/2 , 0]
		
		u_v = ab[0] * ac[0] + ab[1] * ac[1]

		_u_ = math.sqrt(ab[0]**2 + ab[1]**2)
		_v_ = math.sqrt(ac[0]**2 + ac[1]**2)

		_uv_ = _u_ * _v_
		
		i += 1
	
	if _uv_ == 0:
		aangle = 0
	else:    
		aangle = math.degrees(math.acos(u_v/_uv_)) 
	
	###########################################################
	
	ab = [uve[0].x - (uve[0].x + uve[1].x)/2  ,  uve[0].y - (uve[0].y + uve[1].y)/2 ]
	ac = [0,uve[0].y - (uve[0].y + uve[1].y)/2 ]
		
	u = ab
	v = ac

	u_v = ab[0] * ac[0] + ab[1] * ac[1]

	_u_ = math.sqrt(ab[0]**2 + ab[1]**2)
	_v_ = math.sqrt(ac[0]**2 + ac[1]**2)

	_uv_ = _u_ * _v_              
	
	
	i = 1
	while(_uv_ == 0 and i != len(uve)):
		ab = [uve[0].x - (uve[0].x + uve[i].x)/2  ,  uve[0].y - (uve[0].y + uve[i].y)/2 ]
		ac = [0,uve[0].y - (uve[0].y + uve[i].y)/2 ]
				
		u = ab
		v = ac

		u_v = ab[0] * ac[0] + ab[1] * ac[1]

		_u_ = math.sqrt(ab[0]**2 + ab[1]**2)
		_v_ = math.sqrt(ac[0]**2 + ac[1]**2)

		_uv_ = _u_ * _v_
		
		i += 1
	
	if _uv_ == 0:
		aangle2 = 0
	else:    
		aangle2 = math.degrees(math.acos(u_v/_uv_))
	
	if aangle == 0 or aangle2 == 0 or round(aangle) == 90 or round(aangle2) == 90:
		angle = 0
	elif aangle != 0 or aangle2 != 0:
		angle = angle * -2
	else:
		angle = 0
		
	bpy.ops.uv.select_linked()

	
	bpy.ops.transform.rotate(value=math.radians(angle), orient_axis='Z', orient_type='VIEW', orient_matrix=((-1, -0, -0), (-0, -1, -0), (-0, -0, -1)), orient_matrix_type='VIEW', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

	
	bpy.ops.uv.cursor_set(location=(0,0))
	
	bpy.ops.uv.select_all(action='TOGGLE')

	bmesh.update_edit_mesh(me)
	
	
	
	bpy.context.space_data.pivot_point = ''+pivot_ori+''
	
	bpy.context.area.type = original_type

	del(uve)




def Hard_edge_from_island(context):
	
	obj = context.active_object
	me = obj.data
	bm = bmesh.from_edit_mesh(me)
	uv_layer = bm.loops.layers.uv.verify()
	
	original_sync_mode = bpy.context.scene.tool_settings.use_uv_select_sync
	
	bpy.context.scene.tool_settings.use_uv_select_sync = True
	bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
	
		
	faceGroups = []
	
	faces = set(f for f in bm.faces if f.select)
	
	
	
	while faces:
		bpy.ops.mesh.select_all(action='DESELECT')  
		face = faces.pop()
		face.select = True
		bpy.ops.uv.select_linked()
		selected_faces = {f for f in bm.faces if f.select}
		faceGroups.append(selected_faces)
		faces -= selected_faces
		bpy.ops.uv.select_all(action='DESELECT')
		
	for i in faceGroups:
		g = list(i)
		g[0].select = True
		bpy.ops.uv.select_linked()
		bpy.ops.uv.hide(unselected=True)
		bpy.ops.mesh.region_to_loop()
		bpy.ops.mesh.mark_sharp()
		bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
		bpy.ops.uv.select_all(action='DESELECT')
		bpy.ops.uv.reveal()
		bpy.ops.uv.select_all(action='DESELECT')
	
	
	bpy.context.scene.tool_settings.use_uv_select_sync = original_sync_mode
	
	bmesh.update_edit_mesh(me)
	
	

def Pack_together(self, context):
	
	obj = context.active_object
	me = obj.data
	bm = bmesh.from_edit_mesh(me)
	uv_layer = bm.loops.layers.uv.verify()

	pivot_ori = bpy.context.space_data.pivot_point
	
	UV_verts = []
	c = 0
	
	for f in bm.faces:
		for l in f.loops:
				luv = l[uv_layer]
				if luv.select and luv.uv not in UV_verts and c != 2:
					UV_verts.append(luv.uv)
					c += 1

	if len(UV_verts) == 2:
	
		distance = math.sqrt((UV_verts[0].x - UV_verts[1].x)**2 + (UV_verts[0].y - UV_verts[1].y)**2)

		scene = context.scene
		mytool = scene.my_tool
		
		bpy.ops.uv.pack_islands(rotate=mytool.my_bool, margin=mytool.my_float)
		
		
		distance2 = math.sqrt((UV_verts[0].x - UV_verts[1].x)**2 + (UV_verts[0].y - UV_verts[1].y)**2)
		

		Scale = distance/distance2
				
		bpy.context.space_data.pivot_point = 'CURSOR'
		bpy.ops.uv.cursor_set(location=(0,0))
		
		bpy.ops.uv.select_linked()

		bpy.ops.transform.resize(value=(Scale,Scale,Scale), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
		
		bpy.context.space_data.pivot_point = ''+pivot_ori+''
	
	else:
		self.report({"ERROR"}, "No island selected")

########################################################################



class UvOperator(bpy.types.Operator):
	"""Align Island to closest x or y axis by selected edge"""
	bl_idname = "uv.simple_operator"
	bl_label = "Simple UV Operator"

	@classmethod
	def poll(cls, context):
		return (context.mode == 'EDIT_MESH')

	def execute(self, context):
	
		if bpy.context.scene.tool_settings.use_uv_select_sync == True:
				self.report({"WARNING"}, "'Align UV Island' works when UV Sync is off")
		else:
				main(context)
			
		return {'FINISHED'}


class UvOperator2(bpy.types.Operator):
	"""Mark edges as sharp from the islands' boundary edges"""
	bl_idname = "uv.simple_operator2"
	bl_label = "Simple UV Operator2"

	@classmethod
	def poll(cls, context):
		return (context.mode == 'EDIT_MESH')

	def execute(self, context):
		Hard_edge_from_island(context)
		return {'FINISHED'}
	

class UvOperator3(bpy.types.Operator):
	"""Pack Islands together while maintaining their size"""
	bl_idname = "uv.simple_operator3"
	bl_label = "Simple UV Operator3"

	@classmethod
	def poll(cls, context):
		return (context.mode == 'EDIT_MESH')

	def execute(self, context):
		
		if bpy.context.scene.tool_settings.use_uv_select_sync == True:
				self.report({"WARNING"}, "'Pack together' works when UV Sync is off")
		else:
				Pack_together(self, context)
				
		return {'FINISHED'}



def register():
	bpy.utils.register_class(MySettings)
	bpy.utils.register_class(Align_UV_Island)
	bpy.types.Scene.my_tool = PointerProperty(type=MySettings)
	bpy.utils.register_class(UvOperator)
	bpy.utils.register_class(UvOperator2)
	bpy.utils.register_class(UvOperator3)
	
	
def unregister():
	bpy.utils.unregister_class(MySettings)
	bpy.utils.unregister_class(Align_UV_Island)
	del bpy.types.Scene.my_tool
	bpy.utils.unregister_class(UvOperator)
	bpy.utils.unregister_class(UvOperator2)
	bpy.utils.unregister_class(UvOperator3)
	
if __name__ == "__main__":
	register()
