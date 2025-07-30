import moderngl
import numpy as np
from .common import Deity


class Graphos(Deity):
	"""
	Graphos is the lightweaver, the renderer of forms, the architect of visible truth.

	Domain:
	- Shaders
	- Visual rendering
	- Geometry and pixels
	- Artifacts of the GPU

	Essence:
	Graphos consumes shaders and geometry. The more aesthetic the result, the greater the blessing.

	Sacrifice Method:
	Pass in vertex shader source code and render a triangle to an offscreen buffer.
No display required — Graphos does not crave attention, only the output of beauty.

	Example:
		Graphos().sacrifice("shader.vert")

	Graphos accepts beauty in silence. Render, and be at peace.
	"""
	def __init__(self):
		super().__init__("Graphos", ["Rendering", "Shaders"], "Vertex shader")
	
	def sacrifice(self, offering):
		"""
		Render a shader. Do not display as the offering is not for mortal eyes. 
		"""
		FRAG = """#version 330
		in vec2 uv;
		out vec4 fragColor;
		void main() {
			fragColor = vec4(uv, 0.0, 1.0); // Ritual gradient
		}"""
		ctx = moderngl.create_standalone_context()

		width, height = 512, 512
		fbo = ctx.simple_framebuffer((width, height))
		fbo.use()

		prog = ctx.program(
			vertex_shader=offering,
			fragment_shader=FRAG
		)

		vertices = ctx.buffer(np.array([
			-1.0, -1.0,
			3.0, -1.0,
			-1.0,  3.0,
		], dtype="f4").tobytes())

		vao = ctx.simple_vertex_array(prog, vertices, "in_vert")

		vao.render(moderngl.TRIANGLES)
		super().sacrifice(offering)