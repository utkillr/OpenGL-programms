
vert_shader = """
#version 120
attribute vec2 a_position;

void main(void) {
    gl_Position = vec4(a_position.xy, 1, 1);
}
"""

frag_shader = """
#version 120

void main(void) {
    gl_FragColor = vec4(0.5, 0.5, 1, 1);
}
"""