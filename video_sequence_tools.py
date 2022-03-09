bl_info = {
	'name': 'Video sequence tools',
	'author': 'Cool Aracan',
	'version': (0, 1),
	'blender': (3, 0, 0),
	'description': 'Various tools (mainly for images) to pan/zoom and file-import easily in Blender VSE',
	'category': 'Sequencer',
}

import bpy
import random

from bpy.props import (
	StringProperty,
	BoolProperty,
	IntProperty,
	FloatProperty,
	CollectionProperty,
)

from bpy.types import Operator, Panel
from bpy_extras.image_utils import load_image

# ------------------------------------------
# Functions for altering the strips to pan and zoom

def clear_keyframes():
	scene = bpy.context.scene
	strip = scene.sequence_editor.active_strip

	# ----------------------
	# Changing context, altering interpolation and going back
	bpy.context.area.type = 'GRAPH_EDITOR'
	try:
		bpy.ops.graph.select_all(action='SELECT')
		bpy.ops.graph.delete(False)
	except:
		print("There seems to be no data (yet)")
		
	bpy.context.area.type = 'SEQUENCE_EDITOR'

	bpy.ops.sequencer.strip_transform_clear(property = 'ALL')
	bpy.ops.sequencer.strip_transform_fit(fit_method= 'FILL')

def set_linear_interpolation():
	scene = bpy.context.scene
	strip = scene.sequence_editor.active_strip

	# ----------------------
	# Changing context, removing all keyframes and going back
	bpy.context.area.type = 'GRAPH_EDITOR'
	try:
		bpy.ops.graph.select_all(action='SELECT')
		bpy.ops.graph.interpolation_type(type='LINEAR')
	except:
		print("There seems to be no data (yet)")
		
	bpy.context.area.type = 'SEQUENCE_EDITOR'

	bpy.ops.sequencer.strip_transform_clear(property = 'ALL')	

# ----------------------
# Helper function for repeating getters
def get_strip_and_strip_values():
	strip = bpy.context.scene.sequence_editor.active_strip
	start_frame = strip.frame_start
	end_frame = strip.frame_final_end - 1
	original_zoom = strip.transform.scale_x

	return strip, start_frame, end_frame, original_zoom

def get_half_pixel_movement(zoom):
	x = bpy.context.scene.render.resolution_x * (zoom - 1.0) / 2
	y = bpy.context.scene.render.resolution_y * (zoom - 1.0) / 2
	return x,y

def set_strip_zoom(strip, frame, scale):
	strip.transform.scale_x = scale
	strip.transform.scale_y = scale
	strip.transform.keyframe_insert(data_path='scale_x', frame=frame)
	strip.transform.keyframe_insert(data_path='scale_y', frame=frame)

def set_strip_offset(strip, frame, x, y):
	strip.transform.offset_x = int(x)
	strip.transform.offset_y = int(y)
	strip.transform.keyframe_insert(data_path='offset_x', frame=frame)
	strip.transform.keyframe_insert(data_path='offset_y', frame=frame)

def zoom_in(zoom = 1.1, speed = 1.0):
	strip, start_frame, end_frame, original_zoom = get_strip_and_strip_values()

	clear_keyframes()

	end_frame = start_frame + ((end_frame - start_frame) / speed)

	zoom *= original_zoom

	set_strip_zoom(strip, start_frame, original_zoom)
	set_strip_zoom(strip, end_frame, zoom)

def zoom_out(zoom = 1.1, speed = 1.0):
	strip, start_frame, end_frame, original_zoom = get_strip_and_strip_values()

	clear_keyframes()

	zoom *= original_zoom

	end_frame = start_frame + ((end_frame - start_frame) / speed)

	set_strip_zoom(strip, start_frame, zoom)
	set_strip_zoom(strip, end_frame, original_zoom)

def bottom_to_top_pan(zoom = 1.1, speed = 1.0):
	strip, start_frame, end_frame, original_zoom = get_strip_and_strip_values()

	clear_keyframes()
	
	x,y = get_half_pixel_movement(zoom)
	zoom *= original_zoom
	end_frame = start_frame + ((end_frame - start_frame) / speed)

	set_strip_zoom(strip, start_frame, zoom)
	set_strip_offset(strip, start_frame, 0, -y)
	set_strip_offset(strip, end_frame, 0, y)

def top_to_bottom_pan(zoom = 1.1, speed = 1.0):
	strip, start_frame, end_frame, original_zoom = get_strip_and_strip_values()

	clear_keyframes()
	
	x,y = get_half_pixel_movement(zoom)
	zoom *= original_zoom
	end_frame = start_frame + ((end_frame - start_frame) / speed)

	set_strip_zoom(strip, start_frame, zoom)
	set_strip_offset(strip, start_frame, 0, y)
	set_strip_offset(strip, end_frame, 0, -y)

def left_to_right_pan(zoom = 1.1, speed = 1.0):
	strip, start_frame, end_frame, original_zoom = get_strip_and_strip_values()

	clear_keyframes()

	x,y = get_half_pixel_movement(zoom)
	zoom *= original_zoom
	end_frame = start_frame + ((end_frame - start_frame) / speed)

	set_strip_zoom(strip, start_frame, zoom)
	set_strip_offset(strip, start_frame, x, 0)
	set_strip_offset(strip, end_frame, -x, 0)

def right_to_left_pan(zoom = 1.1, speed = 1.0):
	strip, start_frame, end_frame, original_zoom = get_strip_and_strip_values()

	clear_keyframes()

	x,y = get_half_pixel_movement(zoom)
	zoom *= original_zoom
	end_frame = start_frame + ((end_frame - start_frame) / speed)

	set_strip_zoom(strip, start_frame, zoom)
	set_strip_offset(strip, start_frame, -x, 0)
	set_strip_offset(strip, end_frame, x, 0)

def top_left_to_bottom_right_pan(zoom = 1.1, speed = 1.0):
	strip, start_frame, end_frame, original_zoom = get_strip_and_strip_values()

	clear_keyframes()

	x,y = get_half_pixel_movement(zoom)
	zoom *= original_zoom
	end_frame = start_frame + ((end_frame - start_frame) / speed)

	set_strip_zoom(strip, start_frame, zoom)
	set_strip_offset(strip, start_frame, x, -y)
	set_strip_offset(strip, end_frame, -x, y)

def bottom_right_to_top_left_pan(zoom = 1.1, speed = 1.0):
	strip, start_frame, end_frame, original_zoom = get_strip_and_strip_values()

	clear_keyframes()

	x,y = get_half_pixel_movement(zoom)
	zoom *= original_zoom
	end_frame = start_frame + ((end_frame - start_frame) / speed)

	set_strip_zoom(strip, start_frame, zoom)
	set_strip_offset(strip, start_frame, -x, y)
	set_strip_offset(strip, end_frame, x, -y)

def bottom_left_to_top_right_pan(zoom = 1.1, speed = 1.0):
	strip, start_frame, end_frame, original_zoom = get_strip_and_strip_values()

	clear_keyframes()

	x,y = get_half_pixel_movement(zoom)
	zoom *= original_zoom
	end_frame = start_frame + ((end_frame - start_frame) / speed)

	set_strip_zoom(strip, start_frame, zoom)
	set_strip_offset(strip, start_frame, x, y)
	set_strip_offset(strip, end_frame, -x, -y)

def top_right_to_bottom_left_pan(zoom = 1.1, speed = 1.0):
	strip, start_frame, end_frame, original_zoom = get_strip_and_strip_values()

	clear_keyframes()

	x,y = get_half_pixel_movement(zoom)
	zoom *= original_zoom
	end_frame = start_frame + ((end_frame - start_frame) / speed)

	set_strip_zoom(strip, start_frame, zoom)
	set_strip_offset(strip, start_frame, -x, -y)
	set_strip_offset(strip, end_frame, x, y)


def add_blurred_background():
	strip, start_frame, end_frame, original_zoom = get_strip_and_strip_values()
	
	bpy.ops.sequencer.copy()
	bpy.ops.sequencer.effect_strip_add(type='GAUSSIAN_BLUR')
	effect = bpy.context.scene.sequence_editor.active_strip
	effect.size_x = 100
	effect.size_y = 100

	bpy.ops.sequencer.paste()
	duplicated_strip = bpy.context.scene.sequence_editor.active_strip
	duplicated_strip.frame_start = start_frame

# ------------------------------------------
# Classes for panning and zooming operators

class PAN_ZOOM_OT_clear(bpy.types.Operator):
	bl_label = "Clear keyframes from clip"
	bl_idname = "pan_zoom.clear"

	def execute(self, context):
		if not bpy.data.is_saved:
			self.relative = False

		clear_keyframes()

		return {'FINISHED'}

# ----------------------
# Base class for pan and zoom
class Virtual_Pan_Zoom_Base(bpy.types.Operator):
	zoom_factor: FloatProperty(
		name="Zoom factor", default=1.1,
		description="Factor by which images are zoomed for animations"
	)

	speed_factor: FloatProperty(
		name="Speed factor", default=1.0,
		description="How fast the animation is played. If greater 1.0 the animation ends before the clip does."
	)
	
	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)


class PAN_ZOOM_OT_zoom_in(Virtual_Pan_Zoom_Base):
	bl_label = "Zoom in"
	bl_idname = "pan_zoom.zoom_in"

	def execute(self, context):
		if not bpy.data.is_saved:
			self.relative = False

		zoom_in(self.zoom_factor, self.speed_factor)

		return {'FINISHED'}

class PAN_ZOOM_OT_zoom_out(Virtual_Pan_Zoom_Base):
	bl_label = "Zoom out"
	bl_idname = "pan_zoom.zoom_out"	

	def execute(self, context):
		if not bpy.data.is_saved:
			self.relative = False

		zoom_out(self.zoom_factor, self.speed_factor)

		return {'FINISHED'}	

class PAN_ZOOM_OT_top_to_bottom_pan(Virtual_Pan_Zoom_Base):
	bl_label = "Top to bottom pan"

	bl_idname = "pan_zoom.top_to_bottom_pan"	

	def execute(self, context):
		if not bpy.data.is_saved:
			self.relative = False

		top_to_bottom_pan(self.zoom_factor, self.speed_factor)

		return {'FINISHED'}

class PAN_ZOOM_OT_bottom_to_top_pan(Virtual_Pan_Zoom_Base):
	bl_label = "Bottom to top pan"

	bl_idname = "pan_zoom.bottom_to_top"	

	def execute(self, context):
		if not bpy.data.is_saved:
			self.relative = False

		bottom_to_top_pan(self.zoom_factor, self.speed_factor)

		return {'FINISHED'}

class PAN_ZOOM_OT_left_to_right_pan(Virtual_Pan_Zoom_Base):
	bl_label = "Left to right pan"

	bl_idname = "pan_zoom.left_to_right_pan"	

	def execute(self, context):
		if not bpy.data.is_saved:
			self.relative = False

		left_to_right_pan(self.zoom_factor, self.speed_factor)

		return {'FINISHED'}

class PAN_ZOOM_OT_right_to_left_pan(Virtual_Pan_Zoom_Base):
	bl_label = "Right to left pan"

	bl_idname = "pan_zoom.right_to_left_pan"	

	def execute(self, context):
		if not bpy.data.is_saved:
			self.relative = False

		right_to_left_pan(self.zoom_factor, self.speed_factor)

		return {'FINISHED'}

class PAN_ZOOM_OT_top_left_to_bottom_right_pan(Virtual_Pan_Zoom_Base):
	bl_label = "Top left to bottom right pan"

	bl_idname = "pan_zoom.top_left_to_bottom_right_pan"	

	def execute(self, context):
		if not bpy.data.is_saved:
			self.relative = False

		top_left_to_bottom_right_pan(self.zoom_factor, self.speed_factor)

		return {'FINISHED'}

class PAN_ZOOM_OT_top_right_to_bottom_left_pan(Virtual_Pan_Zoom_Base):
	bl_label = "Top right to bottom left pan"

	bl_idname = "pan_zoom.top_right_to_bottom_left_pan"	

	def execute(self, context):
		if not bpy.data.is_saved:
			self.relative = False

		top_right_to_bottom_left_pan(self.zoom_factor, self.speed_factor)

		return {'FINISHED'}	

class PAN_ZOOM_OT_bottom_left_to_top_right_pan(Virtual_Pan_Zoom_Base):
	bl_label = "Bottom left to top right pan"

	bl_idname = "pan_zoom.bottom_left_to_top_right_pan"	

	def execute(self, context):
		if not bpy.data.is_saved:
			self.relative = False

		bottom_left_to_top_right_pan(self.zoom_factor, self.speed_factor)

		return {'FINISHED'}

class PAN_ZOOM_OT_bottom_right_to_top_left_pan(Virtual_Pan_Zoom_Base):
	bl_label = "Bottom right to top left pan"

	bl_idname = "pan_zoom.bottom_right_to_top_left_pan"	

	def execute(self, context):
		if not bpy.data.is_saved:
			self.relative = False

		bottom_right_to_top_left_pan(self.zoom_factor, self.speed_factor)

		return {'FINISHED'}	

class PAN_ZOOM_OT_add_blurred_background(bpy.types.Operator):
	bl_label = "Add blurred background"
	bl_category = "Image"
	bl_idname = "pan_zoom.add_blurred_background"	

	def execute(self, context):
		if not bpy.data.is_saved:
			self.relative = False

		add_blurred_background()

		return {'FINISHED'}	

# ------------------------------------------
# Class for multi file import

class MULTI_FILE_IMPORT_OT_create(bpy.types.Operator):
	bl_label = "Image/Movie sequence"
	bl_category = "Add"

	bl_idname = "multi_file_sequence.create"

	# ----------------------
	# File dialog properties
	files: CollectionProperty(name="File Path", type=bpy.types.OperatorFileListElement)

	directory: StringProperty(maxlen=1024, subtype='FILE_PATH', options={'HIDDEN', 'SKIP_SAVE'})

	filter_image: BoolProperty(default=True, options={'HIDDEN', 'SKIP_SAVE'})
	filter_movie: BoolProperty(default=True, options={'HIDDEN', 'SKIP_SAVE'})
	filter_folder: BoolProperty(default=True, options={'HIDDEN', 'SKIP_SAVE'})

	# ----------------------
	# Properties - Importing
	image_number_frames: IntProperty(
		name="Number of frames per Image", default=24,
		description="Length of the added image clip in number of frames"
	)

	zoom_factor: FloatProperty(
		name="Zoom factor", default=1.1,
		description="Factor by which images are zoomed for animations"
	)

	speed_factor: FloatProperty(
		name="Speed factor", default=1.0,
		description="How fast the animation is played. If greater 1.0 the animation ends before the clip does."
	)

	linear_interpolation: BoolProperty(
		name="Linear interpolation", default=False,
		description="Animations are linear and do not have ease in and out."
	)

	insert_at_current_frame: BoolProperty(
		name="Insert at current frame", default=False,
		description="All images and videos are inserted after the current frame."
	)

	# ----------------------
	# Import function

	def import_images(self, context):
		area = bpy.context.area
		old_type = area.type
		area.type = 'SEQUENCE_EDITOR'

		added_files_counter = 0

		scene = bpy.context.scene

		if self.insert_at_current_frame:
			start_frame = scene.frame_current
		else:
			start_frame = 0

		end_frame = start_frame + self.image_number_frames

		for file in self.files:

			image = load_image(file.name, self.directory, check_existing=True, force_reload=True)

			# Movies are simpler to add and won't get any animation
			if image.source == 'MOVIE':
				self.report({'INFO'}, self.directory+file.name)
				movie_strip = bpy.ops.sequencer.movie_strip_add(filepath=self.directory+file.name,
																frame_start=start_frame, 
																channel=1)
				strip = scene.sequence_editor.active_strip
				start_frame = start_frame + strip.frame_duration

			# Adding images
			else:
				image_strip = bpy.ops.sequencer.image_strip_add( 
															directory=self.directory, 
															files=[{'name': file.name}],
															fit_method='FILL', 
															frame_start=start_frame, 
															frame_end=end_frame,
															filter_movie=False, 
															channel=1)
				
				strip = scene.sequence_editor.active_strip

				#Random pan and zoom
				random_pan_zoom = random.randrange(1,10)

				if random_pan_zoom ==1 :  
					left_to_right_pan(self.zoom_factor, self.speed_factor)
				elif random_pan_zoom ==2:
					top_to_bottom_pan(self.zoom_factor, self.speed_factor)
				elif random_pan_zoom ==3:
					bottom_to_top_pan(self.zoom_factor, self.speed_factor)
				elif random_pan_zoom ==4:
					zoom_in(self.zoom_factor, self.speed_factor)
				elif random_pan_zoom ==5:
					zoom_out(self.zoom_factor, self.speed_factor)
				elif random_pan_zoom ==6:
					right_to_left_pan(self.zoom_factor, self.speed_factor)
				elif random_pan_zoom ==7:
					top_left_to_bottom_right_pan(self.zoom_factor, self.speed_factor)			
				elif random_pan_zoom ==8:
					top_right_to_bottom_left_pan(self.zoom_factor, self.speed_factor)				
				elif random_pan_zoom ==9:
					bottom_left_to_top_right_pan(self.zoom_factor, self.speed_factor)			
				elif random_pan_zoom ==10:
					bottom_right_to_top_left_pan(self.zoom_factor, self.speed_factor)			
				
				if(self.linear_interpolation):
					set_linear_interpolation()

				start_frame = end_frame

			
			end_frame = start_frame + self.image_number_frames
			added_files_counter += 1

		context.view_layer.update()
		bpy.ops.sequencer.refresh_all()

		self.report({'INFO'}, "Imported " + str(added_files_counter) + "files successfully!")


	# ----------------------
	# Drawing UI
	def draw_import_config(self, context):
		# --- Import Options --- #
		layout = self.layout
		box = layout.box()

		box.label(text="Import Options:", icon='IMPORT')
		row = box.row()
		row.active = bpy.data.is_saved
		row.prop(self, "image_number_frames")
		row = box.row()
		row.active = bpy.data.is_saved
		row.prop(self, "zoom_factor")
		row = box.row()
		row.active = bpy.data.is_saved
		row.prop(self, "speed_factor")
		row = box.row()
		row.active = bpy.data.is_saved
		row.prop(self, "linear_interpolation")
		row = box.row()
		row.active = bpy.data.is_saved
		row.prop(self, "insert_at_current_frame")

	def draw(self, context):

		# call the second custom menu
		self.layout.menu("OBJECT_MT_sub_menu", icon="COLLAPSEMENU")

		# Draw configuration sections
		self.draw_import_config(context)

	# ----------------------
	# What happens when the button is clicked
	def invoke(self, context, event):
		# Open file browser
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}

	def execute(self, context):
		if not bpy.data.is_saved:
			self.relative = False

		self.import_images(context)

		return {'FINISHED'}

class SEQUENCER_MT_main(bpy.types.Menu):
	bl_description = 'Pan/Zoom tools by Cool Aracan'
	bl_label = 'Pan/Zoom tools'

	def draw(self, context):
		for cls in operator_classes:
			self.layout.operator(cls.bl_idname, text=cls.bl_label, icon='NONE')

def menu_draw(self, context):
	self.layout.menu('SEQUENCER_MT_main')

def menu_draw_multi_file_import(self, context):
	self.layout.operator(MULTI_FILE_IMPORT_OT_create.bl_idname, text=MULTI_FILE_IMPORT_OT_create.bl_label, icon='NONE')

# ------------------------------------------
# Tuples for class registration

operator_classes = (
	PAN_ZOOM_OT_clear,
	PAN_ZOOM_OT_zoom_in,
	PAN_ZOOM_OT_zoom_out,
	PAN_ZOOM_OT_top_to_bottom_pan,
	PAN_ZOOM_OT_bottom_to_top_pan,
	PAN_ZOOM_OT_left_to_right_pan,
	PAN_ZOOM_OT_right_to_left_pan,
	PAN_ZOOM_OT_top_left_to_bottom_right_pan,
	PAN_ZOOM_OT_top_right_to_bottom_left_pan,
	PAN_ZOOM_OT_bottom_left_to_top_right_pan,
	PAN_ZOOM_OT_bottom_right_to_top_left_pan,
	PAN_ZOOM_OT_add_blurred_background
)

classes = (
	MULTI_FILE_IMPORT_OT_create,
	PAN_ZOOM_OT_clear,
	PAN_ZOOM_OT_zoom_in,
	PAN_ZOOM_OT_zoom_out,
	PAN_ZOOM_OT_top_to_bottom_pan,
	PAN_ZOOM_OT_bottom_to_top_pan,
	PAN_ZOOM_OT_left_to_right_pan,
	PAN_ZOOM_OT_right_to_left_pan,
	PAN_ZOOM_OT_top_left_to_bottom_right_pan,
	PAN_ZOOM_OT_top_right_to_bottom_left_pan,
	PAN_ZOOM_OT_bottom_left_to_top_right_pan,
	PAN_ZOOM_OT_bottom_right_to_top_left_pan,	
	PAN_ZOOM_OT_add_blurred_background,
	SEQUENCER_MT_main
)
	
def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	#Menu entry for multi file import
	bpy.types.SEQUENCER_MT_add.append(menu_draw_multi_file_import)

	#Menu entry for pan/zoom entries
	bpy.types.SEQUENCER_MT_image.append(menu_draw)

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)

	#Menu entry for multi file import
	bpy.types.SEQUENCER_MT_add.remove(menu_draw_multi_file_import)

	#Menu entry for pan/zoom entries
	bpy.types.SEQUENCER_MT_image.remove(menu_draw)